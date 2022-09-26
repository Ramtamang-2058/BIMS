from django.shortcuts import render, reverse, redirect, get_object_or_404
from authentication.models import User
from django.db.models import Sum, Avg, Min, Count, F, Q
import matplotlib
from matplotlib import pyplot as plt
import numpy as np
from hospital_admin.forms import *
from about.models import *
from django.contrib import messages
from authentication.forms import CustomUserForm
from django.http import JsonResponse, HttpResponse
from django.conf import settings
from json import dumps

matplotlib.use('Agg')


def dashboard(request):
    equipments = Equipment.objects.aggregate(equipments=Sum('unit'))
    icubeds = Hospital.objects.aggregate(icubeds=Sum('icu_beds'))
    hdubeds = Hospital.objects.aggregate(hdubeds=Sum('hdu_beds'))
    hfnbeds = Hospital.objects.aggregate(hnfbeds=Sum('hfnc_beds'))
    isolationbeds = Hospital.objects.aggregate(isolationbeds=Sum('isolation_beds'))
    oxygensuplybeds = Hospital.objects.aggregate(oxygensuppiedbeds=Sum('oxygen_supplied_beds'))
    beds = sum(icubeds.values()) + sum(hdubeds.values()) + sum(hfnbeds.values()) + sum(isolationbeds.values()) + sum(
        oxygensuplybeds.values())
    hospitals = Hospital.objects.all()
    list_of_candidates = []
    votes_count = []
    chart_data = {}
    context = {
        'equipments': equipments,
        'hospitals_count': hospitals.count(),
        'beds': beds,
        'chart_data': chart_data,
        'page_title': "Dashboard"
    }
    return render(request, "admin/home.html", context)


def barchart(request):
    objects = ['ICU', 'DHU', 'HFNC', 'ISOLATION', 'OXYGEN SUPPLY', '']
    y_pos = np.arange(len(objects))
    icubeds = Hospital.objects.aggregate(icubeds=Sum('icu_beds'))
    hdubeds = Hospital.objects.aggregate(hdubeds=Sum('hdu_beds'))
    hfnbeds = Hospital.objects.aggregate(hnfbeds=Sum('hfnc_beds'))
    isolationbeds = Hospital.objects.aggregate(isolationbeds=Sum('isolation_beds'))
    oxygensuplybeds = Hospital.objects.aggregate(oxygensuppiedbeds=Sum('oxygen_supplied_beds'))
    icu = list(icubeds.values())
    hfn = list(hfnbeds.values())
    hdu = list(hdubeds.values())
    oxygensuply = list(oxygensuplybeds.values())
    isolation = list(isolationbeds.values())

    qty = [icu, hfn, hdu, isolation, oxygensuply, 0]
    plt.bar(y_pos, qty, align='center', alpha=0.5)
    plt.xticks(y_pos, objects)
    plt.ylabel('Unit')
    plt.title('Hospital Beds')
    plt.savefig('media/barchart.png')
    return render(request, 'admin/home.html')


def voters(request):
    hospitals = Hospital.objects.all()
    # userForm = CustomUserForm(request.POST or None)
    hospitalForm = HospitalForm(request.POST or None)
    context = {
        # 'form1': userForm,
        'form2': hospitalForm,
        'hospitals': hospitals,
        'page_title': 'Hospital List'
    }
    if request.method == 'POST':
        if hospitalForm.is_valid():
            # user = userForm.save(commit=False)
            hospital = hospitalForm.save(commit=False)
            # hospital.admin = user
            # user.save()
            hospital.save()
            messages.success(request, "New hospital created")
        else:
            messages.error(request, "Form validation failed")
    return render(request, "admin/voters.html", context)


def addHospital(request):
    hospitals = Hospital.objects.all()
    # userForm = CustomUserForm(request.POST or None)
    hospitalForm = HospitalForm(request.POST or None)
    context = {
        # 'form1': userForm,
        'form': hospitalForm,
        'hospitals': hospitals,
        'page_title': 'Hospital'
    }
    if request.method == 'POST':
        if hospitalForm.is_valid():
            # user = userForm.save(commit=False)
            hospital = hospitalForm.save(commit=False)
            # hospital.admin = user
            # user.save()
            hospital.save()
            messages.success(request, "New hospital created")
        else:
            messages.error(request, "Form validation failed")
    return render(request, "admin/add_hospital.html", context)


def add_user(request):
    if request.method == 'POST':
        form = CustomUserForm.save(commit=False)
        form.save()
        return redirect('view_users')
    else:
        form = CustomUserForm
    return render(request, 'admin/reg.html', {'form': form})


