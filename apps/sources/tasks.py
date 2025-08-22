"""
Celery tasks for Telegram sources.
"""

from celery import shared_task
from django.utils import timezone
from .models import Source
from apps.core.models import ValidationStatus


@shared_task
def validate_source(source_id):
    """
    Validate a Telegram source (channel/group).
    """
    try:
        source = Source.objects.get(id=source_id)
        
        # This would integrate with Telethon to validate the source
        # For now, we'll just update the timestamp
        source.update_validation_status(ValidationStatus.OK)
        
        return f"Source {source.input_identifier} validated successfully"
    except Source.DoesNotExist:
        return f"Source with ID {source_id} not found"


@shared_task
def validate_all_sources():
    """
    Validate all active sources.
    """
    sources = Source.objects.filter(is_active=True)
    results = []
    
    for source in sources:
        try:
            # This would integrate with Telethon to validate the source
            source.update_validation_status(ValidationStatus.OK)
            results.append(f"Source {source.input_identifier} validated successfully")
        except Exception as e:
            source.update_validation_status(ValidationStatus.FAILED, str(e))
            results.append(f"Source {source.input_identifier} validation failed: {str(e)}")
    
    return results


@shared_task
def process_source_messages(source_id):
    """
    Process messages from a source and forward/copy to targets.
    """
    try:
        source = Source.objects.get(id=source_id, is_active=True)
        
        # This would integrate with Telethon to:
        # 1. Get messages from the source
        # 2. Apply rules (whitelist/blacklist, text replacement, etc.)
        # 3. Forward/copy to mapped targets
        
        return f"Messages processed for source {source.input_identifier}"
    except Source.DoesNotExist:
        return f"Source with ID {source_id} not found"


@shared_task
def monitor_sources():
    """
    Monitor all active sources for new messages.
    """
    sources = Source.objects.filter(is_active=True, last_validation_status=ValidationStatus.OK)
    
    for source in sources:
        # This would check for new messages and trigger processing
        process_source_messages.delay(source.id)
    
    return f"Monitoring completed for {sources.count()} sources"
