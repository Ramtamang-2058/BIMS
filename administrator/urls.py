from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.dashboard, name="adminDashboard"),
    # * Hospital
    path('hospitals', views.voters, name="adminViewHospital"),
    path('add/hospitals', views.addHospital, name="addHospital"),
    path('hospital/view/<int:pk>', views.viewHospital, name="viewHospital"),
    path('hospital/delete/<int:pk>', views.deleteHospital, name='deleteHospital'),
    path('voters/update', views.updateVoter, name="updateVoter"),
    path('hospital/update/<str:id>/', views.hospitalUpdate, name='hospital'),

    # users
    path('view/users/add', views.add_user, name='addUser'),
    path('view/users/all', views.view_users, name='view_users'),
    path('view/users/delete/<int:pk>/', views.delete_user, name='deleteUser'),
    path('view/users/update/<int:pk>/', views.update_user, name='updateUser'),

    # hospital chart
    path('population-chart/<int:pk>', views.hospital_staff_chart, name='population-chart'),

    # * Equipment
    path('equipment/add', views.add_equipment, name="addEquipment"),
    path('equipment/view/<int:pk>/', views.view_equipment, name="viewEquipment"),
    path('equipment/update/<int:pk>/', views.updateEquipment, name="updateEquipment"),
    path('equipment/delete/<int:pk>/', views.deleteEquipment, name='deleteEquipment'),
    path('equipments', views.viewEquipments, name='viewEquipments'),


    # * bar graph
    path('barchart', views.barchart, name='barchart'),

    # * request
    path('request/all', views.view_all_request, name='requests'),
    path('request/update/<int:pk>/', views.update_request, name='request_update'),

    # trainer
   
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
