from django.db import models
from tinymce.models import HTMLField
from django.shortcuts import reverse
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from PIL import Image
from io import BytesIO
from django.conf import settings
from django.core.files.storage import default_storage
from authentication.models import User


def upload_about_picture(instance, filename):
    return "about/pictures/{id}_{host_to}/{filename}".format(host_to=instance.full_name, filename=filename,
                                                             id=instance.id)


def upload_about_resume(instance, filename):
    return "about/resumes/{id}_{host_to}/{filename}".format(host_to=instance.full_name, filename=filename,
                                                            id=instance.id)


def upload_about_organization_picture(instance, filename):
    return "about/pictures/{id}_{host_to}/{filename}".format(host_to=instance.title, filename=filename, id=instance.id)


def upload_resources_image(instance, filename):
    return "about/resources/{id}_{host_to}/{filename}".format(host_to=instance.title, filename=filename, id=instance.id)


def upload_solve_files(instance, filename):
    return "about/solve/{id}/{filename}".format(filename=filename, id=instance.id)


def community_member_image(instance, filename):
    return "about/resources/{id}_{host_to}/{filename}".format(host_to=instance.name, filename=filename, id=instance.id)


def trainer_profile(instance, filename):
    return "about/resources/{id}_{host_to}/{filename}".format(host_to=instance.name, filename=filename, id=instance.id)


def trainer_document(instance, filename):
    return "static/about/trainer/document/{id}_{host_to}/{filename}".format(host_to=instance.name, filename=filename, id=instance.id)

