from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Team, Organization, Hospital, Equipment, Resource, Achievement, Province, District, Municipality, \
    Ward, Solve, Discussion, Choices, HelpRequest, CommunityMember, Trainer, Trainee, Skills, Trainings


class TeamAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('full_name', 'province', 'member_type', 'position', 'primary_contact', 'is_approved')
    search_fields = ('full_name', 'province', 'member_type', 'is_approved', 'position')
    readonly_fields = ('created_date', 'edited_date')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
    ordering = ('created_date',)


class OrganizationAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('title', 'contact_number', 'contact_email', 'contact_website', 'created_date')
    search_fields = ('title', 'contact_website', 'contact_email', 'contact_number')
    readonly_fields = ('created_date', 'edited_date')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
    ordering = ('created_date',)


class HospitalAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = (
        'name', 'contact_number', 'contact_email', 'province', 'district', 'municipality', 'ward', 'address',
        'created_date')
    search_fields = ('name', 'province__id', 'address', 'contact_number')
    readonly_fields = ('created_date', 'edited_date')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
    ordering = ('created_date',)


class EquipmentAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = (
        'hospital', 'equipment_type', 'operational', 'not_operational', 'in_maintenance', 'total_equipments',
        'model_number', 'unit', 'company_name', 'created_date')
    search_fields = ('suppliers', 'remarks', 'hospital', 'equipment_type', 'model_number')
    readonly_fields = ('created_date', 'edited_date')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
    ordering = ('created_date',)


class HospitalInfoAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'hospital', 'total_beds_no', 'total_staff', 'total_biomedical_equipments',
                    'total_patients_admitted', 'equipment_emergency_for_patients', 'must_used_equipments',
                    'yearly_expenditure_spent_for_equipments', 'calibrate_biomedical_equipment',
                    'are_hospital_repair_equipments', 'aware_about_calibration_of_biomedical_equipment',
                    'repair_and_maintenance', 'repaired_by', 'created_date', 'edited_date',)


class ResourcesAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('author', 'title', 'category', 'created_date')
    search_fields = ('author', 'title', 'category')
    readonly_fields = ('created_date', 'edited_date')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
    ordering = ('created_date',)


class AchievementAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('title', 'number')
    search_fields = ('title',)
    readonly_fields = ('created_date', 'edited_date')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
    ordering = ('created_date',)


class ProvinceAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
    ordering = ('name',)


class DistrictAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('name', 'province')
    search_fields = ('name', 'province')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
    ordering = ('name',)


class MunicipalityAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('name', 'province', 'district')
    search_fields = ('name', 'province', 'district')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
    ordering = ('name',)


class WardAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('name', 'province', 'district', 'municipality')
    search_fields = ('name', 'province', 'district', 'municipality')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
    ordering = ('name',)


class SolveAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('request_from', 'request_for', 'created_date', 'edited_date')
    search_fields = ('request_from', 'request_for')
    readonly_fields = ('created_date', 'edited_date')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
    ordering = ('created_date',)


class DiscussionAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('topic', 'description', 'thumbnail', 'slug', 'created_date', 'edited_date')
    search_fields = ('topic', 'description', 'thumbnail', 'slug', 'created_date', 'edited_date')
    readonly_fields = ('created_date', 'edited_date')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
    ordering = ('created_date',)


class CommentAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('question', 'comment', 'vote', 'created_date', 'edited_date')
    search_fields = ('question', 'comment', 'vote', 'created_date', 'edited_date')
    readonly_fields = ('created_date', 'edited_date')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
    ordering = ('created_date',)


class HelpRequestAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display= ('organization', 'urgency', 'province', 'name', 'contact', 'email', 'request_for', 'request_status',
                   'our_supports_for_you',
                   'time_duration', 'anything', 'created_date', 'edited_date')
    search_fields = ('organization', 'province', 'name', 'contact', 'email', 'request_for', 'our_supports_for_you',
                     'time_duration', 'anything', 'created_date', 'edited_date')
    readonly_fields = ('created_date', 'edited_date')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
    ordering = ('created_date',)


class CommunityMemberAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display= ('community', 'name', 'position', 'organization', 'created_date', 'edited_date')
    search_fields = ('community', 'name', 'position', 'organization', 'created_date', 'edited_date')
    readonly_fields = ('created_date', 'edited_date')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
    ordering = ('created_date',)


class TrainerAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('name', 'phone', 'email', 'address', 'area_of_expertise')
    search_fields = ('name', 'phone', 'email', 'address', 'area_of_expertise')
    readonly_fields = ('created_date', 'edited_date')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
    ordering = ('created_date',)


class TraineeAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('name', 'phone', 'email', 'address')
    search_fields = ('name', 'phone', 'email', 'address')
    readonly_fields = ('created_date', 'edited_date')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
    ordering = ('created_date',)


class SkillsAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('skill', 'skill_percentage')


admin.site.register(Team, TeamAdmin)
admin.site.register(Organization, OrganizationAdmin)
admin.site.register(Hospital, HospitalAdmin)
admin.site.register(Equipment, EquipmentAdmin)
admin.site.register(Resource, ResourcesAdmin)
admin.site.register(Achievement, AchievementAdmin)
admin.site.register(Province, ProvinceAdmin)
admin.site.register(District, DistrictAdmin)
admin.site.register(Municipality, MunicipalityAdmin)
admin.site.register(Ward, WardAdmin)
admin.site.register(Solve, SolveAdmin)
admin.site.register(Discussion, DiscussionAdmin)
admin.site.register(Choices, CommentAdmin)
admin.site.register(HelpRequest, HelpRequestAdmin)
admin.site.register(CommunityMember, CommunityMemberAdmin)
admin.site.register(Trainer, TrainerAdmin)
admin.site.register(Trainee, TraineeAdmin)
admin.site.register(Skills, SkillsAdmin)
admin.site.register(Trainings)