def view_users(request):
    users = User.objects.all()
    context = {

        'users': users}
    return render(request,
                  'admin/view_users.html', context)


def update_user(request, pk):
    user = User.objects.get(id=pk)
    if request.method == 'POST':
        form = CustomUserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            # redirect to the detail page of the `Band` we just updated
            return redirect('adminViewHospital')
    else:
        form = CustomUserForm(instance=user)

    return render(request,
                  'admin/update_user.html',
                  {'form': form})


def delete_user(request, pk):
    user = User.objects.get(id=pk)
    user.delete()
    messages.success(request, "User has been deleted")
    return redirect(reverse('view_users'))


def viewHospital(request, pk):
    hospital = Hospital.objects.get(id=pk)
    equipments = Equipment.objects.filter(hospital=pk)
    icubeds = hospital.icu_beds
    hdubeds = hospital.hdu_beds
    hfnbeds = hospital.hfnc_beds
    isolationbeds = hospital.isolation_beds
    oxygensuplybeds = hospital.oxygen_supplied_beds
    beds_total = icubeds + hdubeds + hfnbeds + isolationbeds + oxygensuplybeds
    if beds_total == 0:
        beds = 1
    else:
        beds = beds_total
    icu_percentage = ((icubeds / beds) * 100)
    hdu_percentage = ((hdubeds / beds) * 100)
    hfn_percentage = ((hfnbeds / beds) * 100)
    isolation_percentage = ((isolationbeds / beds) * 100)
    oxygen_supply_percentage = ((oxygensuplybeds / beds) * 100)
    hospitals = Hospital.objects.all()
    p1 = hospital.biomedical_engineer_permanent_staff
    p2 = hospital.doctor_permanents_staff
    p3 = hospital.nurse_permanent_staff
    p4 = hospital.lab_technician_permanent_staff
    p5 = hospital.health_assistant_permanent_staff
    p6 = hospital.biomedical_technician_permanent_staff
    p7 = hospital.pharmacist_permanent_staff
    p8 = hospital.radio_grapher_permanent_staff
    p9 = hospital.other_paramedics_permanent_staff
    pt = p1 + p2 + p3 + p4 + p5 + p6 + p7 + p8 + p9
    if pt == 0:
        permanent_total = 1
    else:
        permanent_total = pt
    # temporary staff
    t1 = hospital.biomedical_engineer_temperoray_staff
    t2 = hospital.doctor_temperoray_staff
    t3 = hospital.nurse_temperoray_staff
    t4 = hospital.lab_technician_temperoray_staff
    t5 = hospital.health_assistant_temperoray_staff
    t6 = hospital.biomedical_technician_temperoray_staff
    t7 = hospital.pharmacist_temperoray_staff
    t8 = hospital.radio_grapher_temperoray_staff
    t9 = hospital.other_paramedics_temperoray_staff
    tt = t1 + t2 + t3 + t4 + t5 + t5 + t6 + t7 + t8 + t9
    if tt == 0:
        temporary_total = 1;
    else:
        temporary_total = tt
    # development staff
    d1 = hospital.biomedical_engineer_development_staff
    d2 = hospital.doctor_development_staff
    d3 = hospital.nurse_development_staff
    d4 = hospital.lab_technician_development_staff
    d5 = hospital.health_assistant_temperoray_staff
    d6 = hospital.biomedical_technician_development_staff
    d7 = hospital.pharmacist_development_staff
    d8 = hospital.radio_grapher_development_staff
    d9 = hospital.other_paramedics_development_staff
    dt = d1 + d2 + d3 + d4 + d5 + d6 + d7 + d8 + d9
    if dt == 0:
        development_total = 1
    else:
        development_total = dt
    biomedical_engineer_total = p1 + t1 + d1
    doctor_total = p2 + t2 + d2
    nurse_total = p3 + t3 + d3
    lab_technician_total = p4 + t4 + d4
    health_assistant_total = p5 + t5 + d5
    biomedical_technician_total = p6 + t6 + d6
    pharmacist_total = p7 + t7 + d7
    radio_grapher_total = p8 + t8 + d8
    other_paramedics_total = p9 + t9 + d9
    total = pt + tt + dt
    data = [icubeds, hdubeds, hfnbeds, isolationbeds, oxygensuplybeds]  # data4 hospital beds data for pi chart
    labels = ["ICU BEDS", "HDU BEDS", "HFN BEDS", "ISOLATION BEDS", "OXYGEN SUPPLY BEDS"]
    context = {'hospital': hospital,
               'hospitals': hospitals,
               'equipments': equipments.count(),
               'equipments_detail': equipments,
               'hospitals_count': hospitals.count(),
               'beds': beds,
               'beds_total': beds_total,
               'icu_percentage': icu_percentage,
               'hdu_percentage': hdu_percentage,
               'hfn_percentage': hfn_percentage,
               'isolation_percentage': isolation_percentage,
               'oxygen_supply_percentage': oxygen_supply_percentage,
               'pt': pt,
               'dt': dt,
               'tt': tt,
               'permanent_total': permanent_total,
               'temporary_total': temporary_total,
               'development_total': development_total,
               'biomedical_engineer_total': biomedical_engineer_total,
               'doctor_total': doctor_total,
               'nurse_total': nurse_total,
               'radio_grapher_total': radio_grapher_total,
               'lab_technician_total': lab_technician_total,
               'health_assistant_total': health_assistant_total,
               'biomedical_technician_total': biomedical_technician_total,
               'pharmacist_total': pharmacist_total,
               'other_paramedics_total': other_paramedics_total,
               'total': total,
               'labels': labels,
               'data': data,
               }
    return render(request, 'admin/hospital_detail_view.html', context)