class Team(models.Model):
    types = (
        ('L', 'Leads'),
        ('M', 'Members'),
        ('T', 'Management')
    )

    lead_types_options = (
        ('P', 'Provincial Lead'),
        ('T', 'Team Lead')
    )
    member_type = models.CharField(max_length=1, choices=types, null=True, blank=True)
    # account_from = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.EmailField()
    lead_type = models.CharField(max_length=1, default='P', choices=lead_types_options, null=True, blank=True)
    province = models.CharField(max_length=255)
    profile_picture = models.ImageField(upload_to=upload_about_picture, null=True, blank=True)
    full_name = models.CharField(max_length=255)
    position = models.CharField(max_length=255)
    primary_contact = models.CharField(max_length=14, null=True, blank=True)
    secondary_contact = models.CharField(max_length=14, null=True, blank=True)
    qualifications = models.CharField(max_length=1024)
    description = models.CharField(max_length=1024)
    resume = models.FileField(upload_to=upload_about_resume, null=True, blank=True)
    is_approved = models.BooleanField(default=False)
    province_np = models.CharField(max_length=255, null=True, blank=True)
    full_name_np = models.CharField(max_length=255, null=True, blank=True)
    position_np = models.CharField(max_length=255, null=True, blank=True)
    primary_contact_np = models.CharField(max_length=14, null=True, blank=True)
    secondary_contact_np = models.CharField(max_length=14, null=True, blank=True)
    qualifications_np = models.CharField(max_length=1024, null=True, blank=True)
    description_np = models.CharField(max_length=1024, null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    edited_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.full_name


class Organization(models.Model):
    category_type = (
        ('L', 'Leading'),
        ('S', 'Support'),
        ('C', 'Co-Support'),
    )
    title = models.CharField(max_length=255)
    logo = models.ImageField(upload_to=upload_about_organization_picture, null=True, blank=True)
    category = models.CharField(max_length=2, choices=category_type, default='C', null=True, blank=True)
    description = models.CharField(max_length=1024, null=True, blank=True)
    contact_number = models.CharField(max_length=14, null=True, blank=True)
    contact_email = models.CharField(max_length=255, null=True, blank=True)
    contact_website = models.CharField(max_length=255, null=True, blank=True)
    contact_social_media = models.CharField(max_length=1024, null=True, blank=True)
    title_np = models.CharField(max_length=255)
    description_np = models.CharField(max_length=1024, null=True, blank=True)
    contact_number_np = models.CharField(max_length=14, null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    edited_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Province(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class District(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)
    province = models.ForeignKey('Province', related_name='district',
                                 on_delete=models.CASCADE)

    def __str__(self):
        return str(self.name)


class Municipality(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)
    province = models.ForeignKey('Province', related_name='municipality',
                                 on_delete=models.CASCADE, blank=True, null=True)
    district = models.ForeignKey('District', related_name='municipality',
                                 on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Municipalities"

    def __str__(self):
        return self.name


class Ward(models.Model):
    name = models.CharField(max_length=50)
    province = models.ForeignKey('Province', related_name='ward',
                                 on_delete=models.CASCADE, blank=True, null=True)
    district = models.ForeignKey('District', related_name='ward',
                                 on_delete=models.CASCADE)
    municipality = models.ForeignKey('Municipality', related_name='ward',
                                     on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class EquipmentInfo(models.Model):
    EQUIPMENTS = (
        ('ICU Machine', 'ICU Machine'),
        ('Ventilator Machine', 'Ventilator Machine'),
        ('Patient Monitor', 'Patient Monitor'),
        ('Infusion Pump', 'Infusion Pump'),
        ('Suction Pump', 'Suction Pump'),
        ('X-ray Machine', 'X-ray Machine'),
        ('Arterial Blood Gas (ABG) Machine', 'Arterial Blood Gas (ABG) Machine'),
        ('Defibrillator', 'Defibrillator'),
        ('BiPap Machine (bilevel positive airway pressure)', 'BiPap Machine (bilevel positive airway pressure)'),
        ('CPAP Machine (Continuous positive airway pressure', 'CPAP Machine (Continuous positive airway pressure'),
        ('High flow Nasal Cannula', 'High flow Nasal Cannula'),
        ('ECG Machine', 'ECG Machine'),
        ('Oxygen Concentrator', 'Oxygen Concentrator'),
        ('Autoclave Machine', 'Autoclave Machine'),
        ('BSC Level', 'BSC Level'),
        ('Automated Extraction', 'Automated Extraction'),
        ('PCR Machine', 'PCR Machine'),
    )
    name = models.CharField(max_length=255, choices=EQUIPMENTS, null=True, blank=True)
    equipments_before_covid = models.CharField(max_length=255, null=True, blank=True)
    equipments_after_covid = models.CharField(max_length=255, null=True, blank=True)
    operational = models.CharField(max_length=255, null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    edited_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Hospital(models.Model):
    patient_emergency_count = (
        ('Never', 'Never'),
        ('Rarely (1-3 patients/month', 'Rarely (1-3 patients/month'),
        ('Many times (4-9 patients/month', 'Many times (4-9 patients/month'),
        ('Frequently (410 patients/month', 'Frequently (410 patients/month'),
        ('I do not know', 'I do not know')
    )
    expenditure = (
        ('Less than 1 lakh', 'Less than 1 lakh'),
        ('1-50 lakh', '1-50 lakh'),
        ('50 lakh - 1 crore', '50 lakh - 1 crore'),
        ('more than 1 crore', 'more than 1 crore')
    )
    option = (
        ('yes', 'yes'),
        ('no', 'No')
    )
    RAM = (
        ('Twice in a year', 'Twice in an year'),
        ('Once a year', 'Once a year'),
        ('After problem arises', 'After problem arises'),
        ('other', 'other')
    )
    REPAIRE = (
        ('self', 'self'),
        ('from others', 'from others')
    )
    name = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=255, null=True, blank=True)
    contact_email = models.CharField(max_length=255, null=True, blank=True)
    province = models.ForeignKey('Province', related_name='hospital',
                                 on_delete=models.CASCADE, blank=True, null=True)
    district = models.ForeignKey('District', related_name='hospital',
                                 on_delete=models.CASCADE, blank=True, null=True)
    municipality = models.ForeignKey('Municipality', related_name='hospital',
                                     on_delete=models.CASCADE, blank=True, null=True)
    ward = models.ForeignKey('Ward', related_name='hospital',
                             on_delete=models.CASCADE, blank=True, null=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    name_np = models.CharField(max_length=255, null=True, blank=True)
    contact_number_np = models.CharField(max_length=255, null=True, blank=True)
    contact_email_np = models.CharField(max_length=255, null=True, blank=True)
    province_np = models.CharField(max_length=255, null=True, blank=True)
    address_np = models.CharField(max_length=255, null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    edited_date = models.DateTimeField(auto_now=True)

    icu_beds = models.IntegerField(null=True, blank=True, default=0)
    hdu_beds = models.IntegerField(null=True, blank=True, default=0)
    hfnc_beds = models.IntegerField(null=True, blank=True, default=0)
    isolation_beds = models.IntegerField(null=True, blank=True, default=0)
    oxygen_supplied_beds = models.IntegerField(null=True, blank=True, default=0)

    doctor_permanents_staff = models.IntegerField(null=True, blank=True, default=0)
    doctor_temperoray_staff = models.IntegerField(null=True, blank=True, default=0)
    doctor_development_staff = models.IntegerField(null=True, blank=True, default=0)

    nurse_permanent_staff = models.IntegerField(null=True, blank=True, default=0)
    nurse_temperoray_staff = models.IntegerField(null=True, blank=True, default=0)
    nurse_development_staff = models.IntegerField(null=True, blank=True, default=0)

    pharmacist_permanent_staff = models.IntegerField(null=True, blank=True, default=0)
    pharmacist_temperoray_staff = models.IntegerField(null=True, blank=True, default=0)
    pharmacist_development_staff = models.IntegerField(null=True, blank=True, default=0)

    biomedical_engineer_permanent_staff = models.IntegerField(null=True, blank=True, default=0)
    biomedical_engineer_temperoray_staff = models.IntegerField(null=True, blank=True, default=0)
    biomedical_engineer_development_staff = models.IntegerField(null=True, blank=True, default=0)

    biomedical_technician_permanent_staff = models.IntegerField(null=True, blank=True, default=0)
    biomedical_technician_temperoray_staff = models.IntegerField(null=True, blank=True, default=0)
    biomedical_technician_development_staff = models.IntegerField(null=True, blank=True, default=0)

    health_assistant_permanent_staff = models.IntegerField(null=True, blank=True, default=0)
    health_assistant_temperoray_staff = models.IntegerField(null=True, blank=True, default=0)
    health_assistant_development_staff = models.IntegerField(null=True, blank=True, default=0)

    lab_technician_permanent_staff = models.IntegerField(null=True, blank=True, default=0)
    lab_technician_temperoray_staff = models.IntegerField(null=True, blank=True, default=0)
    lab_technician_development_staff = models.IntegerField(null=True, blank=True, default=0)

    radio_grapher_permanent_staff = models.IntegerField(null=True, blank=True, default=0)
    radio_grapher_temperoray_staff = models.IntegerField(null=True, blank=True, default=0)
    radio_grapher_development_staff = models.IntegerField(null=True, blank=True, default=0)

    other_paramedics_permanent_staff = models.IntegerField(null=True, blank=True, default=0)
    other_paramedics_temperoray_staff = models.IntegerField(null=True, blank=True, default=0)
    other_paramedics_development_staff = models.IntegerField(null=True, blank=True, default=0)

    # Equipment_Info = models.ForeignKey(EquipmentInfo, on_delete=models.CASCADE, null=True, blank=True)

    icu_patients_admitted = models.IntegerField(null=True, blank=True, default=0)
    icu_patients_discharged = models.IntegerField(null=True, blank=True, default=0)
    icu_patients_deaths = models.IntegerField(null=True, blank=True, default=0)

    ventilator_patients_admitted = models.IntegerField(null=True, blank=True, default=0)
    ventilator_patients_discharged = models.IntegerField(null=True, blank=True, default=0)
    ventilator_patients_deaths = models.IntegerField(null=True, blank=True, default=0)

    hdu_patients_admitted = models.IntegerField(null=True, blank=True, default=0)
    hdu_patients_discharged = models.IntegerField(null=True, blank=True, default=0)
    hdu_patients_deaths = models.IntegerField(null=True, blank=True, default=0)

    hfnc_patients_admitted = models.IntegerField(null=True, blank=True, default=0)
    hfnc_patients_discharged = models.IntegerField(null=True, blank=True, default=0)
    hfnc_patients_deaths = models.IntegerField(null=True, blank=True, default=0)

    isolation_patients_admitted = models.IntegerField(null=True, blank=True, default=0)
    isolation_patients_discharged = models.IntegerField(null=True, blank=True, default=0)
    isolation_patients_deaths = models.IntegerField(null=True, blank=True, default=0)

    oxygen_supplied_patients_admitted = models.IntegerField(null=True, blank=True, default=0)
    oxygen_supplied_patients_discharged = models.IntegerField(null=True, blank=True, default=0)
    oxygen_supplied_patients_deaths = models.IntegerField(null=True, blank=True, default=0)

    # equipments after and before covid
    EQUIPMENTS = (
        ('ICU Machine', 'ICU Machine'),
        ('Ventilator Machine', 'Ventilator Machine'),
        ('Patient Monitor', 'Patient Monitor'),
        ('Infusion Pump', 'Infusion Pump'),
        ('Suction Pump', 'Suction Pump'),
        ('X-ray Machine', 'X-ray Machine'),
        ('Arterial Blood Gas (ABG) Machine', 'Arterial Blood Gas (ABG) Machine'),
        ('Defibrillator', 'Defibrillator'),
        ('BiPap Machine (bilevel positive airway pressure)', 'BiPap Machine (bilevel positive airway pressure)'),
        ('CPAP Machine (Continuous positive airway pressure', 'CPAP Machine (Continuous positive airway pressure'),
        ('High flow Nasal Cannula', 'High flow Nasal Cannula'),
        ('ECG Machine', 'ECG Machine'),
        ('Oxygen Concentrator', 'Oxygen Concentrator'),
        ('Autoclave Machine', 'Autoclave Machine'),
        ('BSC Level', 'BSC Level'),
        ('Automated Extraction', 'Automated Extraction'),
        ('PCR Machine', 'PCR Machine'),
    )
    equipments_name = models.CharField(max_length=255, choices=EQUIPMENTS, null=True, blank=True)
    equipments_before_covid = models.CharField(max_length=255, null=True, blank=True, default=0)
    equipments_after_covid = models.CharField(max_length=255, null=True, blank=True, default=0)
    operational = models.CharField(max_length=255, null=True, blank=True)
    total_biomedical_equipments = models.IntegerField(null=True, blank=True)
    total_patients_admitted = models.IntegerField(null=True, blank=True)
    equipment_emergency_for_patients = models.CharField(max_length=255, choices=patient_emergency_count, null=True,
                                                        blank=True)
    must_used_equipments = models.CharField(max_length=255, null=True, blank=True)
    yearly_expenditure_spent_for_equipments = models.CharField(max_length=255, choices=expenditure, null=True,
                                                               blank=True)
    calibrate_biomedical_equipment = models.CharField(max_length=255, choices=RAM, null=True, blank=True)
    biomedical_calibrate_from_others = models.CharField(max_length=400, null=True, blank=True)
    are_hospital_repair_equipments = models.CharField(max_length=255, choices=option, null=True, blank=True)
    aware_about_calibration_of_biomedical_equipment = models.CharField(max_length=255, choices=option, null=True,
                                                                       blank=True)
    repair_and_maintenance = models.CharField(max_length=255, choices=RAM, null=True, blank=True)
    repaired_by = models.CharField(max_length=255, choices=REPAIRE, null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    edited_date = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.name


class Equipment(models.Model):
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    equipment_type = models.CharField(max_length=255)
    unit = models.IntegerField(null=True, blank=True)
    model_number = models.CharField(max_length=255, null=True, blank=True)
    company_name = models.CharField(max_length=255, null=True, blank=True)
    suppliers = models.CharField(max_length=255, null=True, blank=True)
    remarks = models.CharField(max_length=255, null=True, blank=True)
    equipment_type_np = models.CharField(max_length=255, null=True, blank=True)
    unit_np = models.IntegerField(null=True, blank=True)
    model_number_np = models.CharField(max_length=255, null=True, blank=True)
    company_name_np = models.CharField(max_length=255, null=True, blank=True)
    suppliers_np = models.CharField(max_length=255, null=True, blank=True)
    remarks_np = models.CharField(max_length=255, null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    edited_date = models.DateTimeField(auto_now=True)
    operational = models.IntegerField(null=True, blank=True, default=0)
    not_operational = models.IntegerField(null=True, blank=True, default=0)
    in_maintenance = models.IntegerField(null=True, blank=True, default=0)
    total_equipments = models.IntegerField(null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.equipment_type

    def __str__(self):
        return self.equipment_type


class Resource(models.Model):
    category_type = (
        ('AN', 'announcement'),
        ('NE', 'news'),
        ('VI', 'videos'),
        ('AR', 'articals'),
    )
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    category = models.CharField(max_length=2, choices=category_type, null=True, blank=True)
    content = HTMLField(default="<p>Hello world</p>")
    video_link = models.CharField(max_length=1024, null=True, blank=True)
    slug = models.CharField(max_length=1024, null=True, blank=True)
    image = models.ImageField(default='default.jpg', upload_to=upload_resources_image, max_length=1024, null=True,
                              blank=True)
    summary = models.CharField(max_length=255, null=True, blank=True)
    title_np = models.CharField(max_length=255, null=True, blank=True)
    content_np = HTMLField(default="<p>विवरण</p>")
    slug_np = models.CharField(max_length=1024, null=True, blank=True)
    summary_np = models.CharField(max_length=255, null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    edited_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Achievement(models.Model):
    title = models.CharField(max_length=255)
    number = models.IntegerField()
    title_np = models.CharField(max_length=255, null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    edited_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Solve(models.Model):
    request_from = models.CharField(max_length=1024)
    request_for = models.CharField(max_length=1024)
    support_provided = models.CharField(max_length=1024)
    details = models.CharField(max_length=1024)
    request_from_np = models.CharField(max_length=1024, null=True, blank=True)
    request_for_np = models.CharField(max_length=1024, null=True, blank=True)
    support_provided_np = models.CharField(max_length=1024, null=True, blank=True)
    details_np = models.CharField(max_length=1024, null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    edited_date = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to=upload_solve_files, null=True, blank=True)
    document = models.CharField(max_length=1024, null=True, blank=True)


class Discussion(models.Model):
    topic = models.CharField(max_length=255)
    description = HTMLField(default="<p>write your questions</p>")
    thumbnail = models.ImageField(
        _("Thumbnail"), upload_to="thumbnail", blank=True, null=True
    )
    slug = models.SlugField(_("Slug"), blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    edited_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.topic

    def get_absolute_url(self):
        """Absolute URL for Post"""
        return reverse("post_detail", kwargs={"slug": self.slug})

    def get_update_url(self):
        """Update URL for Post"""
        return reverse("post_update", kwargs={"slug": self.slug})

    def get_delete_url(self):
        """Delete URL for Post"""
        return reverse("post_delete", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):
        self.slug = slugify(self.topic)
        super().save(*args, **kwargs)
        if self.thumbnail:
            img = Image.open(default_storage.open(self.thumbnail.name))
            if img.height > 1080 or img.width > 1920:  # pragma:no cover
                output_size = (1920, 1080)
                img.thumbnail(output_size)
                buffer = BytesIO()
                img.save(buffer, format="JPEG")
                default_storage.save(self.thumbnail.name, buffer)


class Choices(models.Model):
    question = models.ForeignKey(Discussion, on_delete=models.CASCADE)
    comment = HTMLField(default="<p>write your answer</p>", null=True, blank=True)
    vote = models.IntegerField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    edited_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.comment

    class Meta:
        verbose_name = "Comment and like"


class HelpRequest(models.Model):
    status = [
        ('solved', 'solved'),
        ('unsolved', 'unsolved')
    ]
    request = [
        ('OC', 'Oxygen Concentrator'),
        ('OV', 'Oxygen Ventilator'),
        ('OP', 'Oxygen Plant'),
        ('DM', 'Dialysis Machine'),
        ('other', 'Other')

    ]
    urgency_of_request = [
        ('Urgent', 'Urgent'),
        ('Moderate', 'Moderate'),
        ('NotUrgent', 'Not Urgent')
    ]
    organization = models.CharField(max_length=255, null=True, blank=True)
    province = models.ForeignKey(Province, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=255)
    contact = models.CharField(max_length=10)
    email = models.EmailField()
    urgency = models.CharField(max_length=255, choices=urgency_of_request)
    request_for = models.CharField(choices=request, max_length=255)
    our_supports_for_you = models.CharField(max_length=500, blank=True, null=True)
    time_duration = models.CharField(max_length=255, blank=True, null=True)
    anything = models.TextField(blank=True, null=True)
    request_status = models.CharField(max_length=255, choices=status, null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    edited_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class CommunityMember(models.Model):
    type = [
        ('Board of Director', 'Board of Director'),
        ('Technical team', 'Technical Team'),
        ('Advisory Committee', 'Advisory Committee'),
        ('Management Committee', 'Management Committee')
    ]
    community = models.CharField(choices=type, max_length=255, null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    position = models.CharField(max_length=255, null=True, blank=True)
    organization = models.CharField(max_length=255, null=True, blank=True)
    name_np = models.CharField(max_length=255, null=True, blank=True)
    position_np = models.CharField(max_length=255, null=True, blank=True)
    organization_np = models.CharField(max_length=255, null=True, blank=True)
    profile_pic = models.ImageField(upload_to=community_member_image, null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    edited_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class HitCount(models.Model):
    visits = models.IntegerField(default=0)


class Trainer(models.Model):
    age_group = [
        ('Below 19', 'Below 19'),
        ('20-29', '20-29'),
        ('30-39', '30-39'),
        ('40-49', '40-49'),
        ('50-59', '50-59'),
        ('Above 60', 'Above 60')
    ]
    ch = [
        ('yes', 'Yes'),
        ('No', 'No')
    ]
    name = models.CharField(max_length=255, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=255, null=True, blank=True)
    email = models.CharField(max_length=255, null=True, blank=True)
    ethnic = models.CharField(max_length=255, null=True, blank=True)
    education = models.CharField(max_length=255, null=True, blank=True)
    associated_organization_or_clinic = models.CharField(max_length=255, null=True, blank=True)
    area_of_expertise = models.CharField(max_length=255, null=True, blank=True)
    experience = models.CharField(max_length=255, null=True, blank=True)
    ege_group = models.CharField(max_length=100, choices=age_group, null=True, blank=True)
    province = models.ForeignKey('Province', related_name='trainer',
                                 on_delete=models.CASCADE, blank=True, null=True)
    district = models.ForeignKey('District', related_name='trainer',
                                 on_delete=models.CASCADE, blank=True, null=True)
    municipality = models.ForeignKey('Municipality', related_name='trainer',
                                     on_delete=models.CASCADE, blank=True, null=True)
    ward = models.ForeignKey('Ward', related_name='trainer',
                             on_delete=models.CASCADE, blank=True, null=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    logitude = models.FloatField(null=True, blank=True)
    profile = models.ImageField(upload_to=trainer_profile, null=True, blank=True, default = '/profile.png')
    certification_from_mot = models.CharField(max_length=50, choices=ch, null=True, blank=True)
    document = models.FileField(upload_to=trainer_document, null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    edited_date = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name

    @property
    def image(self):
        try:
            url = self.profile.url
        except:
            url = ''
        return url

    @property
    def documentf(self):
        try:
            url = self.document.url
        except:
            url = ''
        return url

class Trainee(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=255, null=True, blank=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    edited_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Skills(models.Model):
    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE)
    skill = models.CharField(max_length=255)
    skill_percentage = models.IntegerField(null=True, blank=True)


class Trainings(models.Model):
    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255, null=True, blank=True)
    time = models.DateTimeField(null=True, blank=True)
    lalitude = models.DecimalField(max_digits=22, decimal_places=16, blank=True, null=True)
    logitude = models.DecimalField(max_digits=22, decimal_places=16, blank=True, null=True)

    def __str__(self):
        return self.name
