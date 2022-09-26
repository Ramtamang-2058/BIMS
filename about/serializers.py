from rest_framework import serializers
from .models import Team, Organization, Hospital, Equipment, Resource, Achievement, Solve, Discussion, Choices, \
    HelpRequest, CommunityMember, HitCount
from django.db.models import Sum, Count


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = [
            'id',
            'member_type',
            'email',
            'province',
            'profile_picture',
            'full_name',
            'position',
            'primary_contact',
            'secondary_contact',
            'qualifications',
            'description',
            'lead_type',
            'resume',
            'is_approved',
            'latitude',
            'longitude',
            'created_date',
            'edited_date',
        ]


class PostTeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = [
            'id',
            'province',
            'email',
            'profile_picture',
            'full_name',
            'position',
            'primary_contact',
            'secondary_contact',
            'qualifications',
            'description',
            'resume',
        ]


class GetOrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = [
            'id',
            'title',
            'logo',
            'description',
            'category',
            'contact_number',
            'contact_email',
            'contact_website',
            'contact_social_media',
            'created_date',
            'edited_date',
        ]


class GetOrganizationNepaliSerializer(serializers.ModelSerializer):
    title = serializers.CharField(source='title_np')
    description = serializers.CharField(source='description_np')
    contact_number = serializers.CharField(source='contact_number_np')

    class Meta:
        model = Organization
        fields = [
            'id',
            'title',
            'logo',
            'description',
            'category',
            'contact_number',
            'contact_email',
            'contact_website',
            'contact_social_media',
            'created_date',
            'edited_date',
        ]


class TeamNepaliSerializer(serializers.ModelSerializer):
    province = serializers.CharField(source='province_np')
    full_name = serializers.CharField(source='full_name_np')
    position = serializers.CharField(source='position_np')
    primary_contact = serializers.CharField(source='primary_contact_np')
    secondary_contact = serializers.CharField(source='secondary_contact_np')
    qualifications = serializers.CharField(source='qualifications_np')
    description = serializers.CharField(source='description_np')

    class Meta:
        model = Team
        fields = [
            'id',
            'member_type',
            'email',
            'province',
            'profile_picture',
            'full_name',
            'position',
            'primary_contact',
            'secondary_contact',
            'qualifications',
            'description',
            'resume',
            'is_approved',
            'latitude',
            'longitude',
            'created_date',
            'edited_date',
        ]


class EquipmentEnglishSerializer(serializers.ModelSerializer):
    hospital_info = serializers.SerializerMethodField('get_hospital_name')
    oxygencylinder = serializers.SerializerMethodField()
    oxygenconcerntrator = serializers.SerializerMethodField()
    dialyzer = serializers.SerializerMethodField()
    ventrilator = serializers.SerializerMethodField()

    class Meta:
        model = Equipment
        fields = [
            'id',
            'hospital',
            'equipment_type',
            'unit',
            'model_number',
            'company_name',
            'suppliers',
            'remarks',
            'created_date',
            'edited_date',
            'hospital_info',
            'oxygencylinder',
            'oxygenconcerntrator',
            'dialyzer',
            'ventrilator',
            'created_by',
        ]

    def get_hospital_name(self, equipment):
        request = self.context.get('request')
        data = {
            'hospital_id': equipment.hospital.id,
            'hospital_name': equipment.hospital.name,

        }
        return data

    def get_oxygencylinder(self, obj):
        total_oxygencylinder = Equipment.objects.filter(equipment_type='Oxygen Cylinder and Regulator').aggregate(
            total_oxygencylinder=Sum('unit'))
        return total_oxygencylinder["total_oxygencylinder"]

    def get_oxygenconcerntrator(self, obj):
        total_oxygenconcerntrator = Equipment.objects.filter(equipment_type='Oxygen Concentrator').aggregate(
            total_oxygenconcerntrator=Sum('unit'))
        return total_oxygenconcerntrator["total_oxygenconcerntrator"]

    def get_dialyzer(self, obj):
        total_dialyzer = Equipment.objects.filter(equipment_type='Dialyzer').aggregate(total_dialyzer=Sum('unit'))
        return total_dialyzer["total_dialyzer"]

    def get_ventrilator(self, obj):
        total_ventrilator = Equipment.objects.filter(equipment_type='Ventilator').aggregate(
            total_ventrilator=Sum('unit'))
        return total_ventrilator["total_ventrilator"]


