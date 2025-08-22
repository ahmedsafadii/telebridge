"""
Models for Telegram targets (destination channels/groups).
"""

from django.db import models
from apps.core.models import TimeStampedModel, ValidationStatus
from apps.accounts.models import TelegramAccount


class TargetType(models.TextChoices):
    """
    Choices for target types.
    """
    TELEGRAM = 'telegram', 'Telegram'
    EMAIL = 'email', 'Email'


class Target(TimeStampedModel):
    """
    Model to store target information for message forwarding.
    """
    name = models.CharField(max_length=100, help_text="Friendly name for this target")
    target_type = models.CharField(
        max_length=10,
        choices=TargetType.choices,
        default=TargetType.TELEGRAM
    )
    
    # Telegram target fields
    account = models.ForeignKey(
        TelegramAccount,
        on_delete=models.CASCADE,
        related_name='targets',
        null=True,
        blank=True
    )
    channel_identifier = models.CharField(
        max_length=500,
        blank=True,
        help_text="Channel identifier (username, ID, or invite link)"
    )
    
    # Email target fields
    email_address = models.EmailField(blank=True)
    
    # Common fields
    is_active = models.BooleanField(default=True)
    
    # Validation information
    last_validated_at = models.DateTimeField(null=True, blank=True)
    last_validation_status = models.CharField(
        max_length=20,
        choices=ValidationStatus.choices,
        default=ValidationStatus.UNKNOWN
    )
    last_validation_error = models.TextField(blank=True)

    class Meta:
        verbose_name = "Target"
        verbose_name_plural = "Targets"
        ordering = ['name']

    def __str__(self):
        if self.target_type == TargetType.TELEGRAM:
            return f"{self.name} (Telegram: {self.channel_identifier})"
        else:
            return f"{self.name} (Email: {self.email_address})"

    def clean(self):
        """Validate the model."""
        from django.core.exceptions import ValidationError
        
        if self.target_type == TargetType.TELEGRAM:
            if not self.account:
                raise ValidationError("Account is required for Telegram targets")
            if not self.channel_identifier:
                raise ValidationError("Channel identifier is required for Telegram targets")
        elif self.target_type == TargetType.EMAIL:
            if not self.email_address:
                raise ValidationError("Email address is required for email targets")

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
        """Check if the target is valid."""
        return self.last_validation_status == ValidationStatus.OK


class SourceTargetMapping(TimeStampedModel):
    """
    Model to map sources to targets for message forwarding.
    """
    source = models.ForeignKey(
        'sources.Source',
        on_delete=models.CASCADE,
        related_name='target_mappings'
    )
    target = models.ForeignKey(
        Target,
        on_delete=models.CASCADE,
        related_name='source_mappings'
    )
    is_active = models.BooleanField(default=True)
    
    # Processing options
    delay_seconds = models.PositiveIntegerField(
        default=0,
        help_text="Delay in seconds before processing"
    )
    max_retries = models.PositiveIntegerField(
        default=3,
        help_text="Maximum number of retry attempts"
    )

    class Meta:
        verbose_name = "Source-Target Mapping"
        verbose_name_plural = "Source-Target Mappings"
        unique_together = ['source', 'target']
        ordering = ['source', 'target']

    def __str__(self):
        return f"{self.source} → {self.target}"
