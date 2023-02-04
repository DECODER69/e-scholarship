
from dataclasses import field
import csv
from distutils.command.build_scripts import first_line_re
from genericpath import exists
import io

from pkgutil import extend_path
import re
from subprocess import IDLE_PRIORITY_CLASS
from turtle import end_fill
from webbrowser import get
from django.http import HttpResponseRedirect
from django.http.request import QueryDict
from pkgutil import extend_path


from http.client import HTTPResponse
from django.urls import reverse
from multiprocessing import context
from pickle import FALSE
# from re import S
from tabnanny import check
from tkinter import FLAT
from urllib import response
from django.shortcuts import render, redirect,  reverse
from django.contrib.auth.models import User, auth
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages 
from django.contrib.auth.decorators import login_required
import datetime
import datetime as dt
#models imported
from .models import extenduser,school_year, sections, training_day,Announcement, certification, name_care_of, feedbacks
import os
import csv  

from django.http import HttpResponse, Http404

# emails
from django.core.mail import send_mail
from django.db import IntegrityError

# Create your views here.

# track active users
from django.utils.timezone import now
from datetime import timedelta
from datetime import datetime

# for pdf


from django.http import FileResponse
from django.template.loader import get_template
from django.shortcuts import render
from io import BytesIO
import os
from django.conf import settings


from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle

from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter

import pandas as pd
#   PAGE SHOWING
def index(request):
    return render(request, 'activities/landing.html')
def signup_page(request):
    schools = sections.objects.all()
    context = {
        'schools':schools,
    }
    return render(request, 'activities/signup.html', context)
def login_page(request):
    return render(request, 'activities/login.html')

@login_required(login_url='/login_page')
def dashboard_page(request):
    
    name = extenduser.objects.filter(user = request.user)
    anns = Announcement.objects.all().order_by('date_posted').reverse()
    context = {
        'name': name,
        'anns':anns
    }
    return render(request, 'activities/dashboard.html', context)
@login_required(login_url='/login_page')

@login_required(login_url='/login_page')
def editprofile(request):
    editwow = extenduser.objects.filter(user=request.user)
    context = {
        'ediwow':editwow,
    }
    return render(request, 'activities/editprofile.html', context)
@login_required(login_url='/login_page')
def others(request):
    uwu = extenduser.objects.filter(user=request.user)
    context = {
        'uwu':uwu,
    }
    return render(request, 'activities/others.html', context)
@login_required(login_url='/login_page')
def health(request):
    uwus = extenduser.objects.filter(user=request.user)
    context = {
        'uwus':uwus,
    }
    return render(request, 'activities/health.html', context)

def file_manager(request):
    return render(request, 'activities/file_manager.html')

def files_rotc(request):
    return render(request, 'activities/files_rotc.html')
def files_cwts(request):
    return render(request, 'activities/files_cwts.html')
def fields(request):
    return render(request, 'activities/fields.html')

def field_rotc(request):
    return render(request, 'activities/field_rotc.html')



def admin_nav(request):
    pending = extenduser.objects.filter(status='PENDING').count()
    
    context = {
        'pending':pending,
        
    }
    return render(request, 'activities/admin_nav.html', context)
def navbar(request):
    return render(request, 'activities/navbar.html')
def logout_student(request):
    logout(request)
    return redirect('/')

# ADMIN DISPLAY PAGE###################################
####################
#####################
####################
#########################
# ADMIN PAGE DISPLAYS
@login_required(login_url='/login_page')
def admin_dashboard(request):
    end_date = datetime.now()
    start_date = end_date - timedelta(days=1)
    if request.user.is_superuser:
        feed = feedbacks.objects.filter(status='PENDING')
        audience = sections.objects.all()
        ann = Announcement.objects.all()
        sy = school_year.objects.all()
        active = extenduser.objects.filter(status='APPROVED').count()
        pending = extenduser.objects.filter(status='PENDING').count()
        processing = extenduser.objects.filter(status='PROCESSING').count()
        cnt = sections.objects.all().count()
        nav_pending_count = extenduser.objects.filter(status='PENDING').count()
        new = extenduser.objects.filter(date_applied__range= (start_date, end_date)).count()
        exam = extenduser.objects.filter(date_exam__range= (start_date, end_date)).count()
        ip = extenduser.objects.filter(ip_status='IP').count()
        ip_pday = extenduser.objects.filter(date_applied__range= (start_date, end_date)).count()
        context = {
            'active':active,   
            'pending':pending,
            'sy':[sy.last()],
            'audience':audience,
            'ann':ann,
            'cnt':cnt,
            'nav_pending_count':nav_pending_count,
            'new':new,
            'exam':exam,
            'processing':processing,
            'ip':ip,
            'ip_pday':ip_pday,
            'feed':feed
        
        
        }
        return render(request, 'activities/admin_dashboard.html', context)
    else:
        messages.info(request, 'Invalid User Type')
    return redirect('/')

@login_required(login_url='/admin_login')
def admin_staff(request):
    if request.user.is_superuser:
        care_off = name_care_of.objects.all()
        s_years = school_year.objects.all()
        details = extenduser.objects.filter(status='PENDING')
        pendings = extenduser.objects.filter(status='PENDING')
        pending = extenduser.objects.filter(status='PENDING').count()

        context = {
            'pending':pending,
            'details': details,
            'pendings':pendings,
            's_years':[s_years.last()],
            'care_off':care_off
        
        }
        
        return render(request, 'activities/admin_staffs.html', context)

def admin_pending(request):
    care_off = name_care_of.objects.all()
    platoons = sections.objects.all()
    pending = extenduser.objects.filter(status='PROCESSING').count()
    pendings = extenduser.objects.filter(status='PROCESSING')
    context = {
        'pendings':pendings,
        'pending':pending,
        'platoons':platoons,
        'care_off':care_off
    }
    return render(request, 'activities/admin_pending.html', context)

def admin_approved(request):
    # pending = extenduser.objects.filter(status='PENDING').count()
    rejected = extenduser.objects.filter(status='APPROVED')

    context = {
      
        'rejected':rejected,
       
    }
    return render(request, 'activities/admin_rejected.html', context)

def admin_view_profile(request, id):
    profiles = extenduser.objects.filter(id=id)
    pending = extenduser.objects.filter(status='PENDING').count()
    context = {
        'profiles':profiles,
        'pending':pending
    }
    return render(request, 'activities/pending_view.html', context)



def school_years(request):
   
    s_years = school_year.objects.all()
    ss_years = extenduser.objects.all()
    ewan = school_year.objects.all()
   
    context = {
        'ewan':ewan,
        's_years':[s_years.last()],
        'ss_years':ss_years,
        # 'graduates':graduates
        
    }

    return render(request, 'activities/sy.html', context)

def create_platoon_page(request):
    current_datetime = dt.datetime.now() 
    userContent = User.objects.all()
    sectionxx = extenduser.objects.all()
    counts = extenduser.objects.filter(status='APPROVED').count()
    counts1 = extenduser.objects.filter(status='APPROVED')
    section = sections.objects.all()
    section1 = sections.objects.all().count()
    context = {
        
    'counts':counts,
    'counts1':counts1,
    'section':section,
    'section1':section1,
    'sectionxx':sectionxx,
    'userContent':userContent,
    'current_datetime':current_datetime,
    }
    return render (request, 'activities/create_platoon.html', context)




def create_platoon_page2(request):
    sectionxx = extenduser.objects.all()
    counts = extenduser.objects.filter(status='ENROLLED').count()
    counts1 = extenduser.objects.filter(status='APPROVED')
    section = sections.objects.all()
    section1 = sections.objects.all().count()
    context = {
        
    'counts':counts,
    'counts1':counts1,
    'section':section,
    'section1':section1,
    'sectionxx':sectionxx,
    }
    return render (request, 'activities/create_platoon2.html', context)

def manage_section(request):
    current_datetime = dt.datetime.now() 
    userContent = User.objects.all()
    sectionxx = extenduser.objects.all()
    counts = extenduser.objects.filter(status='ENROLLED').count()
    counts1 = extenduser.objects.filter(status='ENROLLED')
    section = sections.objects.all()
    section1 = sections.objects.all().count()
    secCount = request.POST.get('secCount')
    # counts3 = extenduser.objects.filter(status='ENROLLED').filter(platoons='ALPHA')
    context = {
        
    'counts':counts,
    'counts1':counts1,
    'section':section,
    'section1':section1,
    'sectionxx':sectionxx,
    'userContent':userContent,
    'current_datetime':current_datetime,
    # 'counts3':counts3
    }
 
    print(secCount)
    return render(request, 'activities/manage_section.html', context)
  






# MALI ITOOO

def attendance_main_page(request):
    return render(request, 'activities/attendance_main.html')


# eof mali




#   EOF PAGE SHOWING

# functions