class EquipmentNepaliSerializer(serializers.ModelSerializer):
    hospital_info = serializers.SerializerMethodField('get_hospital_name')

    equipment_type = serializers.CharField(source='equipment_type_np')
    unit = serializers.CharField(source='unit_np')
    company_name = serializers.CharField(source='company_name_np')
    suppliers = serializers.CharField(source='suppliers_np')
    remarks = serializers.CharField(source='remarks_np')
    model_number = serializers.CharField(source='model_number_np')
    oxygencylinder = serializers.SerializerMethodField()
    oxygenconcerntrator = serializers.SerializerMethodField()
    dialyzer = serializers.SerializerMethodField()
    ventrilator = serializers.SerializerMethodField()

    class Meta:
        model = Equipment
        fields = [
            'id',
            'hospital',
            'equipment_type',
            'unit',
            'model_number',
            'company_name',
            'suppliers',
            'remarks',
            'latitude',
            'longitude',
            'created_date',
            'edited_date',
            'hospital_info',
            'oxygencylinder',
            'oxygenconcerntrator',
            'dialyzer',
            'ventrilator',
            'created_by',
        ]

    def get_hospital_name(self, equipment):
        request = self.context.get('request')
        data = {
            'hospital_id': equipment.hospital.id,
            'hospital_name': equipment.hospital.name,

        }
        return data

    def get_oxygencylinder(self, obj):
        total_oxygencylinder = Equipment.objects.filter(equipment_type='Oxygen Cylinder and Regulator').aggregate(
            total_oxygencylinder=Sum('unit'))
        return total_oxygencylinder["total_oxygencylinder"]

    def get_oxygenconcerntrator(self, obj):
        total_oxygenconcerntrator = Equipment.objects.filter(equipment_type='Oxygen Concentrator').aggregate(
            total_oxygenconcerntrator=Sum('unit'))
        return total_oxygenconcerntrator["total_oxygenconcerntrator"]

    def get_dialyzer(self, obj):
        total_dialyzer = Equipment.objects.filter(equipment_type='Dialyzer').aggregate(total_dialyzer=Sum('unit'))
        return total_dialyzer["total_dialyzer"]

    def get_ventrilator(self, obj):
        total_ventrilator = Equipment.objects.filter(equipment_type='Ventilator').aggregate(
            total_ventrilator=Sum('unit'))
        return total_ventrilator["total_ventrilator"]


class HospitalEnglishSerializer(serializers.ModelSerializer):
    equipments = EquipmentEnglishSerializer(many=True, read_only=True)

    class Meta:
        model = Hospital
        fields = [
            'id',
            'name',
            'contact_number',
            'contact_email',
            'province',
            'district',
            'municipality',
            'ward',
            'address',
            'equipments',
            'latitude',
            'longitude',
            'created_date',
            'edited_date',
            'objects'
            'created_by',
        ]


class HospitalNepaliSerializer(serializers.ModelSerializer):
    equipments_np = EquipmentNepaliSerializer(many=True, read_only=True)
    # name = serializers.CharField(source='name_np')
    # contact_number = serializers.CharField(source='contact_number_np')
    # contact_email = serializers.CharField(source='contact_email_np')
    province = serializers.SerializerMethodField()
    # address = serializers.CharField(source='address_np')
    ward = serializers.SerializerMethodField()
    municipality = serializers.SerializerMethodField()
    district = serializers.SerializerMethodField()

    class Meta:
        model = Hospital
        fields = [
            'id',
            'name',
            'contact_number',
            'contact_email',
            'province',
            'district',
            'municipality',
            'ward',
            'address',
            'equipments_np',
            'latitude',
            'longitude',
            'created_date',
            'edited_date',
            'created_by',
        ]

    def get_district(self, obj):
        if obj.district:
            return obj.district.name
        return None

    def get_municipality(self, obj):
        if obj.municipality:
            return obj.municipality.name
        return None

    def get_ward(self, obj):
        if obj.ward:
            return obj.ward.name
        return None

    def get_province(self, obj):
        if obj.province:
            return obj.province.name
        return None

