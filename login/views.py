from django.shortcuts import render, redirect
from .forms import SignUpForm, OTPForm, LoginForm, ForgotForm, ResetForm, EditAccountForm
from .models import Accounts, Users
from django.core.mail import EmailMessage
from django.contrib import messages
from django.utils.crypto import get_random_string
from datetime import datetime, timedelta
from django.utils import timezone
from .backends import MyAuthBackend
from upload.models import Items, Products, Licence, Settings
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
import json
from bson import json_util
from whatif.decorators import check_login

# @check_login
def dashboard(request):
    if not request.session.get('user'):
        return redirect('login')
    user = Accounts.get_user_details(request.session.get('user'))
    userid = Users.get_userid(request.session.get('user'))
    items = Items.objects.filter(UserId=userid).count()
    sub_depts = Products.objects.order_by('SubDeptName').filter(UserId=userid).values('SubDeptName').distinct()
    storeids = Products.objects.order_by('StoreId').filter(UserId=userid).values('StoreId').distinct()
    category = Products.objects.order_by('CategoryName').filter(UserId=userid).values('CategoryName').distinct()
    productname = Products.objects.order_by('Name').filter(UserId=userid).values('Name').distinct()
    upcnumber = Products.objects.order_by('UPC').filter(UserId=userid).values('UPC').distinct()
    licencetab = Licence.objects.values().get(UserId=userid)
    request.session['licence'] = json.dumps(licencetab, default=lambda o: o.isoformat() if hasattr(o, 'isoformat') else o)
    rule_set = Settings.objects.get(UserId=userid)
    productlist = Products.objects.filter(UserId=userid).values()
    records = len(productlist)
    counter1 = 0
    for i in productlist:
        if i['FirstCompPrice'] == '':
            counter1 += 1
    counter2 = 0
    for i in productlist:
        if i['SecondCompPrice'] == '':
            counter2 += 1
    counter3 = 0
    for i in productlist:
        if i['ThirdCompPrice'] == '':
            counter3 += 1
    competitor = False if [records,records,records]==[counter1,counter2,counter3] else True
    if competitor and licencetab['CompetitorFeatured']:
        title= 'PRODUCT PRICE INDEX'
        red, yel, green = (0,0,0)
        if rule_set.MinCompPrice:
            mincompprice = (100 - rule_set.MinCompPrice)/100;
        else:
            mincompprice = 0.9;
        if rule_set.MinCompPrice:
            maxcompprice = (100 + rule_set.MaxCompPrice)/100;
        else:
            maxcompprice = 1.1;
        for p in productlist:
            min_range = float(p['ProductPrice']) * mincompprice
            max_range = float(p['ProductPrice']) * maxcompprice
            if p['FirstCompPrice'] and p['FirstCompPrice'] != '-NA-':
                if float(p['FirstCompPrice']) < min_range:
                    red += 1
                elif float(p['FirstCompPrice']) > max_range:
                    green +=1
                elif min_range < float(p['FirstCompPrice']) < max_range:
                    yel +=1
                else:
                    pass
            if p['SecondCompPrice'] and p['SecondCompPrice'] != '-NA-':
                if p['SecondCompPrice'] and float(p['SecondCompPrice']) < min_range:
                    red += 1
                elif p['SecondCompPrice'] and float(p['SecondCompPrice']) > max_range:
                    green +=1
                elif min_range < float(p['SecondCompPrice']) < max_range:
                    yel +=1
            if p['ThirdCompPrice'] and p['ThirdCompPrice'] != '-NA-':
                if p['ThirdCompPrice'] and float(p['ThirdCompPrice']) < min_range:
                    red += 1
                elif p['ThirdCompPrice'] and float(p['ThirdCompPrice']) > max_range:
                    green +=1
                elif min_range < float(p['ThirdCompPrice']) < max_range:
                    yel +=1
        pie_data = [{
            'name': 'Price Index Low',
            'y': green,
            'color': '#a6f685',
        }, {
            'name': 'Price Index Mid',
            'y': yel,
            'color': '#f4b908',

        }, {
            'name': 'Price Index High',
            'y': red,
            'color': '#f99192',
        }]
    else:
        subdept = list(Products.objects.values('SubDeptNumber','SubDeptName').filter(UserId=userid).distinct())
        pie_data = []
        for i in subdept:
            data = {}
            data['name'] = i['SubDeptName']
            data['y'] = Items.objects.filter(ICategoryNumber__startswith=i['SubDeptNumber'][1:]).count()
            pie_data.append(data)
        title = 'SUBDEPARTMENT COMPOSITION'
    context = {'rule_set': rule_set, 'user':user, 'items':items,  'sub_depts': sub_depts, 'storeids': storeids, 'category': category,
               'upcnumber': upcnumber, 'productname': productname, 'licencetab': licencetab, 'pie_title': title,
               'pie_data': json.dumps(pie_data)}
    return render(request, 'dashboard.html', context)