def signup(request):
    if request.method == 'POST':
        firstname = request.POST.get('firstname')
        middle = request.POST.get('middlename')
        lastname = request.POST.get('lastname')
        email = request.POST.get('email')
        idnumber = request.POST.get('idnumber')
        password = request.POST.get('password1')
        school = request.POST.get('school')
        profile = request.FILES['picture']
        # s_year = request.POST.get('s_year')
        if User.objects.filter(username=idnumber).exists():
            messages.error(request, 'ID Number ' + str (idnumber) + ' Already Exist !')
            return redirect('/signup_page')
        elif extenduser.objects.filter(email=email).exists():
            messages.error(request, 'Email ' + str (email) + ' Already Exist !')
            return redirect('/signup_page')
       
        else:
            user = User.objects.create_user(username=idnumber, password=password, email=email)
            datas = extenduser(firstname=firstname, middlename=middle, lastname=lastname, email=email, idnumber=idnumber, password=password, school=school,user=user, picture=profile)
            datas.save()
            auth.login(request, user)
            messages.info(request, 'Account created successfully\nPlease Login and complete profile for verification')
            return redirect('/signup_page')
    else:
        return redirect('/')


# def signin(request):
#     if request.method == "POST":
#             username = request.POST.get('username')
#             password = request.POST.get('password')
#             if User.objects.filter(username=username).exists():
#                 user = authenticate(username=username, password=password)
#                 if user is not None:
#                     auth.login(request, user)
#                     return redirect('/dashboard_page')
#                 else:
#                     messages.error(request, 'Incorrect password')
#                     return redirect('/login_page')
#             else:
#                 messages.error(request, 'ID Number ' + str (username) + ' Does not exist !')
#                 return redirect('/login_page')
#     else:
#         messages.error(request, 'Invalid username or password !')
#         return redirect('/login_page')

def signin(request):
    if request.method == "POST":
            username = request.POST.get('username')
            password = request.POST.get('password')
            usertype = User.objects.filter(username=username).filter(is_staff=1)
            if User.objects.filter(username=username).exists():
                if usertype:
                    print("gago")
                    user = authenticate(username=username, password=password)
                    if user is not None:
                        auth.login(request, user)
                        return redirect('/admin_dashboard')
                    else:
                        messages.error(request, 'Incorrect password')
                        return redirect('/login_page')
                else:
                    user = authenticate(username=username, password=password)
                    if user is not None:
                        auth.login(request, user)
                        return redirect('/dashboard_page')
                    else:
                        messages.error(request, 'Incorrect password')
                        return redirect('/login_page')
                    
                
                
                # user = authenticate(username=username, password=password)
                # if user is not None:
                #     auth.login(request, user)
                #     return redirect('/dashboard_page')
                # else:
                #     messages.error(request, 'Incorrect password')
                #     return redirect('/login_page')
            else:
                messages.error(request, 'ID Number ' + str (username) + ' Does not exist !')
                return redirect('/login_page')
    else:
        messages.error(request, 'Invalid username or password !')
        return redirect('/login_page')


@login_required(login_url='/login_page')
def edit_others(request, id):
    hehe = extenduser.objects.get(id=id)
    if request.method == 'POST':
        hehe.idpic = request.FILES['studentid']
        image_path = hehe.idpic.path
        if os.path.exists(image_path):
            os.remove(image_path)
        hehe.save()
        return redirect('/health')
    return redirect('/others')

@login_required(login_url='/login_page')
def edit_health(request, id):
    hehes = extenduser.objects.get(id=id)
    if request.method == 'POST':
        proof = request.FILES['prof']
        if proof is not None:
            proof_path = proof.path
            if os.path.exists(proof_path):
                os.remove(proof_path)
                disease = request.POST.getlist('check')
                specific = request.POST.get('spec')
                hehes=extenduser(disease=disease, specific=specific)
                hehes.save()
                return redirect('/health')
            else:
                disease = request.POST.getlist('check')
                specific = request.POST.get('spec')
                hehes=extenduser(disease=disease, specific=specific)
                hehes.save()
                return redirect('/health')
    else:
        print("DONE")
        return redirect('/health')
    return redirect('/others')

def rotc_files(request):
    users = extenduser.objects.filter(user=request.user).filter(field='ROTC')
    if users:
        return redirect('/files_rotc')
    else:
        messages.error(request, 'You Are not Enrolled here !')
        return redirect('/file_manager')
    
def cwts_files(request):
    users = extenduser.objects.filter(user=request.user).filter(field='CWTS')
    if users:
        return redirect('/files_cwts')
    else:
        messages.error(request, 'You Are not Enrolled here !')
        return redirect('/file_manager')




########################
############################
######################
#############

# ADMIN FUNCTIONS ################################

def approve(request, idnumber):
    stat2 = request.POST.get('getID')
    platoons = request.POST.get('platoons')
    

    extenduser.objects.filter(idnumber=stat2).update(status='APPROVED', platoons=platoons)
    messages.success(request, 'Student ' + str (stat2) + ' has been Approved !')
    return redirect('/admin_pending')

def decline(request, id):
   
    stat2 = request.POST.get('getID2')
   
    print(stat2)
    extenduser.objects.filter(idnumber=stat2).update(status='REJECTED')
    messages.success(request, 'Student ' + str (stat2) + ' has been Rejected !')
    return redirect('/admin_pending')

def r_approve(request, idnumber):
    stat2 = request.POST.get('getID')
    platoons = request.POST.get('platoons')
    

    extenduser.objects.filter(idnumber=stat2).update(status='APPROVED', platoons=platoons)
    messages.success(request, 'Student ' + str (stat2) + ' has been Approved !')
    return redirect('/admin_rejected')

def r_decline(request, id):
   
    stat2 = request.POST.get('getID2')
   
    print(stat2)
    extenduser.objects.filter(idnumber=stat2).update(status='REJECTED')
    messages.success(request, 'Student ' + str (stat2) + ' has been Rejected !')
    return redirect('/admin_rejected')



# EMAILS
def rejected_email_page(request, id):
    rejects = extenduser.objects.filter(status='REJECTED')
    ems = extenduser.objects.filter(id=id)
    context = {
        'rejects':rejects,
        'ems':ems
    }
    
    
    return render(request, 'activities/rejected_email.html', context)

def custom(request):
    if request.method == 'POST':
        try:
            sub = request.POST.get('emailtext')
            msg = request.POST.get('message')
            emaila = request.POST.get('cusemail')
            send_mail(sub, msg,'escholarship2022@gmail.com',[emaila])
            return redirect('/admin_rejected')
        except ImportError:
            messages.success(request, 'Email Encountered some errors. Please Contact your Administrator')
    return redirect('/admin_rejected')
        
def create_sy(request):
    if request.method == 'POST':
        yearsz = request.POST.get('year')
        if school_year.objects.filter(years=yearsz).exists():
            messages.info(request, 'School year ' + str (yearsz) + ' ALready exist !')
            return redirect('/school_years')
        else:
            data = school_year(years=yearsz)
            data.save()
            messages.success(request, 'School year ' + str (yearsz) + ' Successfully Created !')
            return redirect('/school_years')
    return redirect('/school_years')

def allumni_content(request):
    if request.method == 'POST':
        getYear = request.POST.get('getYear')
        content = extenduser.objects.filter(s_year=getYear).filter(status='GRADUATE')
        content2 = extenduser.objects.filter(s_year=getYear).count()
    else:
        print("hahahahaaha")
        return render(request, 'activities/allumni_content.html')
    context = {
        'content':content,
        'content2':content2,
        'getYear':getYear,
    }
    print(getYear)


    return render(request, 'activities/allumni_content.html', context)




def delete_sy(request, id):
    school_year.objects.filter(id=id).delete()
    print(id)
    return redirect('/school_years')

def create_section(request):
    if request.method == 'POST':
        secs = request.POST.get('secs')
        logos = request.FILES['logos']
        print("pogi" +str(field))
        if secs is not None and field is not None:
            if sections.objects.filter(section_created  = secs).exists():
                messages.info(request, 'Section ' + str (secs) + ' Already exist !')
                return redirect('/manage_section')
            else:
                data = sections(section_created=secs, fiel=logos)
                data.save()
                messages.info(request, 'School ' + str (secs) + ' Created !')
                return redirect('/manage_section')
        else:
            messages.info(request, 'Please Input Something!! Ex: ALPHA')
            return redirect('/manage_section')
    return redirect('/manage_section')

def counts(request, secton_created):
    data1 = extenduser.objects.all()
    if request.method == 'POST':
        
        get_section = request.POST.get('get_section')
        get_count = extenduser.objects.filter(platoons=get_section).filter(status='ENROLLED').count()
        context = {
            'get_count':get_count,
            'data1':data1
        }
        
        return redirect('/create_platoon_page', context)
    return redirect('/create_platoon_page', context)



def view_images(request, id):
    counts = extenduser.objects.filter(status='ENROLLED').count()
    counts1 = extenduser.objects.filter(status='ENROLLED')
    section = sections.objects.all()
    section1 = sections.objects.all().count()
    datas = extenduser.objects.filter(id=id)
    sectionxx = extenduser.objects.all()
    userContent = User.objects.all()
    context = {
        'datas':datas,
        'counts':counts,
        'counts1':counts1,
        'section':section,
        'section1':section1,
        'sectionxx':sectionxx,
        'userContent':userContent
    }

    return render(request, 'activities/create_platoon2.html', context)