def hospital_staff_chart(request, pk):
    hospital = Hospital.objects.get(id=pk)
    # p represents the permanent  all staff
    # t represents temporary all staff
    # d represents development all staff
    p1 = hospital.biomedical_engineer_permanent_staff
    p2 = hospital.doctor_permanents_staff
    p3 = hospital.nurse_permanent_staff
    p4 = hospital.lab_technician_permanent_staff
    p5 = hospital.health_assistant_permanent_staff
    p6 = hospital.biomedical_technician_permanent_staff
    p7 = hospital.pharmacist_permanent_staff
    p8 = hospital.radio_grapher_permanent_staff
    p9 = hospital.other_paramedics_permanent_staff
    # temporary staff
    t1 = hospital.biomedical_engineer_temperoray_staff
    t2 = hospital.doctor_temperoray_staff
    t3 = hospital.nurse_temperoray_staff
    t4 = hospital.lab_technician_temperoray_staff
    t5 = hospital.health_assistant_temperoray_staff
    t6 = hospital.biomedical_technician_temperoray_staff
    t7 = hospital.pharmacist_temperoray_staff
    t8 = hospital.radio_grapher_temperoray_staff
    t9 = hospital.other_paramedics_temperoray_staff
    # development staff
    d1 = hospital.biomedical_engineer_development_staff
    d2 = hospital.doctor_development_staff
    d3 = hospital.nurse_development_staff
    d4 = hospital.lab_technician_development_staff
    d5 = hospital.health_assistant_temperoray_staff
    d6 = hospital.biomedical_technician_development_staff
    d7 = hospital.pharmacist_development_staff
    d8 = hospital.radio_grapher_development_staff
    d9 = hospital.other_paramedics_development_staff

    labels = ["Biomedical Engineer", "Doctor", "Nurse", "Lab Technician", "Health Assistance", "Biomedical Technician",
              "Pharmacist", "Radio grapher", "Others"]
    data = [p1, p2, p3, p4, p5, p6, p7, p8, p9]
    data1 = [t1, t2, t3, t4, t5, t6, t7, t8, t9]
    data2 = [d1, d2, d3, d4, d5, d6, d7, d8, d9]
    return JsonResponse(data={
        'labels': labels,
        'data': data,
        'data1': data1,
        'data2': data2,
    })


def hospitalUpdate(request, id):
    hospital = Hospital.objects.get(id=id)

    if request.method == 'POST':
        form = HospitalForm(request.POST, instance=hospital)
        if form.is_valid():
            # update the existing `Band` in the database
            form.save()
            # redirect to the detail page of the `Band` we just updated
            return redirect('adminViewHospital')
    else:
        form = HospitalForm(instance=hospital)

    return render(request,
                  'admin/hospital_update.html',
                  {'form': form})


def updateVoter(request):
    if request.method != 'POST':
        messages.error(request, "Access Denied")
    try:
        instance = Hospital.objects.get(id=request.POST.get('id'))
        hospital = HospitalForm(request.POST or None, instance=instance)
        hospital.save()
        messages.success(request, "Voter's bio updated")
    except:
        messages.error(request, "Access To This Resource Denied")

    return redirect(reverse('adminViewHospital'))