def ajax_dashboard(request):
    name = request.GET.get('product_name', None)
    upc = request.GET.get('UPC', None)
    sub_dept = request.GET.get('sub_dept', None)
    store_id = request.GET.get('store_id', None)
    category = request.GET.get('category', None)
    userid = Users.get_userid(email_id=request.session.get('user'))
    a = {}
    if userid:
        a['UserId'] = userid
    if not name == "":
        a['Name__icontains']= name
    if not upc == "":
        a['UPC__endswith'] = upc
    if not sub_dept == "SUB DEPARTMENT":
        a['SubDeptName'] = sub_dept
    if not store_id == "STORE ID":
        a['StoreId'] = store_id
    if not category == "CATEGORY":
        a['CategoryName'] = category
    print(a)
    productlist = Products.objects.order_by('Name').values('id','Name','UPC','ProductPrice','SubDeptName','CategoryName','FirstCompPrice',
                                                           'SecondCompPrice','ThirdCompPrice').filter(**a).distinct()
    records = len(productlist)
    print(records)
    counter1=0
    for i in productlist:
        if i['FirstCompPrice'] == '':
            counter1 += 1
    counter2=0
    for i in productlist:
        if i['SecondCompPrice'] == '':
            counter2 += 1
    counter3 = 0
    for i in productlist:
        if i['ThirdCompPrice'] == '':
            counter3 += 1
    data = {
        'products': list(productlist),
        'competitor': False if [records,records,records]==[counter1,counter2,counter3] else True,
        'search': True
    }
    print(data)
    return JsonResponse(data)

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            token = get_random_string(length=6, allowed_chars='1234567890')
            reg_token={}
            reg_token['token'] = token
            reg_token['timestamp'] = str(timezone.now())
            request.session['reg_token'] = reg_token
            mail_subject = 'What-If registration OTP.'
            message = 'Your OTP for What-If registration is ' + token
            to_email = form.cleaned_data.get('email_id')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            account = {}
            account['CompanyName'] = form.cleaned_data['company_name']
            account['ContactPerson'] = form.cleaned_data['contact_person']
            account['Email'] = form.cleaned_data['email_id']
            account['PhoneNumber'] = form.cleaned_data['phone_number']
            account['Country'] = form.cleaned_data['country']
            request.session['account'] = account
            user_reg = {}
            user_reg['EmailId'] = form.cleaned_data['email_id']
            user_reg['Password'] = form.cleaned_data['password']
            request.session['user_reg'] = user_reg
            return redirect('otp')
    elif request.session.get('user'):
        messages.success(request, "Your already Signed in!")
        return redirect('/')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def verify_otp(request):
    if not request.session.get('user_reg'):
        return redirect('signup')
    if request.method == 'POST':
        form = OTPForm(request.POST)
        if form.is_valid():
            otp = form.cleaned_data['otp']
            reg_token = request.session['reg_token']
            print(otp)
            print(reg_token['token'])
            print(reg_token['timestamp'])
            print(str(timezone.now()))
            if str(timezone.now() - timedelta(seconds=900)) < reg_token['timestamp']:
                if otp == reg_token['token']:
                    user_detail = request.session['user_reg']
                    account = request.session['account']
                    acc = Accounts(**account)
                    acc.save()
                    user = Users()
                    user.EmailId = user_detail['EmailId']
                    user.PasswordEncrypted = Users.set_password(Users,raw_password=user_detail['Password'])
                    acc = Accounts.get_user_details(user_detail['EmailId'])
                    user.AccountId = acc.id
                    user.save()
                    userid = Users.get_userid(user_detail['EmailId'])
                    lic = Licence()
                    lic.UserId = userid
                    lic.save()
                    rule= Settings()
                    rule.UserId = userid
                    rule.save()
                    messages.success(request, "Congratulations! You have successfully registered with What-If. Please login and analyze your products.")
                    return redirect('login')
                else:
                    messages.error(request, "OTP not matching error!")
            else:
                messages.error(request, "OTP has expired!")
        else:
            messages.error(request, "Please enter correct OTP!")
            print(form)
    else:
        form = OTPForm()
    return render(request, 'otp.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        print(form)
        if form.is_valid():
            print("form is valid")
            email_id = form.cleaned_data['email_id']
            password = form.cleaned_data['password']
            ab =MyAuthBackend()
            user = ab.authenticate(request, email=email_id, password=password)
            if user is not None:
                print('auth success')
                user.LastLogin = timezone.now()
                user.save()
                request.session['user'] = user.EmailId
                return redirect('/')
            else:
                messages.error(request, "This Email or Password does not exist")
    elif request.session.get('user'):
        print(request.session['user'])
        return redirect('dashboard')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def forgot_password(request):
    if request.method == 'POST':
        form = ForgotForm(request.POST)
        print(form)
        if form.is_valid():
            email_id = form.cleaned_data['email_id']
            if Users.objects.filter(EmailId=email_id).exists():
                print("User exist")
                token = get_random_string(length=6, allowed_chars='1234567890')
                reg_token={}
                print(token)
                reg_token['token'] = token
                reg_token['timestamp'] = str(timezone.now())
                request.session['reg_token'] = reg_token
                mail_subject = 'whatif forgot password OTP.'
                message = 'OTP for password Reset ' + token
                to_email =form.cleaned_data.get('email_id')
                print(to_email)
                email = EmailMessage(
                    mail_subject, message, to=[to_email])
                email.send()
                request.session['reset_useremail']=to_email
                return redirect('otp_verification')
            else:
                messages.error(request, "Incorrect Email")
    else:
        form = ForgotForm()
    return render(request, 'forgot.html', {'form': form})


def otp_verification(request):
    if not request.session.get('reset_useremail'):
        return redirect('forgot_password')
    if request.method == 'POST':
        form = OTPForm(request.POST)
        print('here')
        print(form)
        if form.is_valid():
            otp = form.cleaned_data['otp']
            reg_token = request.session['reg_token']
            print(reg_token['timestamp'])
            print(str(timezone.now()))
            if str(timezone.now() - timedelta(seconds=900)) < reg_token['timestamp']:
                print('intime')
                if str(otp) == reg_token['token']:
                    print('tokenmatch')
                    request.session['reset_token'] = 'verified'
                    return redirect('reset_password')
                else:
                    messages.error(request, "invalid OTP")
            else:
                messages.error(request, "Timeout")
        else:
            messages.error(request, "Incorrect OTP")
    else:
        form = OTPForm()
    return render(request, 'otp.html')


def reset_password(request):
    if not request.session.get('reset_token'):
        return redirect('forgot_password')
    if request.method == 'POST':
        form = ResetForm(request.POST)
        print(form)
        if form.is_valid():
            password = form.cleaned_data.get("password")
            confirm_password = form.cleaned_data.get("confirm_password")
            useremail = request.session['reset_useremail']
            user = Users.objects.get(EmailId=useremail)
            if user:
               user.PasswordEncrypted = user.set_password(raw_password=form.cleaned_data['password'])
               user.save()
               return redirect('login')
            else:
                messages.error(request, "invalid password")
        else:
            messages.error(request, "invalid password")
    else:
        form = ResetForm()
    return render(request, 'reset.html', {'form': form})


def logout(request):
    request.session.flush()
    return redirect('login')

def profile(request):
    if not request.session.get('user'):
        return redirect('login')
    acc = Accounts.get_user_details(request.session.get('user'))
    form = EditAccountForm(initial={'contact_person': acc.ContactPerson, 'company_name': acc.CompanyName, 'email_id':acc.Email,
                                    'phone_number': acc.PhoneNumber, 'country': acc.Country, 'state': acc.State, 'address': acc.Address,
                                    'zipcode': acc.Zip})
    context = {
        "form": form
    }
    return render(request,'profile.html', {'acc': acc}, context)

def editaccount(request):
    if not request.session.get('user'):
        return redirect('login')
    acc = Accounts.get_user_details(request.session.get('user'))
    form = EditAccountForm(request.POST or None, initial={'contact_person': acc.ContactPerson, 'company_name': acc.CompanyName,
                                                          'email_id':acc.Email, 'phone_number':acc.PhoneNumber, 'country': acc.Country,
                                                          'state': acc.State, 'address': acc.Address, 'zip_code': acc.Zip})
    if request.method == 'POST':
        if form.is_valid():
            acc.ContactPerson = request.POST['contact_person']
            acc.CompanyName = request.POST['company_name']
            acc.Email = request.POST['email_id']
            acc.PhoneNumber = request.POST['phone_number']
            acc.Country = request.POST['country']
            acc.State = request.POST['state']
            acc.Address = request.POST['address']
            acc.Zip = request.POST['zip_code']
            acc.save()
            if len(request.POST['password']) != 0:
                user = Users.objects.get(EmailId=request.session.get('user'))
                user.PasswordEncrypted = Users.set_password(Users, raw_password=request.POST['password'])
                user.save()
            return HttpResponseRedirect('%s' % (reverse('profile')))
    context = {
        "form": form
    }
    return render(request, 'editaccount.html', context)