def edit_manage(request, id):
    counts = extenduser.objects.filter(status='ENROLLED').count()
    counts1 = extenduser.objects.filter(status='ENROLLED')
    section = sections.objects.all()
    section1 = sections.objects.all().count()
    datas = extenduser.objects.filter(id=id)
    sectionxx = extenduser.objects.all()
    userContent = User.objects.all()
    context = {
        'datas':datas,
        'counts':counts,
        'counts1':counts1,
        'section':section,
        'section1':section1,
        'sectionxx':sectionxx,
        'userContent':userContent
    }
    if request.method == 'POST':
        try:
            id= request.POST.get('ids')
            sub = request.POST.get('emailtext')
            msg = request.POST.get('message')
            emaila = request.POST.get('rname')
            send_mail(sub, msg,'escholarship2022@gmail.com',[emaila])
            messages.success(request, 'Email Sent to ' +str(emaila))
            
        except ImportError:
            messages.success(request, 'Email Encountered some errors. Please Contact your Administrator')

    return render (request, 'activities/edit_manage.html', context)


        
        
        
    


def export(request):
    normal_style = xlwt.easyxf("""
     font:
         name Verdana
     """) 
    response = HTTPResponse(content_type='application/ms-excel')
    wb = xlwt.Workbook()
    ws0 = wb.add_sheet('Worksheet')
    ws0.write(0, 0, "something", normal_style)
    wb.save(response)
    return response

def edit_student(request, id):
    idnums = request.POST.get('geti')

    firstname = request.POST.get('firstname')
    middle = request.POST.get('middle')
    lastname = request.POST.get('lastname')
    email = request.POST.get('email')
    idnumber = request.POST.get('idnumber')
    gender = request.POST.get('gender')
    address = request.POST.get('address')
    cpnumber = request.POST.get('cpnumber')
    birthday = request.POST.get('birthday')
    age = request.POST.get('age')
    section = request.POST.get('section')
    civil = request.POST.get('civil')
    nfather = request.POST.get('nfather')
    foccupation  =request.POST.get('foccupation')
    pcontact = request.POST.get('pcontact')
    nmother = request.POST.get('nmother')
    moccupation  =request.POST.get('moccupation')
    pcontact = request.POST.get('pcontact')
    disease = request.POST.get('disease')
    specific = request.POST.get('specific')
    
    extenduser.objects.filter(id=idnums).update(firstname=firstname, middlename = middle, 
                                                lastname=lastname, email=email, idnumber=idnumber, gender=gender,
                                                address=address, cpnumber=cpnumber, birthday=birthday, age=age, 
                                                section=section, civil=civil, nfather=nfather, foccupation=foccupation,
                                                pcontact=pcontact, nmother=nmother, moccupation=moccupation, disease=disease, specific=specific)

    return redirect('/create_platoon_page')
    
    



def section_content(request):
    current_datetime = dt.datetime.now() 
    userContent = User.objects.all()
    schools = school_year.objects.all()
    if request.method == 'POST':
     
        getSection = request.POST.get('getSection')
       
        content3 = extenduser.objects.filter(school=getSection).filter(status='APPROVED')
        print("school" + str(content3))
        print(getSection)
        content33 = extenduser.objects.filter(school=getSection).filter(status='APPROVED').count()
        ip = extenduser.objects.filter(school=getSection, status='APPROVED').filter(ip_status='IP').count()
        non_ip  =extenduser.objects.filter(school=getSection, status='APPROVED').filter(ip_status='Non IP').count()
    else:
       
        return render(request, 'activities/pl_content.html')
    context = {
        'content3':content3,
        'userContent':userContent,
        'content33':content33,
        'getSection':getSection,
        'schools':[schools.last()],
        'ip':ip,
        'non_ip':non_ip,
        'current_datetime':current_datetime
         
    }
    print(content33)
    print(getSection)
    return render(request, 'activities/pl_content.html', context)

def download(request):
    if request.method == 'POST':
    
        csvfile = extenduser.objects.filter(status='APPROVED')
        response = HttpResponse(content_type='text/csv')  
        print("CSV FILE ITO" + str(csvfile))
        
        response['Content-Disposition'] = 'attachment; filename="List.csv"  '
        writer = csv.writer(response)  
        writer.writerow(['STUDENT NUMBER', 'FIRSTNAME', 'LASTNAME', 'COURSE', 'STATUS', 'START DATE', 'END DATE'])  
        for s in csvfile:  
   
            writer.writerow([s.idnumber, s.firstname, s.lastname, s.section, s.status, s.start_dates, s.end_date ])  
    return response  
def download1(request):
    if request.method == 'POST':
    
        csvfile = extenduser.objects.filter(status='APPROVED')
        response = HttpResponse(content_type='text/csv')  
        print("CSV FILE ITO" + str(csvfile))
        
        response['Content-Disposition'] = 'attachment; filename="Student list.csv"  '
        writer = csv.writer(response)  
        writer.writerow(['STUDENT NUMBER', 'FIRSTNAME', 'LASTNAME', 'NSTP COMPONENT', 'NSTP SECTION'])  
        for s in csvfile:  
   
            writer.writerow([s.idnumber, s.firstname, s.lastname, s.field, s.platoons])  
    return response  



def create_day(request):
    if request.method == 'POST':
   
        title = request.POST.get('title')
  
        if training_day.objects .filter(title=title).exists():
            messages.info(request, (title) + ' Already exist !')
            return redirect('/attendance_page')

        else:
            data = training_day( title=title)
            data.save()
            messages.info(request, (title) + ' Created !')
            return redirect('/attendance_page')

    return redirect('/attendance_page')

def section_day(request):
    return redirect('/attendance_page')

def create_announcement(request):
    date = dt.datetime.now()  
    if request.method == 'POST':
        assign = request.POST.get('assign')
        subject = request.POST.get('subject')
        content = request.POST.get('content')
        context = {
            'assign':assign
        }
        
        alls = Announcement(assign=assign, subject=subject, content=content, date_posted=date)
        alls.save()
        messages.info(request, 'Announcement ' + str(subject + ' has been posted.'))
        return redirect('/admin_dashboard', context)
    return redirect('/admin_dashboard')

def edit_announcement(request, id):
    if request.method == 'POST':
        ID = request.POST.get('ID')
        content = request.POST.get('content')
        Announcement.objects.filter(id=ID).update(content=content)
        # messages.info(request, 'Edit Success')
        return redirect('/admin_dashboard')
    return redirect('/admin_dashboard')
def delete_announcement(request, id):
    Announcement.objects.filter(id=id).delete()
  
    return redirect('/admin_dashboard')

# for attendance only
     
def attendance_page(request):
    platoons = sections.objects.all()
    days = training_day.objects.all()
    day_count = training_day.objects.all().count()
    context = {
        'days':days,
        'day_count':day_count,
        'platoons':platoons
    }
    return render(request, 'activities/attendance_page.html', context)

def attendance_sections(request):
    platoons = sections.objects.all()
  
    t_days = request.POST.get('t_day')
    he = training_day.objects.filter(title=t_days)


    context = {
        'platoons':platoons,
        'he':he
    }
    return render(request, 'activities/attendance_section.html', context)

# def attendance_main_page(request):
#     return render(request, 'activities/attendance_main.html', context)


def attendance_main(request):
    schools = school_year.objects.all()
    counts = 3

    if request.method == 'POST':
        getSection = request.POST.get('getSection')
        # t_day = request.POST.get('t_day')
        # print("pogi ako talaga  " +str( t_day))
        
        sectionx = sections.objects.all()
        content3 = extenduser.objects.filter(platoons=getSection).filter(status='ENROLLED')
        content33 = extenduser.objects.filter(platoons=getSection).filter(status='ENROLLED').count()
        # messages.info(request, 'Attendance Up to date')

    else:
        return redirect('/attendance_sections')
    context = {
        'content3':content3,
        'content33':content33,
        'getSection':getSection,
        'schools':[schools.last()],
        'sectionx':sectionx,
        'counts':counts
        # 't_day':t_day
       
    }
    return render(request, 'activities/attendance_main.html', context)
  






    # return HttpResponseRedirect(request.session['getSection1'])

def pl_content(request):
    return render(request, 'activities/pl_content.html')

def add_students(request):
    if request.method == 'POST':
        platoon = request.POST.get('platoon')
        allstudent = extenduser.objects.filter(status='ENROLLED').filter(platoons='')
    else:
        return redirect('/manage_section')
    context = {
        'allstudent':allstudent,
        'platoon':platoon
    }
    return render(request, 'activities/students_list.html', context)

def assign_section(request):
    if request.method == 'POST':
        platoons=request.POST.get('platoons')
        lists = request.POST.getlist('students[]')
 
        for s in lists:
            extenduser.objects.filter(id=s).update(platoons=platoons)
            print("id ito" +str(s))
            messages.info(request, 'Adding Students to ' + str(platoons + ' done.'))

        messages.info(request, 'Adding Students to ' + str(platoons + ' done.'))
        print("tanga")
        return redirect('/manage_section')
    else:
        return redirect('/manage_section')

def update_sy(request, ):
    if request.method == 'POST':
        status = request.POST.get('status')
        current = request.POST.get('current')
        school_year.objects.filter(id=current).update(status=status)
        print("School year status Updated")
    return redirect('/school_years')

def update_officially(request, id):
    date_exam = dt.datetime.now()
    if request.method == 'POST':
        care_of = request.POST.get('care_of')
        stats = request.POST.get('slc')
        category = request.POST.get('category')
        
        idd = request.POST.get('idd')
        print("hahaha" +str(idd))
        if stats == 'PROCESSING':
            extenduser.objects.filter(id=idd).update(status=stats, care_of=care_of,  date_exam=date_exam, category=category)
        else:
            extenduser.objects.filter(id=idd).update(status=stats)
    return redirect('/admin_staff')

