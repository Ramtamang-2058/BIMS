from django.urls import path
from hospital_admin import views

urlpatterns = [
    path('', views.account_login, name="account_login"),
    path('logout/', views.account_logout, name="account_logout"),

    # registration
    path('register/trainer', views.trainer_register, name="trainer_register"),
    path('register/hospital', views.hospital_register, name="hospital_register"),
    path('register/dir/', views.formdir, name="form_dir"),
    path('register/myhospital', views.hospital_user, name='hospital_user'),
    # path('trainer/register', views.trainer_form, name="trainerForm"),
    
    # * Hospital
    path('admin/hospital/view/', views.viewHospital, name="hospitalDetailView"),
    path('admin/hospital/update/', views.hospitalUpdate, name='adminHospitalUpdate'),

    # hospital chart
    path('population-chart/<int:pk>', views.hospital_staff_chart, name='population-chart'),

    # * Equipment
    path('equipment/add', views.add_equipment, name="addEquipmentHospital"),
    path('equipment/view/<int:pk>/', views.view_equipment, name="viewEquipmentHospital"),
    path('equipment/update/<int:pk>/', views.updateEquipment, name="updateEquipmentHospital"),
    path('equipment/delete/<int:pk>/', views.deleteEquipment, name='deleteEquipmentHospital'),
    path('equipments', views.viewEquipments, name='viewEquipmentsHospital'),

    # * request
    path('request/all', views.view_all_request, name='requestsHospital'),
    path('request/update/<int:pk>/', views.update_request, name='request_updateHospital'),

    path('hospital/trainer', views.view_trainer, name='trainer'),
    path('hospital/trainer/profile/<int:pk>', views.view_trainer_detail, name='trainerProfile'),
    path('map', views.map, name='map'),
    path('hospital/trainer/location/<int:pk>', views.trainer_location, name='trainer-location'),



]
