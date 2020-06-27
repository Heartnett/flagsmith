from django.dispatch import receiver
from simple_history.signals import post_create_historical_record

from audit.models import AuditLog, RelatedObjectType, FEATURE_SEGMENT_UPDATED_MESSAGE
from util.logging import get_logger
# noinspection PyUnresolvedReferences
from .models import HistoricalFeatureSegment

logger = get_logger(__name__)


@receiver(post_create_historical_record, sender=HistoricalFeatureSegment)
def create_feature_segment_audit_log(instance, history_user, **kwargs):
    message = FEATURE_SEGMENT_UPDATED_MESSAGE % (instance.feature.name, instance.environment.name)
    AuditLog.create_record(
        obj=instance.feature,
        obj_type=RelatedObjectType.FEATURE,
        log_message=message,
        author=history_user,
        project=instance.feature.project
    )