def cert_page(request):
    sys = school_year.objects.all()
    pota = extenduser.objects.filter(status='ENROLLED')
    # last = school_year.objects.all()
    details = certification.objects.all()
    context = {
        'sys':sys,
        'details':[details.last()],
        'pota':pota,
        # 'last':[last.last()],
    }
    return render(request, 'activities/certificate_page.html', context)

def open_cert_page(request):
    section = sections.objects.all()
    if request.method == 'POST':
        sy = request.POST.get('years')
        bracket = extenduser.objects.filter(s_year=sy)
        sen5 = school_year.objects.filter(years=sy)

        context = {
            'bracket':bracket,
            'section':section,
            'sen5':sen5
         
        }
    
    return render(request, 'activities/cert_section.html', context)

def generate(request):
    
    if request.method == 'POST':
        years = request.POST.get('years')
        sys1 = school_year.objects.filter(years=years)
        section = request.POST.get('section')
        details = certification.objects.all()
        yyy =  extenduser.objects.filter(s_year=years).filter(status='GRADUATE')
        namess = extenduser.objects.filter(s_year=years).filter(status='GRADUATE')
        print(section)
        print("pogi"+str(years))
        
        context = {
            'yyy':yyy,
            'sys1':sys1,
            'namess':namess,
            'details':[details.last()],
            
        }
        return render(request, 'activities/certificate.html', context)
    
def add_details(request):
    if request.method == 'POST':
        sys1 = request.POST.get('sys1')
        commandant = request.POST.get('commandant')
        registrar = request.POST.get('registrar')
        month = request.POST.get('month')
        date = request.POST.get('date')
        year = request.POST.get('year')
        data = certification(school_year2=sys1, commandant=commandant, registrar=registrar, month=month, date=date, year=year)
        data.save()
    return redirect('/cert_page', context)

def update_acts(request):
    if request.method == 'POST':
        current_datetime = datetime.datetime.now() 
        ids= request.POST.get('ids')
        print("hahahaha" + str(ids))
        school_year.objects.filter(years=ids).update(acts='DONE', date_generated=current_datetime)
        print("hahahaha" + str(ids))
        return redirect('/cert_page')
        
def admin_files(request):
    section = sections.objects.all()
    context = {
        'section':section
    }
    return render(request, 'activities/admin_files.html', context)

def open_folder(request,section_created):
   
    getSection = request.POST.get('getSection')
    print("hahahahahahaha" +str(getSection))
    context = {
    'getSection':getSection
    }

    return render(request, 'activities/open_folder.html', context)

def dropped(request):
    current_datetime = dt.datetime.now() 
    userContent = User.objects.all()
    sectionxx = extenduser.objects.all()
    counts = extenduser.objects.filter(status='DROP').count()
    counts1 = extenduser.objects.filter(status='DROP')
    section = sections.objects.all()
    section1 = sections.objects.all().count()
    context = {
        
    'counts':counts,
    'counts1':counts1,
    'section':section,
    'section1':section1,
    'sectionxx':sectionxx,
    'userContent':userContent,
    'current_datetime':current_datetime,
    }
    return render (request, 'activities/dropped.html', context)

def download3(request):
    if request.method == 'POST':
    
        csvfile = extenduser.objects.filter(status='DROP')
        response = HttpResponse(content_type='text/csv')  
        print("CSV FILE ITO" + str(csvfile))
        
        response['Content-Disposition'] = 'attachment; filename="Drop list.csv"  '
        writer = csv.writer(response)  
        writer.writerow(['STUDENT NUMBER', 'FIRSTNAME', 'LASTNAME', 'NSTP COMPONENT', 'NSTP SECTION', 'STATUS'])  
        for s in csvfile:  
   
            writer.writerow([s.idnumber, s.firstname, s.lastname, s.field, s.platoons, s.status])  
    return response  


def alumni_page(request):
    school_years = school_year.objects.all()
    context = {
        'school_years':school_years
    }
    return render(request, 'activities/allumni.html', context)


def download4(request):
    if request.method == 'POST':
        getSection = request.POST.get('cate')
        csvfile = extenduser.objects.filter(status='ENROLLED').filter(platoons=getSection)
        response = HttpResponse(content_type='text/csv')  
        print("CSV FILE ITO" + str(csvfile))
        
        response['Content-Disposition'] = 'attachment; filename="Attendance.csv"  '
        writer = csv.writer(response)  
        writer.writerow(['STUDENT NUMBER', 'FIRSTNAME', 'LASTNAME', 'SIGNATURE', 'REMARKS'])  
        for s in csvfile:  
   
            writer.writerow([s.idnumber, s.firstname, s.lastname])  
    return response  

def sample_attendance(request):

    section = sections.objects.all()
    date = training_day.objects.all()

    context = {
        'date':date, 
        'section':section,
    }

    return render(request, 'activities/sample_attendance.html', context)

def show_students(request):
    counted = training_day.objects.all()
    getSection = request.POST.get('getSection')
    content3 = extenduser.objects.filter(platoons=getSection).filter(status='ENROLLED')
    context = {
        'content3':content3,
        'getSection':getSection,
    }
    return render(request, 'activities/show_studens.html', context)

def create_td(request):
    if request.method == 'POST':
        td = request.POST.get('td')
        td_count = request.POST.get('td_count')
        if training_day.objects.filter(td=td).exists():
            messages.error(request, 'Training Day already exists ' +str(td))
            return redirect('/sample_attendance')
        elif training_day.objects.filter(td_count =td_count).exists():
            messages.error(request, 'Training Day count exists ' +str(td_count))
            return redirect('/sample_attendance')
        else:
            alls = training_day(td=td, td_count=td_count)
            alls.save()
            return redirect('/sample_attendance')
    return redirect('/sample_attendance')

def open_date(request):
    section = sections.objects.all()
    if request.method == 'POST':
        td_count = request.POST.get('td_count')
        date = request.POST.get('date')
        context = {
            'date':date,
            'section':section,
            'td_count':td_count
        }
        return render(request, 'activities/open_date.html', context)
    return render(request, 'activities/open_date.html')

def all_sections(request):
    all_section = sections.objects.all()
    date = training_day.objects.all()
    td_count = training_day.objects.all()
    td_counts = request.POST.get('td_counts')
    print("counts " +str(td_counts))
    context = {
        'all_section':all_section,
        'date':[date.last()],
        'td_count':[td_count.last()],
        'td_counts':td_counts
    }
    return render(request, 'activities/all_sections.html', context)

def open_sections(request):
    if request.method == 'POST':
        td_count = request.POST.get('td_count')
        date0 = request.POST.get('date')
        date1 = request.POST.get('date1')
        getSection = request.POST.get('getSection')

        student = extenduser.objects.filter(platoons=getSection).filter(status='ENROLLED')
        counts =  extenduser.objects.filter(platoons=getSection).filter(status='ENROLLED').count()
        print(getSection)
        print(date0)
        print(date1)
        context = {
            'date0':date0,
            'getSection':getSection,
            'student':student,
            'counts':counts,
            'date1':date1,
            'td_count':td_count
          
        }
 
        return render(request, 'activities/open_sections.html', context)
    return render(request, 'activities/open_sections.html')
    
def del_tday(request, id):

    training_day.objects.filter(id=id).delete()
    return redirect('/sample_attendance')

def download5(request):
    if request.method == 'POST':
        getSection = request.POST.get('cate')
        csvfile = extenduser.objects.filter(status='APPROVED').filter(platoons=getSection)
        response = HttpResponse(content_type='text/csv')  
        print("CSV FILE ITO" + str(csvfile))
        
        response['Content-Disposition'] = 'attachment; filename="Attendance.csv"  '
        writer = csv.writer(response)  
        writer.writerow(['STUDENT NUMBER', 'FIRSTNAME', 'LASTNAME', 'SIGNATURE', 'REMARKS'])  
        for s in csvfile:  
   
            writer.writerow([s.idnumber, s.firstname, s.lastname])  
    return response  

