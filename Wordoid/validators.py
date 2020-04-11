from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_text(value):
    # import pdb;pdb.set_trace()
    if len(value) <= 2:
        raise ValidationError(
            _('%(value)s is too short'),
            params={'value': value},
        )
