from django import forms
from about.models import *
from hospital_admin.models import *
from authentication.forms import FormSettings


class HospitalForm(FormSettings):
    class Meta:
        model = Hospital
        fields = '__all__'


class EquipmentsForm(FormSettings):
    class Meta:
        model = Equipment
        fields = ['hospital', 'equipment_type', 'unit', 'model_number', 'company_name', 'suppliers', 'remarks',
                  'operational', 'not_operational', 'in_maintenance', 'total_equipments']


class EquipmentsUpdateForm(FormSettings):
    hospital = forms.CharField(
        widget=forms.TextInput(attrs={'readonly': 'readonly'})
    )

    class Meta:
        model = Equipment
        fields = ['hospital', 'equipment_type', 'unit', 'model_number', 'company_name', 'suppliers', 'remarks',
                  'operational', 'not_operational', 'in_maintenance', 'total_equipments']


class RequestForm(FormSettings):
    class Meta:
        model = HelpRequest
        fields = ['request_status']