def rec_attendance(request):
    if request.method == 'POST':
        td_count = request.POST.get('td_count')
        ids = request.POST.getlist('id4')
        id2 = request.POST.getlist('id2')
        
        date1 = request.POST.get('check1')
        date0 = request.POST.get('check0')
        # print("date 0 ito " +str(date0))
        # print("date 1 ito " +str(date1))
        print("td count ito "+str(td_count))
        if date0 == 'None':
            if td_count == str(1):
                if ids:
                    for i in ids:
                        print("present date 0 "+str(i))
                        extenduser.objects.filter(id=i).update(TD1=date1)
                if id2:
                    for j in id2:
                        print("absent date 0 "+str(j))
                        extenduser.objects.filter(id=j).update(TD1='ABSENT')
                    
            elif td_count == str(2):
                if ids:
                    for i in ids:
                        print("present date 0 "+str(i))
                        extenduser.objects.filter(id=i).update(TD2=date1)
                if id2:
                    for j in id2:
                        print("absent date 0 "+str(j))
                        extenduser.objects.filter(id=j).update(TD2='ABSENT')
            elif td_count == str(3):
                if ids:
                    for i in ids:
                        print("present date 0 "+str(i))
                        extenduser.objects.filter(id=i).update(TD3=date1)
                if id2:
                    for j in id2:
                        print("absent date 0 "+str(j))
                        extenduser.objects.filter(id=j).update(TD3='ABSENT')
            elif td_count == str(4):
                if ids:
                    for i in ids:
                        print("present date 0 "+str(i))
                        extenduser.objects.filter(id=i).update(TD4=date1)
                if id2:
                    for j in id2:
                        print("absent date 0 "+str(j))
                        extenduser.objects.filter(id=j).update(TD4='ABSENT')
            elif td_count == str(5):
                if ids:
                    for i in ids:
                        print("present date 0 "+str(i))
                        extenduser.objects.filter(id=i).update(TD5=date1)
                if id2:
                    for j in id2:
                        print("absent date 0 "+str(j))
                        extenduser.objects.filter(id=j).update(TD5='ABSENT')
            elif td_count == str(6):
                if ids:
                    for i in ids:
                        print("present date 0 "+str(i))
                        extenduser.objects.filter(id=i).update(TD6=date1)
                if id2:
                    for j in id2:
                        print("absent date 0 "+str(j))
                        extenduser.objects.filter(id=j).update(TD6='ABSENT')
            elif td_count == str(7):
                if ids:
                    for i in ids:
                        print("present date 0 "+str(i))
                        extenduser.objects.filter(id=i).update(TD7=date1)
                if id2:
                    for j in id2:
                        print("absent date 0 "+str(j))
                        extenduser.objects.filter(id=j).update(TD7='ABSENT')
            elif td_count == str(8):
                if ids:
                    for i in ids:
                        print("present date 0 "+str(i))
                        extenduser.objects.filter(id=i).update(TD8=date1)
                if id2:
                    for j in id2:
                        print("absent date 0 "+str(j))
                        extenduser.objects.filter(id=j).update(TD8='ABSENT')
            elif td_count == str(9):
                if ids:
                    for i in ids:
                        print("present date 0 "+str(i))
                        extenduser.objects.filter(id=i).update(TD9=date1)
                if id2:
                    for j in id2:
                        print("absent date 0 "+str(j))
                        extenduser.objects.filter(id=j).update(TD9='ABSENT')
            elif td_count == str(10):
                if ids:
                    for i in ids:
                        print("present date 0 "+str(i))
                        extenduser.objects.filter(id=i).update(TD10=date1)
                if id2:
                    for j in id2:
                        print("absent date 0 "+str(j))
                        extenduser.objects.filter(id=j).update(TD10='ABSENT')
            elif td_count == str(11):
                if ids:
                    for i in ids:
                        print("present date 0 "+str(i))
                        extenduser.objects.filter(id=i).update(TD11=date1)
                if id2:
                    for j in id2:
                        print("absent date 0 "+str(j))
                        extenduser.objects.filter(id=j).update(TD11='ABSENT')
            elif td_count == str(12):
                if ids:
                    for i in ids:
                        print("present date 0 "+str(i))
                        extenduser.objects.filter(id=i).update(TD12=date1)
                if id2:
                    for j in id2:
                        print("absent date 0 "+str(j))
                        extenduser.objects.filter(id=j).update(TD12='ABSENT')
            elif td_count == str(13):
                if ids:
                    for i in ids:
                        print("present date 0 "+str(i))
                        extenduser.objects.filter(id=i).update(TD13=date1)
                if id2:
                    for j in id2:
                        print("absent date 0 "+str(j))
                        extenduser.objects.filter(id=j).update(TD13='ABSENT')
            elif td_count == str(14):
                if ids:
                    for i in ids:
                        print("present date 0 "+str(i))
                        extenduser.objects.filter(id=i).update(TD14=date1)
                if id2:
                    for j in id2:
                        print("absent date 0 "+str(j))
                        extenduser.objects.filter(id=j).update(TD14='ABSENT')
            elif td_count == str(15):
                if ids:
                    for i in ids:
                        print("present date 0 "+str(i))
                        extenduser.objects.filter(id=i).update(TD15=date1)
                if id2:
                    for j in id2:
                        print("absent date 0 "+str(j))
                        extenduser.objects.filter(id=j).update(TD15='ABSENT')
                    
                    # absents

                    
        if date1 == 'None':
            if td_count == str(1):
                if ids:
                    for i in ids:
                        print("present date 0 "+str(i))
                        extenduser.objects.filter(id=i).update(TD1=date0)
                if id2:
                    for j in id2:
                        print("absent date 0 "+str(j))
                        extenduser.objects.filter(id=j).update(TD1='ABSENT')
            elif td_count == str(2):
                if ids:
                    for i in ids:
                        print("present date 0 "+str(i))
                        extenduser.objects.filter(id=i).update(TD2=date0)
                if id2:
                    for j in id2:
                        print("absent date 0 "+str(j))
                        extenduser.objects.filter(id=j).update(TD2='ABSENT')
            elif td_count == str(3):
                if ids:
                    for i in ids:
                        print("present date 0 "+str(i))
                        extenduser.objects.filter(id=i).update(TD3=date0)
                if id2:
                    for j in id2:
                        print("absent date 0 "+str(j))
                        extenduser.objects.filter(id=j).update(TD3='ABSENT')
            elif td_count == str(4):
                if ids:
                    for i in ids:
                        print("present date 0 "+str(i))
                        extenduser.objects.filter(id=i).update(TD4=date0)
                if id2:
                    for j in id2:
                        print("absent date 0 "+str(j))
                        extenduser.objects.filter(id=j).update(TD4='ABSENT')
            elif td_count == str(5):
                if ids:
                    for i in ids:
                        print("present date 0 "+str(i))
                        extenduser.objects.filter(id=i).update(TD5=date0)
                if id2:
                    for j in id2:
                        print("absent date 0 "+str(j))
                        extenduser.objects.filter(id=j).update(TD5='ABSENT')
            elif td_count == str(6):
                if ids:
                    for i in ids:
                        print("present date 0 "+str(i))
                        extenduser.objects.filter(id=i).update(TD6=date0)
                if id2:
                    for j in id2:
                        print("absent date 0 "+str(j))
                        extenduser.objects.filter(id=j).update(TD6='ABSENT')
            elif td_count == str(7):
                if ids:
                    for i in ids:
                        print("present date 0 "+str(i))
                        extenduser.objects.filter(id=i).update(TD7=date0)
                if id2:
                    for j in id2:
                        print("absent date 0 "+str(j))
                        extenduser.objects.filter(id=j).update(TD7='ABSENT')
            elif td_count == str(8):
                if ids:
                    for i in ids:
                        print("present date 0 "+str(i))
                        extenduser.objects.filter(id=i).update(TD8=date0)
                if id2:
                    for j in id2:
                        print("absent date 0 "+str(j))
                        extenduser.objects.filter(id=j).update(TD8='ABSENT')
            elif td_count == str(9):
                if ids:
                    for i in ids:
                        print("present date 0 "+str(i))
                        extenduser.objects.filter(id=i).update(TD9=date0)
                if id2:
                    for j in id2:
                        print("absent date 0 "+str(j))
                        extenduser.objects.filter(id=j).update(TD9='ABSENT')
            elif td_count == str(10):
                if ids:
                    for i in ids:
                        print("present date 0 "+str(i))
                        extenduser.objects.filter(id=i).update(TD10=date0)
                if id2:
                    for j in id2:
                        print("absent date 0 "+str(j))
                        extenduser.objects.filter(id=j).update(TD10='ABSENT')
            elif td_count == str(11):
                if ids:
                    for i in ids:
                        print("present date 0 "+str(i))
                        extenduser.objects.filter(id=i).update(TD11=date0)
                if id2:
                    for j in id2:
                        print("absent date 0 "+str(j))
                        extenduser.objects.filter(id=j).update(TD11='ABSENT')
            elif td_count == str(12):
                if ids:
                    for i in ids:
                        print("present date 0 "+str(i))
                        extenduser.objects.filter(id=i).update(TD12=date0)
                if id2:
                    for j in id2:
                        print("absent date 0 "+str(j))
                        extenduser.objects.filter(id=j).update(TD12='ABSENT')
            elif td_count == str(13):
                if ids:
                    for i in ids:
                        print("present date 0 "+str(i))
                        extenduser.objects.filter(id=i).update(TD13=date0)
                if id2:
                    for j in id2:
                        print("absent date 0 "+str(j))
                        extenduser.objects.filter(id=j).update(TD13='ABSENT')
            elif td_count == str(14):
                if ids:
                    for i in ids:
                        print("present date 0 "+str(i))
                        extenduser.objects.filter(id=i).update(TD14=date0)
                if id2:
                    for j in id2:
                        print("absent date 0 "+str(j))
                        extenduser.objects.filter(id=j).update(TD14='ABSENT')
            elif td_count == str(15):
                if ids:
                    for i in ids:
                        print("present date 0 "+str(i))
                        extenduser.objects.filter(id=i).update(TD15=date0)
                if id2:
                    for j in id2:
                        print("absent date 0 "+str(j))
                        extenduser.objects.filter(id=j).update(TD15='ABSENT')

    return redirect('/sample_attendance', context)