def deleteHospital(request, pk):
    hospital = Hospital.objects.get(id=pk)
    hospital.delete()
    messages.success(request, "Hospital has been deleted")
    return redirect(reverse('adminViewHospital'))


def add_equipment(request):
    equipments = Equipment.objects.all()
    # userForm = CustomUserForm(request.POST or None)
    equipment_form = EquipmentsForm(request.POST or None)
    context = {
        # 'form1': userForm,
        'form': equipment_form,
        'equipments': equipments,
        'page_title': 'Add Equipment'
    }
    if request.method == 'POST':
        if equipment_form.is_valid():
            # user = userForm.save(commit=False)
            equipment = equipment_form.save(commit=False)
            # hospital.admin = user
            # user.save()
            equipment.save()
            messages.success(request, "New Equipment add successfully")
            return redirect('viewEquipments')
        else:
            messages.error(request, "Form validation failed")
    return render(request, "admin/add_equipment.html", context)


def viewEquipments(request):
    equipments = Equipment.objects.all()
    form = EquipmentsForm(request.POST or None)
    context = {
        'equipments': equipments,
        'form1': form,
        'page_title': "Equipments"
    }
    if request.method == 'POST':
        if form.is_valid():
            form = form.save(commit=False)
            form.save()
            messages.success(request, "New Position Created")
        else:
            messages.error(request, "Form errors")
    return render(request, "admin/positions.html", context)


def view_equipment(request, pk):
    equipment = Equipment.objects.get(id=pk)
    operational = equipment.operational
    maintenance = equipment.in_maintenance
    not_operational = equipment.not_operational
    et = operational + maintenance + not_operational  # et means total equipments
    if et == 0:
        total = 1
    else:
        total = et
    opnl = int(operational * 100 / total)
    nopnl = int(not_operational * 100 / total)
    mtn = int(maintenance * 100 / total)
    context = {
        'equipment': equipment,
        'total': total,
        'opnl': opnl,
        'nopnl': nopnl,
        'mtn': mtn,
        'page_title': 'Equipment'
    }
    return render(request, 'admin/equipment_detail_view.html', context)


def updateEquipment(request, pk):
    equipment = Equipment.objects.get(id=pk)

    if request.method == 'POST':
        form1 = EquipmentsForm(request.POST, instance=equipment)
        if form1.is_valid():
            # update the existing `Band` in the database
            form1.save()
            # redirect to the detail page of the `Band` we just updated
            messages.success(request, "Equipments has been updated successfully.")
            return redirect('viewEquipments')
    else:
        form1 = EquipmentsUpdateForm(instance=equipment)

    return render(request,
                  'admin/equipment_update.html',
                  {'form1': form1, 'equipment': equipment, 'page_title': 'Update Equipment'})


def deleteEquipment(request, pk):
    pos = Equipment.objects.get(id=pk)
    pos.delete()
    messages.success(request, "Position Has Been Deleted")
    return redirect(reverse('viewEquipments'))


def view_all_request(request):
    requests = HelpRequest.objects.filter(request_status='unsolved')
    context = {
        'requests': requests,
        'page_title': 'view requests'
    }
    return render(request, 'admin/view_requests.html', context)


def update_request(request, pk):
    requests = HelpRequest.objects.get(id=pk)
    if request.method == 'POST':
        form1 = RequestForm(request.POST, instance=requests)
        if form1.is_valid():
            # update the existing `Band` in the database
            form1.save()
            # redirect to the detail page of the `Band` we just updated
            messages.success(request, "Equipments has been updated successfully.")
            return redirect('requests')
    else:
        form1 = RequestForm(instance=requests)
    context = {
        'requests': requests,
        'form': form1,
        'page_title': 'Update Request'
    }
    return render(request, 'admin/update_request.html', context)


def view_trainer_detail(request, pk):
    trainer = Trainer.objects.get(id=pk)
    skills = Skills.objects.filter(trainer=trainer.id)
    trainings = Trainings.objects.filter(trainer=trainer.id)
    lat = trainer.latitude
    lng = trainer.longitude
    td = trainer.name + "," + trainer.phone
    country = "Nepal"
    m = folium.Map(location=[27.6625, 85.4376], zoom_start=8)

    folium.Marker([lat, lng], tooltip=td,
                  popup=country).add_to(m)
    m = m._repr_html_()
    context = {
        'trainer': trainer,
        'page_title': 'Trainer Profile',
        'skills': skills,
        'trainings': trainings,
        'm': m,
    }
    return render(request, 'hospital_admin/hospital/trainer_profile.html', context)



