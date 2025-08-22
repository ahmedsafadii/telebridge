"""
Telegram client service for account management.
"""

import asyncio
import os
from telethon import TelegramClient
from telethon.errors import (
    PhoneCodeInvalidError, 
    PhoneCodeExpiredError,
    SessionPasswordNeededError,
    PhoneNumberInvalidError
)
from django.conf import settings
from django.utils import timezone
from .models import TelegramAccount


class TelegramClientService:
    """Service for managing Telegram client operations."""
    
    def __init__(self, account):
        """Initialize with a TelegramAccount instance."""
        self.account = account
        self.client = None
        
    def get_session_path(self):
        """Get the session file path for this account."""
        sessions_dir = os.path.join(settings.BASE_DIR, 'sessions')
        os.makedirs(sessions_dir, exist_ok=True)
        return os.path.join(sessions_dir, f'session_{self.account.id}')
    
    async def create_client(self):
        """Create and return a TelegramClient instance."""
        if not self.account.api_id or not self.account.api_hash:
            raise ValueError("API ID and API Hash are required")
            
        session_path = self.get_session_path()
        self.client = TelegramClient(
            session_path,
            self.account.api_id,
            self.account.api_hash
        )
        return self.client
    
    async def start_login_process(self):
        """Start the login process by sending phone code."""
        try:
            client = await self.create_client()
            await client.connect()
            
            # Send code request
            phone_code_hash = await client.send_code_request(self.account.phone_number)
            
            # Update account status
            self.account.session_status = 'phone_code_sent'
            self.account.pending_phone = self.account.phone_number
            self.account.phone_code_hash = phone_code_hash.phone_code_hash
            self.account.save()
            
            await client.disconnect()
            return True, "Phone code sent successfully"
            
        except PhoneNumberInvalidError:
            return False, "Invalid phone number"
        except Exception as e:
            return False, f"Error starting login: {str(e)}"
    
    async def confirm_phone_code(self, phone_code):
        """Confirm the phone code and complete login."""
        try:
            client = await self.create_client()
            await client.connect()
            
            # Sign in with phone code
            await client.sign_in(
                self.account.phone_number,
                phone_code,
                phone_code_hash=self.account.phone_code_hash
            )
            
            # Update account status
            self.account.session_status = 'active'
            self.account.pending_phone = None
            self.account.phone_code_hash = None
            self.account.last_check_at = timezone.now()
            self.account.save()
            
            await client.disconnect()
            return True, "Login successful"
            
        except PhoneCodeInvalidError:
            return False, "Invalid phone code"
        except PhoneCodeExpiredError:
            return False, "Phone code expired"
        except SessionPasswordNeededError:
            # Handle 2FA password
            self.account.session_status = 'password_needed'
            self.account.save()
            await client.disconnect()
            return False, "Two-factor authentication required"
        except Exception as e:
            return False, f"Error confirming code: {str(e)}"
    
    async def confirm_password(self, password):
        """Confirm 2FA password."""
        try:
            client = await self.create_client()
            await client.connect()
            
            # Sign in with password
            await client.sign_in(password=password)
            
            # Update account status
            self.account.session_status = 'active'
            self.account.last_check_at = timezone.now()
            self.account.save()
            
            await client.disconnect()
            return True, "Two-factor authentication successful"
            
        except Exception as e:
            return False, f"Error confirming password: {str(e)}"
    
    async def check_status(self):
        """Check if the account is still active."""
        try:
            client = await self.create_client()
            await client.connect()
            
            # Check if we're authorized
            if await client.is_user_authorized():
                self.account.session_status = 'active'
                self.account.last_check_at = timezone.now()
                self.account.last_error = None
                self.account.save()
                await client.disconnect()
                return True, "Account is active"
            else:
                self.account.session_status = 'unknown'
                self.account.save()
                await client.disconnect()
                return False, "Account not authorized"
                
        except Exception as e:
            self.account.session_status = 'error'
            self.account.last_error = str(e)
            self.account.save()
            return False, f"Error checking status: {str(e)}"
    
    async def logout(self):
        """Logout and clear session."""
        try:
            client = await self.create_client()
            await client.connect()
            
            if await client.is_user_authorized():
                await client.log_out()
            
            await client.disconnect()
            
            # Clear session file
            session_path = self.get_session_path()
            if os.path.exists(session_path + '.session'):
                os.remove(session_path + '.session')
            
            # Update account status
            self.account.session_status = 'unknown'
            self.account.pending_phone = None
            self.account.phone_code_hash = None
            self.account.save()
            
            return True, "Logout successful"
            
        except Exception as e:
            return False, f"Error logging out: {str(e)}"


def run_async(coro):
    """Helper function to run async code in sync context."""
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    
    return loop.run_until_complete(coro)
