import django_filters
from about.models import Trainer


class LocationFilter(django_filters.FilterSet):
    class Meta:
        model = Trainer
        fields = [
            'province',
            'district',
            'municipality',
            'certification_from_mot'
        ]