def update_attendance(request):
    if request.method == 'POST':
        # presents
        td1 = request.POST.getlist('td1[]')
        td2 = request.POST.getlist('td2[]')
        td3 = request.POST.getlist('td3[]')
        td4 = request.POST.getlist('td4[]')
        td5 = request.POST.getlist('td5[]')
        td6 = request.POST.getlist('td6[]')
        td7 = request.POST.getlist('td7[]')
        td8 = request.POST.getlist('td8[]')
        td9 = request.POST.getlist('td9[]')
        td10 = request.POST.getlist('td10[]')
        td11 = request.POST.getlist('td11[]')
        td12 = request.POST.getlist('td12[]')
        td13 = request.POST.getlist('td13[]')
        td14 = request.POST.getlist('td14[]')
        td15 = request.POST.getlist('td15[]')
        
        # ABSENTS
        td1A = request.POST.getlist('td1A[]')
        td2A = request.POST.getlist('td2A[]')
        td3A = request.POST.getlist('td3A[]')
        td4A = request.POST.getlist('td4A[]')
        td5A = request.POST.getlist('td5A[]')
        td6A = request.POST.getlist('td6A[]')
        td7A = request.POST.getlist('td7A[]')
        td8A = request.POST.getlist('td8A[]')
        td9A = request.POST.getlist('td9A[]')
        td10A = request.POST.getlist('td10A[]')
        td11A = request.POST.getlist('td11A[]')
        td12A = request.POST.getlist('td12A[]')
        td13A = request.POST.getlist('td13A[]')
        td14A = request.POST.getlist('td14A[]')
        td15A = request.POST.getlist('td15A[]')

        for s in td1:
            extenduser.objects.filter(id=s).update(TD1='PRESENT')
            print(s)
        
        for s in td2:
            extenduser.objects.filter(id=s).update(TD2='PRESENT')
            print(s)
        
        for s in td3:
            extenduser.objects.filter(id=s).update(TD3='PRESENT')
        for s in td4:
            extenduser.objects.filter(id=s).update(TD4='PRESENT')
        for s in td5:
            extenduser.objects.filter(id=s).update(TD5='PRESENT')
        for s in td6:
            extenduser.objects.filter(id=s).update(TD6='PRESENT')

        for s in td7:
            extenduser.objects.filter(id=s).update(TD7='PRESENT')
        for s in td8:
            extenduser.objects.filter(id=s).update(TD8='PRESENT')
        for s in td9:
            extenduser.objects.filter(id=s).update(TD9='PRESENT')
        for s in td10:
            extenduser.objects.filter(id=s).update(TD10='PRESENT')
        for s in td11:
            extenduser.objects.filter(id=s).update(TD11='PRESENT')
        for s in td12:
            extenduser.objects.filter(id=s).update(TD12='PRESENT')
        for s in td13:
            extenduser.objects.filter(id=s).update(TD13='PRESENT')
        for s in td14:
            extenduser.objects.filter(id=s).update(TD14='PRESENT')
        for s in td15:
            extenduser.objects.filter(id=s).update(TD15='PRESENT')
            
            # ABSENNNNNNNNT
        for a in td1A:
            extenduser.objects.filter(id=a).update(TD1='ABSENT')
        for a in td2A:
            extenduser.objects.filter(id=a).update(TD2='ABSENT')
        for a in td3A:
            extenduser.objects.filter(id=a).update(TD3='ABSENT')
        for a in td4A:
            extenduser.objects.filter(id=a).update(TD4='ABSENT')
        for a in td5A:
            extenduser.objects.filter(id=a).update(TD5='ABSENT')
        for a in td6A:
            extenduser.objects.filter(id=a).update(TD6='ABSENT')
        for a in td7A:
            extenduser.objects.filter(id=a).update(TD7='ABSENT')
        for a in td8A:
            extenduser.objects.filter(id=a).update(TD8='ABSENT')
        for a in td9A:
            extenduser.objects.filter(id=a).update(TD9='ABSENT')
        for a in td10A:
            extenduser.objects.filter(id=a).update(TD10='ABSENT')
        for a in td11A:
            extenduser.objects.filter(id=a).update(TD11='ABSENT')
        for a in td12A:
            extenduser.objects.filter(id=a).update(TD12='ABSENT')
        for a in td13A:
            extenduser.objects.filter(id=a).update(TD13='ABSENT')
        for a in td14A:
            extenduser.objects.filter(id=a).update(TD14='ABSENT')
        for a in td15A:
            extenduser.objects.filter(id=a).update(TD15='ABSENT')
   
        messages.info(request, 'Attendance Up to date')
    return redirect('/attendance_page')
def update_years(request):
    if request.method == 'POST':
        act = request.POST.get('act')
        ids = request.POST.get('ids')
        start_dates = request.POST.get('start_date')
        end_dates = request.POST.get('end_date')
        print("start" +str(start_dates))
        print("end" +str(end_dates))
        extenduser.objects.filter(id=ids).update(start_dates=start_dates, end_date= end_dates, status=act)
    return redirect('/manage_section')



def del_school(request, section_created):
    print("id ito" +str(id))
    sections.objects.filter(section_created=section_created).delete()
    
    return redirect('/manage_section')


def graduates(request):
    section = sections.objects.all()
    context ={
        'section':section
    }
    return render(request, 'activities/graduates.html', context)



def open_anns(request, id):
    anns2 = Announcement.objects.filter(id=id)
    print(anns2)
    name = extenduser.objects.filter(user = request.user)
    anns = Announcement.objects.all()
    context={
        'anns':anns,
        'name':name,
        'anns2':anns2
    }
    return render(request, 'activities/anns_view.html', context)


def admin_login(request):
    return render(request, 'activities/admin_login.html')

