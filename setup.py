#!/usr/bin/env python3
"""
Setup script for TeleBridge project.
"""

import os
import subprocess
import sys
from pathlib import Path


def run_command(command, description):
    """Run a command and handle errors."""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False


def main():
    """Main setup function."""
    print("🚀 Setting up TeleBridge project...")
    
    # Check if Python is available
    if not run_command("python --version", "Checking Python installation"):
        return False
    
    # Create virtual environment
    if not os.path.exists("venv"):
        if not run_command("python -m venv venv", "Creating virtual environment"):
            return False
    
    # Activate virtual environment and install dependencies
    if sys.platform == "win32":
        activate_cmd = "venv\\Scripts\\activate"
        pip_cmd = "venv\\Scripts\\pip"
    else:
        activate_cmd = "source venv/bin/activate"
        pip_cmd = "venv/bin/pip"
    
    if not run_command(f"{pip_cmd} install -r requirements.txt", "Installing dependencies"):
        return False
    
    # Create environment file if it doesn't exist
    if not os.path.exists(".env"):
        if os.path.exists("env.example"):
            if not run_command("copy env.example .env", "Creating .env file from template"):
                return False
            print("⚠️  Please edit .env file with your configuration before running the project")
    
    # Run migrations
    if not run_command("python manage.py migrate --settings=telebridge.settings.development", "Running database migrations"):
        return False
    
    # Create superuser
    print("🔄 Creating superuser...")
    print("Please enter the following information for the admin user:")
    if not run_command("python manage.py createsuperuser --settings=telebridge.settings.development", "Creating superuser"):
        print("⚠️  Superuser creation failed, you can create it manually later")
    
    # Initialize sample data
    if not run_command("python manage.py init_sample_data --settings=telebridge.settings.development", "Initializing sample data"):
        print("⚠️  Sample data initialization failed")
    
    print("\n🎉 Setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Edit .env file with your configuration")
    print("2. Start Redis server: redis-server")
    print("3. Start Celery worker: celery -A telebridge worker -l info")
    print("4. Start Celery beat: celery -A telebridge beat -l info")
    print("5. Start Django server: python manage.py runserver --settings=telebridge.settings.development")
    print("6. Visit http://127.0.0.1:8000/admin to access the admin interface")
    
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
