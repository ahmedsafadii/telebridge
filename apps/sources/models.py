"""
Models for Telegram sources (channels/groups).
"""

from django.db import models
from apps.core.models import TimeStampedModel, ValidationStatus
from apps.accounts.models import TelegramAccount


class SourceMode(models.TextChoices):
    """
    Choices for source modes.
    """
    COPY = 'copy', 'Copy'
    FORWARD = 'forward', 'Forward'


class Source(TimeStampedModel):
    """
    Model to store Telegram source information (channels/groups).
    """
    account = models.ForeignKey(
        TelegramAccount,
        on_delete=models.CASCADE,
        related_name='sources'
    )
    input_identifier = models.CharField(
        max_length=500,
        help_text="Channel identifier (username, ID, or invite link)"
    )
    is_active = models.BooleanField(default=True)
    show_source = models.BooleanField(
        default=True,
        help_text="Show source information in forwarded messages"
    )
    mode = models.CharField(
        max_length=10,
        choices=SourceMode.choices,
        default=SourceMode.COPY,
        help_text="Copy or forward mode"
    )
    
    # Channel information (populated after validation)
    channel_id = models.BigIntegerField(null=True, blank=True)
    username = models.CharField(max_length=100, blank=True)
    title = models.CharField(max_length=255, blank=True)
    invite_link = models.URLField(blank=True)
    is_private = models.BooleanField(default=False)
    
    # Validation information
    last_validated_at = models.DateTimeField(null=True, blank=True)
    last_validation_status = models.CharField(
        max_length=20,
        choices=ValidationStatus.choices,
        default=ValidationStatus.UNKNOWN
    )
    last_validation_error = models.TextField(blank=True)

    class Meta:
        verbose_name = "Source"
        verbose_name_plural = "Sources"
        ordering = ['-created_at']
        unique_together = ['account', 'input_identifier']

    def __str__(self):
        return f"{self.title or self.input_identifier} ({self.account.name})"

    def update_validation_status(self, status, error_message=""):
        """Update validation status and error message."""
        from django.utils import timezone
        
        self.last_validation_status = status
        self.last_validation_error = error_message
        self.last_validated_at = timezone.now()
        self.save(update_fields=[
            'last_validation_status', 
            'last_validation_error', 
            'last_validated_at'
        ])

    def is_valid(self):
        """Check if the source is valid."""
        return self.last_validation_status == ValidationStatus.OK

    def get_display_identifier(self):
        """Get display identifier for the source."""
        if self.username:
            return f"@{self.username}"
        elif self.channel_id:
            return str(self.channel_id)
        else:
            return self.input_identifier