def admin_log(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        if User.objects.filter(username=username).exists():
            user = authenticate(username=username, password=password)
            if User.is_superuser:
                if user is not None:
                    auth.login(request, user)
                    return redirect('/admin_dashboard')
                else:
                    messages.error(request, 'Incorrect password')
                    return redirect('/login_page')
            else:
                messages.error(request, 'Invalid User type')
                return redirect('/admin_login')
        else:
            messages.error(request, 'Username does no exists')
            return redirect('/admin_login')
    else:
        messages.error(request, 'Invalid username or password !')
        return redirect('/admin_login')
    
    
    
def admin_logout(request):
    logout(request)
    return redirect('/')

@login_required(login_url='/login_page')
def edit(request):
  
    if request.method == 'POST':
        gender = request.POST.get('gender')
        section = request.POST.get('section')
        email = request.POST.get('email')
        age = request.POST.get('age')
        civil = request.POST.get('civil')
        cpnumber = request.POST.get('cpnumber')
        address = request.POST.get('address')
        birthday = request.POST.get('birthday')
        nfather = request.POST.get('nfather')
        foccupation = request.POST.get('foccupation')
        nmother = request.POST.get('nmother')
        moccupation = request.POST.get('moccupation')
        pcontact = request.POST.get('pcontact')
        nguardian  = request.POST.get('nguardian')
        goccupation = request.POST.get('goccupation')
        gcontact = request.POST.get('gcontact')
        sources_income = request.POST.get('sources_income')
        monthly_income = request.POST.get('monthly_income')
        nationality = request.POST.get('nationality')
        print("hahahahahahaha")
   

    

      
        # print("image to" +str(grade_ss) )
        extenduser.objects.filter(user=request.user).update(gender=gender, section=section, email=email, age=age, 
                                                            civil=civil, cpnumber=cpnumber, address=address, birthday=birthday,
                                                            nfather=nfather, foccupation=foccupation, nmother=nmother, moccupation=moccupation,
                                                            pcontact=pcontact, nguardian=nguardian, goccupation=goccupation, gcontact=gcontact,
                                                            sources_income=sources_income, monthly_income=monthly_income, nationality=nationality)
        
        
        # extenduser.objects.filter(id=ids).update(grade_ss=grade)
        # ids.grade_ss = request.FILES['grade_ss']
        # if ids.grade_ss != ids.grade_ss:
        #     print("equal")
        #     image_path = ids.grade_ss.path
        #     if os.path.exists(image_path):
        #         os.remove(image_path)
        #         ids.save()
        #         print("nagsave")
        #         return redirect('/profile_page')
        #     else:
            
        #         ids.save()
        #         print("nagsave")
        #         return redirect('/profile_page')
        # else:
        #     print("hindi")
        #     return redirect('/profile_page')
        
        # image = extenduser.objects.get(id=id)
   
        # image.grade_ss = request.FILES['grade_ss']
        # image_path = image.grade_ss.path
        # if os.path.exists(image_path):
        #     os.remove(image_path)
        # image.save()
        return redirect('/profile_page')
   

    else:
        return redirect('/profile_page')
    
def profile_page(request):
    name = extenduser.objects.filter(user = request.user)
    usern = extenduser.objects.filter(user=request.user)
    context={
        'usern':usern,
        'name': name,
    }
    return render(request, 'activities/student_profile.html', context)



def feedback(request):
    if request.method == 'POST':
        try:
            sub = request.POST.get('subject')
            msg = request.POST.get('message')
            sender = request.POST.get('sender_email')
            receiver = ['escholarship2022@gmail.com',]
            send_mail(sub, msg ,sender, receiver)
            print(msg)
            return redirect('/')
        except ImportError:
            messages.success(request, 'Email Encountered some errors. Please Contact your Administrator')
    return redirect('/')



def contact_us(request):
    # sss
    return render(request, 'activities/contact_us.html')


# def send_feedback(request):
#     date_time = datetime.datetime.now() 
#     if request.method == 'POST':
#        name = request.POST.get('name')
#        email = request.POST.get('email')
#        subject = request.POST.get('subject')
#        message = request.POST.get('message')
#        data = feedback(sender=name, email=email, date_sent=date_time, subject=subject, message=message)
#        data.save()
#     return redirect('/contact_us')



def enrollment(request):
    name = extenduser.objects.filter(user = request.user)
    sy = school_year.objects.all()
    context = {
        'name': name,
        'sy':[sy.last()]

    }
    return render(request, 'activities/enrollment.html', context)


def requirements(request):
    name = extenduser.objects.filter(user = request.user)
    
    context = {
        'name': name
    }
    return render(request, 'activities/requirements.html', context)


def cor(request, id):
    hehe = extenduser.objects.get(id=id)
    if request.method == 'POST':
        hehe.cor = request.FILES['cor']
        cor_path = hehe.cor.path
        if os.path.exists(cor_path):
            os.remove(cor_path)
        hehe.save()
        return redirect('/requirements')
        
    return redirect('/requirements')


def cog(request, id):
    hehe = extenduser.objects.get(id=id)
    if request.method == 'POST':
        hehe.cog = request.FILES['cog']
        cog_path = hehe.cog.path
        if os.path.exists(cog_path):
            os.remove(cog_path)
        hehe.save()
        return redirect('/requirements')
        
    return redirect('/requirements')


def birth_cert(request, id):
    hehe = extenduser.objects.get(id=id)
    if request.method == 'POST':
        hehe.birth_cert = request.FILES['birth_cert']
        birth_cert_path = hehe.birth_cert.path
        if os.path.exists(birth_cert_path):
            os.remove(birth_cert_path)
        hehe.save()
        return redirect('/requirements')
        
    return redirect('/requirements')


def good_moral(request, id):
    hehe = extenduser.objects.get(id=id)
    if request.method == 'POST':
        hehe.good_moral = request.FILES['good_moral']
        good_moral_path = hehe.good_moral.path
        if os.path.exists(good_moral_path):
            os.remove(good_moral_path)
        hehe.save()
        return redirect('/requirements')
        
    return redirect('/requirements')


def barangay(request, id):
    hehe = extenduser.objects.get(id=id)
    if request.method == 'POST':
        hehe.barangay = request.FILES['barangay']
        barangay_path = hehe.barangay.path
        if os.path.exists(barangay_path):
            os.remove(barangay_path)
        hehe.save()
        return redirect('/requirements')
        
    return redirect('/requirements')


def mangyan(request, id):
    hehe = extenduser.objects.get(id=id)
    if request.method == 'POST':
        hehe.mangyan = request.FILES['mangyan']
        mangyan_path = hehe.mangyan.path
        if os.path.exists(mangyan_path):
            os.remove(mangyan_path)
        hehe.save()
        return redirect('/requirements')
        
    return redirect('/requirements')


def apply(request):
    date_applied = dt.datetime.now()
    if request.method == 'POST':
       
        idnumber = request.POST.get('idnumber')
        not_ip = request.POST.get('not-ip')
        ip = request.POST.get('ip')
        ipcat = request.POST.get('ip-cat')
        if not_ip is not None:
            extenduser.objects.filter(id=idnumber).update(ip_status=not_ip, status='PENDING', date_applied=date_applied)
        elif ipcat is not None:
            extenduser.objects.filter(id=idnumber).update(ip_status=ip,status='PENDING', ip_category='', date_applied=date_applied)
        
     

    
    return redirect('/enrollment')


def view_profile(request, id):
    name = extenduser.objects.filter(id=id)
    context = {
        'name': name
    }
    return render(request, 'activities/view_profile.html', context)


def action_applicant(request):
    date_exam = dt.datetime.now()
    if request.method == 'POST':
        options = request.POST.get('options')
        ids = request.POST.get('ids')
        
        if options == 'PROCESSING':
            extenduser.objects.filter(id=ids).update(status=options, date_exam=date_exam)
        else:
            extenduser.objects.filter(id=ids).update(status=options)
    return redirect('/admin_staff')



def add_score(request):
    date_approved = dt.datetime.now()
    if request.method == 'POST':
        ids = request.POST.get('ids')
      
        status = request.POST.get('status')
        score = request.POST.get('score')
        if status == 'APPROVED':
            sub = "E-SCHOLARSHIP EXAMINATION"
            msg = "Congratualtions! You have passed the e-Scholarship Examination."
            emaila = request.POST.get('cusemail')
            send_mail(sub, msg,'escholarship2022@gmail.com',[emaila])
            extenduser.objects.filter(id=ids).update(status=status,  exam_result=score, date_approved = date_approved) 
        else:
            sub = "E-SCHOLARSHIP EXAMINATION"
            msg = "Good day.  We are sorry to inform you that you have failed the e-Scholarship examination."
            emaila = request.POST.get('cusemail')
            send_mail(sub, msg,'escholarship2022@gmail.com',[emaila])
            extenduser.objects.filter(id=ids).update(status=status,  exam_result=score, date_approved = date_approved) 
    return redirect('/admin_pending')


def view_Approved(request, id):
    name = extenduser.objects.filter(id=id)
    context = {
        'name': name
    }
    return render(request, 'activities/view_approved.html', context)


def view_active(request, id):
    name = extenduser.objects.filter(id=id)
    context = {
        'name': name
    }
    return render(request, 'activities/edit_manage.html', context)

def school_view(request, id):
    name = extenduser.objects.filter(id=id)
    context = {
        'name': name
    }
    return render(request, 'activities/school_view.html', context)

def graduate_view(request, id):
    name = extenduser.objects.filter(id=id)
    context = {
        'name': name
    }
    return render(request, 'activities/graduate_view.html', context)


def view_care_of(request, id):
    name = extenduser.objects.filter(id=id)
    context = {
        'name': name
    }
    return render(request, 'activities/view_care_of.html', context)



def update_manage(request):
    if request.method == 'POST':
        ids = request.POST.get('ids')
        firstname = request.POST.get('firstname')
        middlename = request.POST.get('middlename')
        lastname = request.POST.get('lastname')
        address = request.POST.get('address')
        cpnumber = request.POST.get('cpnumber')
        birthday = request.POST.get('birthday')
        age = request.POST.get('age')
        civil = request.POST.get('civil')
        email = request.POST.get('email')
        idnumber = request.POST.get('idnumber')
        status =request.POST.get('status')
        field = request.POST.get('field')
        platoons = request.POST.get('platoons')
        section2 = request.POST.get('section')
        nfather = request.POST.get('nfather')
        foccupation = request.POST.get('foccupation')
        nmother = request.POST.get('nmother')
        moccupation  = request.POST.get('moccupation')
        pcontact = request.POST.get('pcontact')
        nguardian = request.POST.get('nguardian')
        goccupation = request.POST.get('goccupation')
        gcontact = request.POST.get('gcontact')
        sources_income = request.POST.get('sources_income')
        monthly_income = request.POST.get('monthly_income')
        start = request.POST.get('start')
        end = request.POST.get('end')
       
        extenduser.objects.filter(id=ids).update(firstname = firstname, middlename = middlename, lastname = lastname, 
                                                 address = address, cpnumber=cpnumber, birthday=birthday, age=age,
                                                 civil=civil,email=email,idnumber=idnumber,status=status,field=field,
                                                 platoons=platoons, section=section2,nfather=nfather, foccupation=foccupation, nmother=nmother, moccupation=moccupation,
                                                 pcontact=pcontact, nguardian=nguardian, goccupation=goccupation, gcontact=gcontact, sources_income=sources_income, monthly_income=monthly_income, start=start, end=end)
        User.objects.filter(id=ids).update(username=idnumber)
   
        messages.success(request, str(idnumber)+' has been Updated')
        # return redirect('/create_platoon_page')
        return redirect(request.META['HTTP_REFERER'])

    return redirect('/create_platoon_page')


def update_manage_2(request):
    if request.method == 'POST':
        ids = request.POST.get('ids')
        firstname = request.POST.get('firstname')
        middlename = request.POST.get('middlename')
        lastname = request.POST.get('lastname')
        address = request.POST.get('address')
        cpnumber = request.POST.get('cpnumber')
        birthday = request.POST.get('birthday')
        age = request.POST.get('age')
        civil = request.POST.get('civil')
        email = request.POST.get('email')
        idnumber = request.POST.get('idnumber')
        status =request.POST.get('status')
        field = request.POST.get('field')
        platoons = request.POST.get('platoons')
        section2 = request.POST.get('section')
        nfather = request.POST.get('nfather')
        foccupation = request.POST.get('foccupation')
        nmother = request.POST.get('nmother')
        moccupation  = request.POST.get('moccupation')
        pcontact = request.POST.get('pcontact')
        nguardian = request.POST.get('nguardian')
        goccupation = request.POST.get('goccupation')
        gcontact = request.POST.get('gcontact')
        sources_income = request.POST.get('sources_income')
        monthly_income = request.POST.get('monthly_income')
        start = request.POST.get('start')
        end = request.POST.get('end')
       
        extenduser.objects.filter(id=ids).update(firstname = firstname, middlename = middlename, lastname = lastname, 
                                                 address = address, cpnumber=cpnumber, birthday=birthday, age=age,
                                                 civil=civil,email=email,idnumber=idnumber,status=status,field=field,
                                                 platoons=platoons, section=section2,nfather=nfather, foccupation=foccupation, nmother=nmother, moccupation=moccupation,
                                                 pcontact=pcontact, nguardian=nguardian, goccupation=goccupation, gcontact=gcontact, sources_income=sources_income, monthly_income=monthly_income, start=start, end=end)
        User.objects.filter(id=ids).update(username=idnumber)
   
        messages.success(request, str(idnumber)+' has been Updated')
        # return redirect('/create_platoon_page')
        return redirect(request.META['HTTP_REFERER'])

    return redirect('/create_platoon_page')
def graduates_list(request):
    schools = school_year.objects.all()
    current_datetime = dt.datetime.now() 
    if request.method == 'POST':
     
        getSection = request.POST.get('getSection')
       
        content3 = extenduser.objects.filter(school=getSection).filter(status='GRADUATE')
        print("school" + str(content3))
        print(getSection)
        content33 = extenduser.objects.filter(school=getSection).filter(status='GRADUATE').count()
        ip = extenduser.objects.filter(school=getSection, status='GRADUATE').filter(ip_status='IP').count()
        non_ip  =extenduser.objects.filter(school=getSection, status='GRADUATE').filter(ip_status='Non IP').count()
    else:
       
        return render(request, 'activities/graduates_list.html')
    context = {
        'content3':content3,
        
        'content33':content33,
        'getSection':getSection,
        'schools':[schools.last()],
        'current_datetime':current_datetime,
        'ip':ip,
        'non_ip':non_ip
         
    }
    print(content33)
    print(getSection)
    return render(request, 'activities/graduates_list.html', context)


def care_of(request):
    name = name_care_of.objects.all()
    context ={
        'name':name
    }
    return render(request, 'activities/care_of.html', context)


def create_care_of(request):
    if request.method == 'POST':
        secs = request.POST.get('secs')

        print("pogi" +str(field))
        if secs is not None and field is not None:
            if name_care_of.objects.filter(name=secs).exists():
               
                return redirect('/care_of')
            else:
                data = name_care_of(name=secs)
                data.save()
               
                return redirect('/care_of')
        else:
          
            return redirect('/care_of')
    return redirect('/care_of')



def delete_care(request, id):
    name_care_of.objects.filter(id=id).delete()
 
    return redirect('/care_of')

def care_of_profile(request):
    
    current_datetime = dt.datetime.now() 
    if request.method == 'POST':
        ids = request.POST.get('ids')
        person = request.POST.get('person')
        print(ids)
     
        getSection = request.POST.get('getSection')
        names = name_care_of.objects.filter(id=ids)
        content3 = extenduser.objects.filter(care_of=person).filter(status='APPROVED')

        content33 = extenduser.objects.filter(care_of=person).filter(status='APPROVED').count()
        ip = extenduser.objects.filter(care_of=person, status='APPROVED').filter(ip_status='IP').count()
        non_ip  =extenduser.objects.filter(care_of=person, status='APPROVED').filter(ip_status='Non IP').count()
    else:
       
        return render(request, 'activities/graduates_list.html')
    context = {
        'content3':content3,
        
        'content33':content33,
        'getSection':getSection,
    
        'current_datetime':current_datetime,
        'ip':ip,
        'non_ip':non_ip,
        'names':names
         
    }
    print(content33)
    print(getSection)
    return render(request, 'activities/care_off_content.html',context)





def update_care_of(request):
    if request.method == 'POST':
        ids = request.POST.get('ids')
        firstname = request.POST.get('firstname')
        middlename = request.POST.get('middlename')
        lastname = request.POST.get('lastname')
        address = request.POST.get('address')
        cpnumber = request.POST.get('cpnumber')
        birthday = request.POST.get('birthday')
        age = request.POST.get('age')
        civil = request.POST.get('civil')
        email = request.POST.get('email')
        idnumber = request.POST.get('idnumber')
        status =request.POST.get('status')
        field = request.POST.get('field')
        platoons = request.POST.get('platoons')
        section2 = request.POST.get('section')
        nfather = request.POST.get('nfather')
        foccupation = request.POST.get('foccupation')
        nmother = request.POST.get('nmother')
        moccupation  = request.POST.get('moccupation')
        pcontact = request.POST.get('pcontact')
        nguardian = request.POST.get('nguardian')
        goccupation = request.POST.get('goccupation')
        gcontact = request.POST.get('gcontact')
        sources_income = request.POST.get('sources_income')
        monthly_income = request.POST.get('monthly_income')
        start = request.POST.get('start')
        end = request.POST.get('end')
       
        extenduser.objects.filter(id=ids).update(firstname = firstname, middlename = middlename, lastname = lastname, 
                                                 address = address, cpnumber=cpnumber, birthday=birthday, age=age,
                                                 civil=civil,email=email,idnumber=idnumber,status=status,field=field,
                                                 platoons=platoons, section=section2,nfather=nfather, foccupation=foccupation, nmother=nmother, moccupation=moccupation,
                                                 pcontact=pcontact, nguardian=nguardian, goccupation=goccupation, gcontact=gcontact, sources_income=sources_income, monthly_income=monthly_income, start=start, end=end)
        User.objects.filter(id=ids).update(username=idnumber)
   
        messages.success(request, str(idnumber)+' has been Updated')
        # return redirect('/create_platoon_page')
        return redirect(request.META['HTTP_REFERER'])

    return redirect('/care_of')



def send_message(request):
    date_time = dt.datetime.now() 
    if request.method == 'POST':
       name = request.POST.get('name2')
       email = request.POST.get('email')
       subject = request.POST.get('subject')
       message = request.POST.get('message')
       datas = feedbacks(sender=name, email=email, date_sent=date_time, subject=subject, message=message)
       datas.save()
    return redirect('/contact_us')


def update_mess(request):
    if request.method == 'POST':
        action_date = dt.datetime.now() 
        actionby = request.POST.get('action')
        ids = request.POST.get('ids')
        status = request.POST.get('status')

        feedbacks.objects.filter(id=ids).update(status = status, action_by = actionby, action_date=action_date)
        

    return redirect('/admin_dashboard')


def send_response(request, id):
    feed = feedbacks.objects.filter(status = 'PENDING').order_by('date_sent')
    audience = sections.objects.all()
    ann = Announcement.objects.all()
    sy = school_year.objects.all()
    nav_pending_count = extenduser.objects.filter(status='PENDING').count()
    nav_rejected_count = extenduser.objects.filter(status='REJECTED').count()
    active = extenduser.objects.filter(status='ENROLLED').count()
    pending = extenduser.objects.filter(status='PENDING').count()

   

    id = id
    
    details = feedbacks.objects.filter(id=id)
    
    context = {
        'id': id,
        'details': details,
        'active':active,   
        'pending':pending,
        'sy':[sy.last()],
        'audience':audience,
        'ann':ann,
        # 'staff':staff,
        'nav_pending_count':nav_pending_count,
        'nav_rejected_count':nav_rejected_count ,
        'feed':feed
    }
    return render(request, 'activities/popup.html', context)


def response(request):
    if request.method == 'POST':
        try:
            sub = request.POST.get('emailtext')
            msg = request.POST.get('message')
            email = request.POST.get('email')
            send_mail(sub, msg,'tupc.nstp@gmail.com',[email])
            return redirect('/admin_dashboard')
        except ImportError:
            messages.success(request, 'Email Encountered some errors. Please Contact your Administrator')
    return redirect('/admin_dashboard')

def mess_history(request):
    details = feedbacks.objects.filter(status = 'DONE')
    context = {
        'details':details,
    }
    return render(request, 'activities/history.html', context)





# def export1(request):
#     if request.method == 'POST':
#         pdf = extenduser.objects.get(school=request.POST.get('school'))
#         response = FileResponse(pdf.pdf_file, content_type='application/pdf')
#         response['Content-Disposition'] = f'attachment; filename={pdf.file_name}.pdf'
#         return response

from reportlab.lib import pagesizes

def export1(request):
    # Create a file-like buffer to receive PDF data.
    buffer = io.BytesIO()

    # Create the PDF object, using the buffer as its "file."
    # p = canvas.Canvas(buf, pagesize=letter,bottomup=0)
    page_size = pagesizes.letter
    p = canvas.Canvas(buffer, pagesize=page_size)
    
    # textob = p.beginText()
    # textob.setTextOrigin(inch, inch)
    # textob.setFont('Helvetica',13)
    school = request.POST.get('school')
    students = extenduser.objects.filter(school=school)
    p.drawString(20, 720, "School:"+ school)
    lines =[
        ['Fullname',  'Scholarship category', 'IP Status', 'Care of', 'Start of Subsidy', 'End of Subsidy'],
    ]
    
    for s in students:
        lines.append([s.firstname + ' ' + s.lastname,  s.category, s.ip_status + ' ' + s.ip_category, s.care_of, s.start, s.end])

    # for line in lines:
    #     textob.textLine(line)
        
    table = Table(lines)
    table.setStyle(TableStyle([
       ('BACKGROUND', (0, 0), (-1, 0), (0, 0, 0, 1)),
        ('TEXTCOLOR', (0, 0), (-1, 0), (1, 1, 1)),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), (0.98, 0.98, 0.98)),
        ('GRID', (0, 0), (-1, -1), 1, (0.75, 0.75, 0.75))
    ]))

    # p.build([table])
        
    table.wrapOn(p, page_size[0], page_size[1])
    table.drawOn(p, 20, 650)
    p.save()
    buffer.seek(0)
    
    return FileResponse(buffer, as_attachment=True, filename='List.pdf')
    

    # Draw things on the PDF. Here's where the HTML table is rendered.
   