#
# class HospitalInfoEnglishSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = HospitalInfo
#         fields = [
#             'id',
#             'hospital',
#             'total_beds_no',
#             'total_staff',
#             'total_biomedical_equipments',
#             'total_patients_admitted',
#             'equipment_emergency_for_patients',
#             'must_used_equipments',
#             'yearly_expenditure_spent_for_equipments',
#             'calibrate_biomedical_equipment',
#             'are_hospital_repair_equipments',
#             'aware_about_calibration_of_biomedical_equipment',
#             'repair_and_maintenance',
#             'repaired_by',
#             'created_date',
#             'edited_date',
#         ]


class ResourceEnglishSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = [
            'id',
            'author',
            'title',
            'category',
            'category',
            'content',
            'video_link',
            'slug',
            'image',
            'summary',
            'created_date',
            'edited_date'
        ]


class ResourceNepaliSerializer(serializers.ModelSerializer):
    title = serializers.CharField(source='title_np')
    content = serializers.CharField(source='content_np')
    slug = serializers.CharField(source='slug_np')
    summary = serializers.CharField(source='summary_np')

    class Meta:
        model = Resource
        fields = [
            'id',
            'author',
            'title',
            'category',
            'content',
            'video_link',
            'slug',
            'image',
            'summary',
            'created_date',
            'edited_date'
        ]


class AchievementEnglishSerializer(serializers.ModelSerializer):
    snumber = serializers.SerializerMethodField()

    class Meta:
        model = Achievement
        fields = [
            'id',
            'title',
            'number',
            'created_date',
            'snumber',
        ]

    def get_snumber(self, obj):
        total_solve = Solve.objects.all().aggregate(total_solve=Count('id'))
        return total_solve["total_solve"]


class AchievementNepaliSerializer(serializers.ModelSerializer):
    title = serializers.CharField(source='title_np')
    snumber = serializers.SerializerMethodField()

    class Meta:
        model = Achievement
        fields = [
            'id',
            'title',
            'number',
            'snumber',
            'created_date'''

        ]

    def get_snumber(self, obj):
        total_solve = Solve.objects.all().aggregate(total_solve=Count('id'))
        return total_solve["total_solve"]


class SolveEnglishSerializer(serializers.ModelSerializer):
    number = serializers.SerializerMethodField()

    class Meta:
        model = Solve
        fields = [
            'id',
            'request_from',
            'request_for',
            'support_provided',
            'created_date',
            'edited_date',
            'image',
            'document',
            'number',

        ]

    def get_number(self, obj):
        total_solve = Solve.objects.all().aggregate(total_solve=Count('id'))
        return total_solve["total_solve"]


class SolveNepaliSerializer(serializers.ModelSerializer):
    request_from = serializers.CharField(source='request_from_np')
    request_for = serializers.CharField(source='request_for_np')
    support_provided = serializers.CharField(source='support_provided_np')
    details = serializers.CharField(source='details_np')

    class Meta:
        model = Solve
        fields = [
            'id',
            'request_from',
            'request_for',
            'support_provided',
            'created_date',
            'edited_date',
            'image',
            'document',
            'details',

        ]


class DiscussionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discussion
        fields = [
            'id',
            'topic',
            'description',
            'thumbnail',
            'slug',
            'created_date',
            'edited_date',
        ]


class CommentAndVoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choices
        fields = [
            'id',
            'question',
            'comment',
            'vote',
            'created_date',
            'edited_date',
        ]


class HelpRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = HelpRequest
        fields = [
            'id',
            'organization',
            'province',
            'name',
            'contact',
            'email',
            'urgency',
            'request_for',
            'our_supports_for_you',
            'time_duration',
            'anything',
            'request_status',
            'created_date',
            'edited_date'
        ]


class CommunityMemberEnglishSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommunityMember
        fields = [
            'id',
            'community',
            'name',
            'position',
            'profile_pic',
            'organization',
            'created_date',
            'edited_date'
        ]


class CommunityMemberNepaliSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='name_np')
    position = serializers.CharField(source='position_np')
    organization = serializers.CharField(source='organization_np')

    class Meta:
        model = CommunityMember
        fields = [
            'id',
            'community',
            'name',
            'position',
            'profile_pic',
            'organization',
            'created_date',
            'edited_date'
        ]


class HitCountSerializer(serializers.ModelSerializer):
    class Meta:
        model = HitCount
        fields = ('visits',)

