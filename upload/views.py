from django.shortcuts import render, redirect, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib import messages
from .forms import CategoryForm, SettingsForm, SearchForm, PromoSearchForm, ExecutionSearchForm
from .models import Category, Details, Promotions, Display, Region, Location, Type
import logging
from django.utils import timezone
import pytz
from dateutil.parser import parse
from login.models import Users
from .models import Products, Settings, Items, Category, SalesForecast, ProductHistory, Seasonality, PromotionTierRule, CompetitorTierRule
from itertools import chain
import itertools
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from django.http import HttpResponseRedirect, JsonResponse
import json
from operator import itemgetter, attrgetter
from django.db.models import Count, Max, Sum, Avg
from .excel_utils import WriteToExcel


def upload_csv(request):
    if not request.session.get('user'):
        return redirect('login')
    data = {}
    if "GET" == request.method:
        return render(request, "upload_csv.html", data)
    # if not GET, then proceed
    try:
        csv_file = request.FILES["csv_file"]
        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'File is not CSV type')
            return HttpResponseRedirect(reverse("upload_csv"))
        if csv_file.size > 1000000:
            messages.error(request, "Uploaded file more than 10 MB (%.2f MB)." % (csv_file.size / (1000 * 1000),))
            return HttpResponseRedirect(reverse("upload_csv"))
        # if file is too large, return
        if csv_file.multiple_chunks():
            messages.error(request, "Uploaded file is too big (%.2f MB)." % (csv_file.size / (1000 * 1000),))
            return HttpResponseRedirect(reverse("upload_csv"))

        file_data = csv_file.read().decode("utf-8")

        lines = file_data.split("\r\n")
        # loop over the lines and save them in db. If error , store as string and then display
        header = lines[0].split(",")
        #print(header)
        #print(lines)
        result = []
        for line in lines[1:len(lines)-1]:
            fields = line.split(",")
            data_dict = {}
            for i, j in zip(header, fields):
                data_dict[i] = j
            result.append(data_dict)
        try:
            for data_dict in result:
                form = CategoryForm(data_dict)
                print(data_dict)
                if form.is_valid():
                   form.save()
                else:
                     logging.getLogger("error_logger").error(form.errors.as_json())
            messages.success(request, "Successfully uploaded the file.")
        except Exception as e:
             logging.getLogger("error_logger").error(repr(e))
             pass

    except Exception as e:
        logging.getLogger("error_logger").error("Unable to upload file. " + repr(e))
        messages.error(request, "Unable to upload file. " + repr(e))

    return HttpResponseRedirect(reverse("upload_csv"))


def whatifsearch(request):
    if not request.session.get('user'):
        return redirect('login')
    firststore = Products.objects.order_by('StoreId').values_list('StoreId', flat=True).distinct().first()
    userid = Users.get_userid(request.session.get('user'))
    productslist = Products.objects.order_by('Name').filter(UserId=userid).values('id','Name','UPC','ProductPrice','CategoryName','SubDeptName').filter(StoreId=firststore, UserId=userid).distinct()
    store = Products.objects.order_by('StoreId').filter(UserId=userid).values('StoreId').distinct()
    categoryname = Products.objects.order_by('CategoryName').filter(UserId=userid).values('CategoryName').distinct()
    subdept = Products.objects.order_by('SubDeptName').filter(UserId=userid).values('SubDeptName').distinct()
    productname = Products.objects.order_by('Name').filter(UserId=userid).values('Name').distinct()
    upcnumber= Products.objects.order_by('UPC').filter(UserId=userid).values('UPC').distinct()
    print (userid)
    if request.method == 'POST':
        form = SearchForm(request.POST)
        print(form)
        if form.is_valid():
            print("form is valid")
            product_name = request.POST['product_name']
            upc = request.POST['upc']
            sub_department = request.POST['sub_department']
            store_id = request.POST['store_id']
            category = request.POST['category']
            print(store_id)
            print(form)
            dict = {}
            if userid:
                dict['UserId'] = userid
            if not product_name=='':
                dict['Name__icontains']=product_name
                print (dict['Name__icontains'])
            else:
                None
            if not upc== '':
                dict['UPC__endswith'] = upc
                print (dict['UPC__endswith'])
            else:
                None
            if not category=='CATEGORY':
                dict['CategoryName']=category
                print (dict['CategoryName'])
            else:
                None
            if not store_id=='STORE ID':
                dict['StoreId']=store_id
                print (dict['StoreId'])
            else:
                None
            if not sub_department=='SUB DEPARTMENT':
                dict['SubDeptName'] = sub_department
                print (dict['SubDeptName'])
            else:
                None
            print(dict)
            productslist = Products.objects.order_by('Name').filter(UserId=userid).values('id','Name','UPC','ProductPrice','CategoryName',
                                                                                          'SubDeptName').filter(**dict).distinct()
        else:
            messages.error(request, "Not Valid")
            print(form)
            productslist = Products.objects.order_by('Name').filter(UserId=userid).values('id','Name', 'UPC', 'ProductPrice', 'CategoryName',
                                                                                          'SubDeptName').distinct()
        print(productslist)
        return render(request, 'what_if_search.html', {'form':form, 'store': store, 'categoryname': categoryname,'subdept': subdept,
                                                       'productname':productname, 'upcnumber':upcnumber, 'productslist':productslist})
    else:
        form = SearchForm()
    return render(request, 'what_if_search.html', {'form':form, 'store':store,'categoryname':categoryname, 'subdept':subdept,
                                                   'productname':productname, 'upcnumber':upcnumber, 'productslist':productslist})

def detailspage(request):
    if not request.session.get('user'):
        return redirect('login')
    productid = request.POST.getlist('my_object[]')
    detailstab = list(Details.objects.values().filter(ProductId=productid[0]))
    product = Products.objects.values().get(id=productid[0])
    print (product)
    return render(request, 'detailspage.html', {'detailstab':detailstab, 'product':product, 'productid':productid})

def priceoptimization(request):
    if not request.session.get('user'):
        return redirect('login')
    if request.method == 'POST':
        if request.POST.getlist('my_object[]'):
            print(request.POST.getlist('my_object[]'))
            productids = request.POST.getlist('my_object[]')
            userid = Users.get_userid(request.session.get('user'))
            rule_set = Settings.objects.get(UserId=userid)
            product_name = []
            tot_price = 0
            tot_cost = 0
            tot_qty = 0
            tot_peod = 0
            item_num = len(productids)
            for id in productids:
                print(id)
                prod = Products.objects.get(id=id)
                print(prod.Name)
                product_name.append(prod.Name)
                tot_price += float(prod.ProductPrice)
                tot_cost += float(prod.Cost)
                tot_qty += float(prod.Quantity)
                tot_peod += float(prod.Peod)
            products={'product_price': tot_price/item_num,
            'product_cost': tot_cost/item_num,
            'product_qty': tot_qty/item_num * 3 * 7,
            'product_peod': tot_peod/item_num,
            'current_profit': (tot_price/item_num - tot_cost/item_num) * tot_qty/item_num * 3 * 7,
            'current_revenue': tot_price/item_num * tot_qty/item_num * 3 * 7
            }
            current_week = int(datetime.now().strftime("%U"))
            arr=[]
            cur_qty = {}
            # my_opt_dict = {}
            for i in range(9):
                arr.append((current_week + 1 + i)%53)
            for i in range(9):
                item_count=0
                for j in productids:
                    record = Products.objects.filter(id=int(j),UserId=userid).values().first()
                    if record['InterceptCoefficient'] not in [0, '']:
                        trend = float(record['InterceptCoefficient']) + float(record['PriceCoefficient']) * float(record['ProductPrice']) + float(record['WeekCoefficient']) * arr[i]
                        seasonIndex = float(Seasonality.objects.filter(ProductId=record['id'],WeekNumber=arr[i],UserId=userid).values().first()['SeasonalityIndex'])
                        quantity = trend * seasonIndex
                        if record['CompetitorIndex'] != '':
                            if float(record['Peod']) < 0.8:
                                Peod_range = "<0.8"
                            elif float(record['Peod']) < 1:
                                Peod_range = "0.8-1"
                            elif float(record['Peod']) < 1.25:
                                Peod_range = "1-1.25"
                            else:
                                Peod_range = ">1.25"
                            print(CompetitorTierRule.objects.filter(CompetitorTier=(record['CompetitorIndex']), PeodRange=Peod_range).values().first())
                            rule = CompetitorTierRule.objects.filter(CompetitorTier=(record['CompetitorIndex']), PeodRange=Peod_range).values().first()['ImpactPercentValue']
                            final_quantity = quantity + quantity * rule
                        else:
                            final_quantity = quantity
                        if arr[i] in cur_qty.keys():
                            cur_qty[arr[i]] = int(cur_qty[arr[i]]) + int(final_quantity)
                            item_count += 1
                        else:
                            cur_qty[arr[i]] = int(final_quantity)
                            item_count += 1
                if item_count != 0:
                    cur_qty[arr[i]] = round(cur_qty[arr[i]]/item_count,0)
            print(cur_qty)
            history = list(ProductHistory.objects.values().filter(ProductId__in=productids,PriceTypeId=1))
            #ordered_history = sorted(history, key=lambda x: datetime.strptime(x['Date'], '%m/%d/%Y'),reverse=False)
            ordered_history = sorted(history, key=lambda x: x['Date'], reverse=False)
            trend_list = []
            for i, d in enumerate(ordered_history):
                if len(trend_list) != 0:
                    if ordered_history[i]['Price'] == trend_list[-1]['Price']:
                        trend_list[-1]['UnitSales'] = float(trend_list[-1]['UnitSales']) + float(ordered_history[i]['UnitSales'])
                        trend_list[-1]['counter'] += 1
                    else:
                        ordered_history[i]['counter'] = 1
                        trend_list.append(ordered_history[i])
                else:
                    ordered_history[i]['counter'] = 1
                    trend_list.append(ordered_history[i])
            categories = []
            price = []
            sales = []
            for j in trend_list:
                categories.append((j['Date']).strftime("%m/%d/%Y"))
                price.append(j['Price'])
                sales.append(round(float(j['UnitSales'])/j['counter'],0))
            return render(request, 'priceoptimization.html', {'categories': json.dumps(categories), 'price': price,
                                                              'sales': sales, 'cur_qty': cur_qty, 'products':products,
                                                              'product_name': product_name, 'rule_set': rule_set, 'productids':productids })
        else:
            return redirect('/')
    return redirect('/')

def ajax_whatif_export(request):
    if request.method=='GET':
        print('entry')
        response = HttpResponse(content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename=Report.xlsx'
        pricing_data = ""
        product = "Alessi"
        xlsx_data = WriteToExcel(pricing_data, product)
        response.write(xlsx_data)
        return response


def setting(request):
    if not request.session.get('user'):
        return redirect('login')
    user = Users.objects.get(EmailId= request.session.get('user'))
    try:
        rule = Settings.objects.get(UserId = user.id)
        form = SettingsForm(request.POST or None, initial={'ending_number': rule.EndingNumber, 'min_comp_price': rule.MinCompPrice,
                            'max_comp_price': rule.MaxCompPrice, 'min_price': rule.MinPriceChangeLimits, 'max_price': rule.MaxPriceChangeLimits,
                            'min_margin': rule.MinMargin, 'max_margin': rule.MaxMargin, 'min_volume': rule.MinVolumeChangeLimits,
                            'max_volume': rule.MaxVolumeChangeLimits})
    except Settings.DoesNotExist:
        rule = Settings()
        form = SettingsForm()
    if request.method == 'POST':
        form = SettingsForm(request.POST)
        if form.is_valid():
            rule.EndingNumber = form.cleaned_data['ending_number']
            rule.MinCompPrice = form.cleaned_data['min_comp_price']
            rule.MaxCompPrice = form.cleaned_data['max_comp_price']
            rule.MinPriceChangeLimits = form.cleaned_data['min_price']
            rule.MaxPriceChangeLimits = form.cleaned_data['max_price']
            rule.MinMargin = form.cleaned_data['min_margin']
            rule.MaxMargin = form.cleaned_data['max_margin']
            rule.MinVolumeChangeLimits = form.cleaned_data['min_volume']
            rule.MaxVolumeChangeLimits = form.cleaned_data['max_volume']
            rule.ModifiedDate = timezone.now()
            rule.UserId = user.id
            rule.save()
            return redirect('/')
    return render(request, 'setting.html',{'form':form})

def categorydisplay(request):
    subdept = request.GET.get('SubDeptName')
    data= {'categoryname' : list(Products.objects.filter(SubDeptName__icontains=subdept).order_by('SubDeptName').values_list('CategoryName' , flat=True).distinct())}
    # print(data)
    return JsonResponse(data)



def promotion(request):
    if not request.session.get('user'):
        return redirect('login')
    userid = Users.get_userid(request.session.get('user'))
    items = Items.objects.filter(UserId=userid).count()
    storepromo = Products.objects.order_by('StoreId').filter(UserId=userid).values('StoreId').distinct()
    categorynamepromo = Products.objects.order_by('CategoryName').filter(UserId=userid).values('CategoryName').distinct()
    subdeptpromo = Products.objects.order_by('SubDeptName').filter(UserId=userid).values('SubDeptName').distinct()
    productnamepromo = Products.objects.order_by('Name').filter(UserId=userid).values('Name').distinct()
    upcnumberpromo= Products.objects.order_by('UPC').filter(UserId=userid).values('UPC').distinct()
    promotypedip= Promotions.objects.order_by('PromotionType').filter(UserId=userid).values('PromotionType').distinct()
    # promotionnamedip = Promotions.objects.order_by('PromotionName').filter(UserId=userid).values('PromotionName').distinct()
    if request.method == 'POST':
        form = PromoSearchForm(request.POST)
        if form.is_valid():
            name = request.POST.get('product_name', None)
            upc = request.POST.get('upc', None)
            sub_dept = request.POST.get('sub_department', None)
            store_id = request.POST.get('store_id', None)
            category = request.POST.get('category', None)
            promotype = request.POST.get('promotype', None)
            # promotionname = request.POST.get('promotionname', None)
            startdate = request.POST.get('startdate', None)
            enddate = request.POST.get('enddate', None)
            nb1_newprice_percent = request.POST.get('nb1_newprice', '')
            print('newprice', nb1_newprice_percent)
            userid = Users.get_userid(email_id=request.session.get('user'))
            selecteddict = {}
            if userid:
                selecteddict['UserId'] = userid
            if not name=='':
                selecteddict['Name']=name
            if not upc== '':
                selecteddict['UPC_NAME'] = list(Products.objects.filter(UPC=upc)[0:1].values_list('Name' ,flat=True))[0]
            if not category=='CATEGORY':
                selecteddict['CategoryName']=category
            if not store_id=='STORE ID':
                selecteddict['StoreId']=store_id
            # print(selecteddict)
            a = {}
            if userid:
                a['UserId'] = userid
            if not name == "":
                a['Name'] = name
            if not upc == "":
                a['UPC__endswith'] = upc
            if not sub_dept == "SUB DEPARTMENT":
                a['SubDeptName'] = sub_dept
            if not store_id == "STORE ID":
                a['StoreId'] = store_id
            if not category == "CATEGORY":
                a['CategoryName'] = category
            # print(a)
            productids = list(Products.objects.filter(**a).values_list('id', flat=True))
            # print(productids)
            product_info = Products.objects.filter(id__in=productids).values().first()
            b = {}
            if userid:
                b['UserId'] = userid
            if productids != None:
                b['ProductId__in'] = productids
            if startdate and enddate:
                utc_startdate = pytz.utc.localize(datetime.strptime(startdate,"%d-%b-%Y"))
                utc_enddate = pytz.utc.localize(datetime.strptime(enddate, "%d-%b-%Y"))
                b['StartDate__lte'] = utc_enddate
            if startdate and enddate:
                utc_startdate = pytz.utc.localize(datetime.strptime(startdate, "%d-%b-%Y"))
                utc_enddate = pytz.utc.localize(datetime.strptime(enddate, "%d-%b-%Y"))
                b['EndDate__gte'] = utc_startdate
            if not promotype == "PROMOTION TYPE":
                b['PromotionType'] = promotype
            # if not promotionname == "PROMOTION NAME":
            #     b['PromotionName'] = promotionname
            promo = Promotions.objects.values().filter(**b)
            # print(b)
            #print(promo)
            highlights={}
            if promo:
                BICLoc = promo.values_list('BICLocation', flat=True).annotate(BICLoc=Count('BICLocation')).order_by(
                    '-BICLoc').first()
                BICTy = promo.values_list('BICType', flat=True).annotate(BICTy=Count('BICType')).order_by('-BICTy').first()
                item_count = len(promo)
                tot_acvwopromo = 0
                tot_acvwpromo = 0
                tot_saleslift = 0
                tot_promospend = 0
                for p in promo:
                    tot_acvwopromo += float(p['SalesWithoutPromo'])
                    tot_acvwpromo += float(p['SalesWithPromo'])
                    tot_saleslift += float(p['SalesLift'])
                    if p['PromotionSpend'] != '':
                        tot_promospend += float(p['PromotionSpend'])
                highlights = {'acvwopromo': round(tot_acvwopromo),
                              'acvwpromo': round(tot_acvwpromo),
                              'saleslift': round(tot_saleslift / item_count),
                              'promospend': round(tot_promospend),
                              'BICLoc': BICLoc,
                              'BICTy': BICTy,
                              }
            promo_period = []
            for j in promo:
                period = {}
                period['StartDate'] = j['StartDate'].strftime("%Y-%m-%d")
                period['EndDate'] = j['EndDate'].strftime("%Y-%m-%d")
                period['PromotionType'] = j['PromotionType']
                period['PromotionName'] = j['PromotionName']
                promo_period.append(period)
            # print(promo_period)
            ordered_promo_period = sorted(promo_period, key=lambda x: x['StartDate'], reverse=False)
            # print(ordered_promo_period)
            avgplotband = []
            for j in promo:
                plotband = {}
                plotband['EndDate'] = j['EndDate'].strftime("%Y-%m-%d")
                plotband['StartDate'] = j['StartDate'].strftime("%Y-%m-%d")
                plotband['saleslift'] = round(float(j['SalesLift']))
                # print(plotband)
                #print(j)
                promosales = ProductHistory.objects.values().filter(ProductId__in=productids,Date__gte=j['StartDate'], Date__lte=j['EndDate'])
                print(promosales)
                salesqty = 0
                revenue = 0
                saleslength = len(promosales)
                print(saleslength)
                for item in promosales:
                    # print (item)
                    salesqty += float(item["UnitSales"])
                    revenue += (float(item['UnitSales'])*float(item['Price']))
                plotband['salesqty']=round(salesqty/saleslength)
                plotband['revenue']=round(revenue/saleslength)
                avgplotband.append(plotband)
                # print(plotband)
            print(avgplotband)
            # avgplot = ProductHistory.objects.values().filter(Date__range=[utc_startdate, utc_enddate])
            c = {}
            if userid:
                c['UserId'] = userid
            # if productids:
            #     c['ProductId__in'] = productids
            if startdate:
                utc_startdate = pytz.utc.localize(datetime.strptime(startdate, "%d-%b-%Y"))
                c['Date__gte'] = utc_startdate
            if enddate:
                utc_enddate = pytz.utc.localize(datetime.strptime(enddate, "%d-%b-%Y"))
                c['Date__lte'] = utc_enddate
            # print(c)
            sales = ProductHistory.objects.values().filter(**c)
            # print(sales)
            sales_data = {}
            for i in productids:
                product_sales= sales.filter(ProductId=i).values()
                if product_sales:
                    for j in product_sales:
                        if j['Date'] in sales_data.keys():
                            sales_data[j['Date']][0] += int(j['UnitSales'])
                            sales_data[j['Date']][1] += 1
                            sales_data[j['Date']][2] += float(j['Price'])
                        else:
                            sales_data[j['Date']] = [int(j['UnitSales']), 1, float(j['Price'])]
            sd ={}
            for k,v in sales_data.items():
                sd[k.strftime("%Y-%m-%d")] = [round(v[0] / v[1], 0), round(v[2] / v[1], 2)]
            # print(sd)
            ordered_sd = sorted(sd.items(), key=lambda x: datetime.strptime(x[0], "%Y-%m-%d"), reverse=False)
            # print(ordered_sd)
            base_sales = {}
            for i in productids:
                product_base = Seasonality.objects.filter(ProductId=i, UserId= userid).values()
                if product_base:
                    dates = [k for k in sd.keys()]
                    # print(dates)
                    for j in dates:
                        # print(j)
                        if j in base_sales.keys():
                            base_sales[j][0] += float(product_base.filter(WeekNumber=int((datetime.strptime(j,"%Y-%m-%d")).strftime("%V"))).values().first()['BaselineSales'])
                            base_sales[j][1] += 1
                        else:
                            base_sales[j] = [float(product_base.filter(WeekNumber=int((datetime.strptime(j,"%Y-%m-%d")).strftime("%V"))).values().first()['BaselineSales']),1]
            bs = {}
            for k, v in base_sales.items():
                bs[k] = [round(v[0] / v[1], 0)]
            ordered_bs = sorted(bs.items(), key=lambda x: datetime.strptime(x[0], "%Y-%m-%d"), reverse=False)
            d = {}
            if userid:
                d['UserId'] = userid
            if productids != None:
                d['ProductId__in'] = productids
            if not promotype == "PROMOTION TYPE":
                d['PromotionType'] = promotype
            promo_fc = {}
            promo_names = list(Promotions.objects.values_list('id', 'PromotionType', 'PromotionName', 'PromotionIndex', 'PromotionPrice').filter(**d))
            # print(promo_names)
            current_week_date = datetime.now().date() - timedelta(days=datetime.now().date().weekday()) + timedelta(days=5)
            arr = []
            for i in range(9):
                arr.append(current_week_date + timedelta(days=7 * i))
            product = Products.objects.values().filter(id__in=productids, UserId=userid)
            ordered_product = sorted(product, key=lambda x: x['id'], reverse=False)
            for p in promo_names:
                inner_fc_dict = {}
                if p[2] in promo_fc.keys():
                    for i in ordered_product:
                        if i['InterceptCoefficient'] != '':
                            for j in arr:
                                if i['NB1_PriceCoefficient'] != '':
                                    old_price = Products.objects.filter(id=i['NB1_ProductId']).values().first()['ProductPrice']
                                    if nb1_newprice_percent != '':
                                        NB1_price = float(old_price) + float(old_price) * float(nb1_newprice_percent) * 0.01
                                    else:
                                        NB1_price = old_price
                                    trend = float(i['InterceptCoefficient']) + float(i['PriceCoefficient']) * float(p[4]) + float(i['PromoIndexCoefficient']) * p[3] + float(i['WeekCoefficient']) * int(j.strftime('%U')) + float(i['NB1_PriceCoefficient']) * float(NB1_price) + float(i['NB1_PromoCoefficient']) * float(0)
                                else:
                                    trend = float(i['InterceptCoefficient']) + float(i['PriceCoefficient']) * float(p[4]) + float(i['PromoIndexCoefficient']) * p[3] + float(i['WeekCoefficient']) * int(j.strftime('%U'))
                                seasonIndex = float(Seasonality.objects.filter(ProductId=i['id'], WeekNumber=int(j.strftime('%U')), UserId=userid).values().first()['SeasonalityIndex'])
                                quantity = trend * seasonIndex
                                rule = PromotionTierRule.objects.filter(PromotionIndexTier= p[3], PromotionType =p[1]).values().first()['ImpactPercentValue']
                                promo_quantity = quantity + quantity * rule
                                if i['CompetitorIndex'] != '':
                                    if float(i['Peod']) < 0.8:
                                        Peod_range = "<0.8"
                                    elif float(i['Peod']) < 1:
                                        Peod_range = "0.8-1"
                                    elif float(i['Peod']) < 1.25:
                                        Peod_range = "1-1.25"
                                    else:
                                        Peod_range = ">1.25"
                                    rule = CompetitorTierRule.objects.filter(CompetitorTier =(i['CompetitorIndex']),PeodRange=Peod_range).values().first()['ImpactPercentValue']
                                    final_quantity = promo_quantity + promo_quantity * rule
                                else:
                                    final_quantity = promo_quantity
                                promo_fc[p[2]][0][j.strftime("%Y-%m-%d")] += round(final_quantity)
                        promo_fc[p[2]][1] += 1
                else:
                    for i in ordered_product:
                        if i['InterceptCoefficient'] != '':
                            for j in arr:
                                if i['NB1_PriceCoefficient'] != '':
                                    old_price = Products.objects.filter(id=i['NB1_ProductId']).values().first()['ProductPrice']
                                    if nb1_newprice_percent != '':
                                        NB1_price = float(old_price) + float(old_price) * float(nb1_newprice_percent) * 0.01
                                    else:
                                        NB1_price = old_price
                                    trend = float(i['InterceptCoefficient']) + float(i['PriceCoefficient']) * float(p[4]) + float(i['PromoIndexCoefficient']) * p[3] + float(i['WeekCoefficient']) * int(j.strftime('%U')) + float(i['NB1_PriceCoefficient']) * float(NB1_price) + float(i['NB1_PromoCoefficient']) * float(0)
                                else:
                                    trend = float(i['InterceptCoefficient']) + float(i['PriceCoefficient']) * float(p[4]) + float(i['PromoIndexCoefficient']) * p[3] + float(i['WeekCoefficient']) * int(j.strftime('%U'))
                                seasonIndex = float(Seasonality.objects.filter(ProductId=i['id'], WeekNumber=int(j.strftime('%U')), UserId=userid).values().first()['SeasonalityIndex'])
                                quantity = trend * seasonIndex
                                rule = PromotionTierRule.objects.filter(PromotionIndexTier=p[3], PromotionType=p[1]).values().first()['ImpactPercentValue']
                                promo_quantity = quantity + quantity * rule
                                if i['CompetitorIndex'] != '':
                                    if float(i['Peod']) < 0.8:
                                        Peod_range = "<0.8"
                                    elif float(i['Peod']) < 1:
                                        Peod_range = "0.8-1"
                                    elif float(i['Peod']) < 1.25:
                                        Peod_range = "1-1.25"
                                    else:
                                        Peod_range = ">1.25"
                                    rule = CompetitorTierRule.objects.filter(CompetitorTier =(i['CompetitorIndex']),PeodRange=Peod_range).values().first()['ImpactPercentValue']
                                    final_quantity = promo_quantity + promo_quantity * rule
                                else:
                                    final_quantity = promo_quantity
                                inner_fc_dict[j.strftime("%Y-%m-%d")] = round(final_quantity)
                        if inner_fc_dict:
                            promo_fc[p[2]] = [inner_fc_dict,1]
            inner_fc_dict = {}
            for i in ordered_product:
                if i['InterceptCoefficient'] != '':
                    for j in arr:
                        if i['NB1_PriceCoefficient'] != '':
                            old_price = Products.objects.filter(id=i['NB1_ProductId']).values().first()['ProductPrice']
                            if nb1_newprice_percent != '':
                                NB1_price = float(old_price) + float(old_price) * float(nb1_newprice_percent) * 0.01
                            else:
                                NB1_price = old_price
                            trend = float(i['InterceptCoefficient']) + float(i['PriceCoefficient']) * float(i['ProductPrice']) + float(i['PromoIndexCoefficient']) * 0 + float(i['WeekCoefficient']) * int(j.strftime('%U')) + float(i['NB1_PriceCoefficient']) * float(NB1_price) + float(i['NB1_PromoCoefficient']) * float(0)
                        else:
                            trend = float(i['InterceptCoefficient']) + float(i['PriceCoefficient']) * float(i['ProductPrice']) + float(i['PromoIndexCoefficient']) * 0 + float(i['WeekCoefficient']) * int(j.strftime('%U'))
                        seasonIndex = float(Seasonality.objects.filter(ProductId=i['id'], WeekNumber=int(j.strftime('%U')), UserId=userid).values().first()['SeasonalityIndex'])
                        quantity = trend * seasonIndex
                        if i['CompetitorIndex'] != '':
                            if float(i['Peod']) < 0.8:
                                Peod_range = "<0.8"
                            elif float(i['Peod']) < 1:
                                Peod_range = "0.8-1"
                            elif float(i['Peod']) < 1.25:
                                Peod_range = "1-1.25"
                            else:
                                Peod_range = ">1.25"
                            rule = CompetitorTierRule.objects.filter(CompetitorTier=(i['CompetitorIndex']), PeodRange=Peod_range).values().first()['ImpactPercentValue']
                            final_quantity = quantity + quantity * rule
                        else:
                            final_quantity = quantity
                        inner_fc_dict[j.strftime("%Y-%m-%d")] = round(final_quantity)
                if inner_fc_dict:
                    promo_fc['Non-Promotional Sales'] = [inner_fc_dict, 1]
            forecast_qty = {}
            for k,v in promo_fc.items():
                fc_qty = {}
                for m,n in v[0].items():
                    fc_qty[m] = round(n/v[1],0)
                forecast_qty[k]= fc_qty
        context = {'form': form, 'items': items, 'productnamepromo': productnamepromo, 'storepromo': storepromo, 'categorynamepromo': categorynamepromo,
                   'subdeptpromo': subdeptpromo, 'upcnumberpromo': upcnumberpromo, 'promotypedip': promotypedip, 'product_info': product_info,
                   'highlights': highlights, 'sd': ordered_sd, 'promo_period': ordered_promo_period, 'forecast_qty': forecast_qty,
                   'productids': productids, 'selecteddict': selecteddict, 'avgplotband':avgplotband, 'bs': ordered_bs}
    else:
        selecteddict = {}
        productids = {}
        product_info = {}
        highlights={}
        ordered_promo_period = []
        ordered_sd ={}
        ordered_bs ={}
        forecast_qty ={}
        form = PromoSearchForm()
        context = {'form': form, 'items': items, 'productnamepromo': productnamepromo, 'storepromo': storepromo,'categorynamepromo': categorynamepromo,
                   'subdeptpromo': subdeptpromo, 'upcnumberpromo': upcnumberpromo, 'promotypedip': promotypedip, 'product_info': product_info,
                   'highlights': highlights, 'sd': ordered_sd, 'promo_period': ordered_promo_period, 'forecast_qty': forecast_qty,
                   'productids': productids, 'selecteddict': selecteddict, 'bs': ordered_bs}
    if request.is_ajax():
        print(request.method, 1)
        nb_product = Products.objects.values().filter(id=product_info['NB1_ProductId'], UserId=userid)
        nb_fc ={}
        for i in nb_product:
            for k in ['current', 'new']:
                inner_fc_dict = {}
                if i['InterceptCoefficient'] != '':
                    for j in arr:
                        old_price = i['ProductPrice']
                        if k == 'new':
                            NB1_price = float(old_price) + float(old_price) * float(nb1_newprice_percent) * 0.01
                        else:
                            NB1_price = old_price
                        trend = float(i['InterceptCoefficient']) + float(i['PriceCoefficient']) * float(NB1_price) + float(
                            i['PromoIndexCoefficient']) * 0 + float(i['WeekCoefficient']) * int(j.strftime('%U'))
                        seasonIndex = float(Seasonality.objects.filter(ProductId=i['id'], WeekNumber=int(j.strftime('%U')), UserId=userid).values().first()['SeasonalityIndex'])
                        quantity = trend * seasonIndex
                        print(i)
                        print(int(j.strftime('%U')),trend,seasonIndex, quantity)
                        if i['CompetitorIndex'] != '':
                            if float(i['Peod']) < 0.8:
                                Peod_range = "<0.8"
                            elif float(i['Peod']) < 1:
                                Peod_range = "0.8-1"
                            elif float(i['Peod']) < 1.25:
                                Peod_range = "1-1.25"
                            else:
                                Peod_range = ">1.25"
                            rule = CompetitorTierRule.objects.filter(CompetitorTier=(i['CompetitorIndex']),
                                                                     PeodRange=Peod_range).values().first()['ImpactPercentValue']
                            final_quantity = quantity + quantity * rule
                        else:
                            final_quantity = quantity
                        inner_fc_dict[j.strftime("%Y-%m-%d")] = round(final_quantity)
                if inner_fc_dict and k =='current':
                    nb_fc['NB1_sales'] = [inner_fc_dict, 1]
                elif inner_fc_dict and k =='new':
                    nb_fc['NB1_new_sales'] = [inner_fc_dict, 1]
                else:
                    pass
        nb_forecast_qty = {}
        for k, v in nb_fc.items():
            fc_qty = {}
            for m, n in v[0].items():
                fc_qty[m] = round(n / v[1], 0)
            nb_forecast_qty[k] = fc_qty
        print(nb_forecast_qty)
        nb_sales = {}
        for k, v in nb_forecast_qty.items():
            nb_sales[k] = sum([n for m, n in v.items()]) / float(len(v))
        print(nb_sales)
        data = {'forecast_qty': forecast_qty, 'nb_sales': nb_sales}
        #print(data)
        return JsonResponse(data)
    else:
        print(request.method,2)
        return render(request, 'promotion.html', context)

def promotionnamedisplay(request):
    promotype = request.GET.get('PromotionType')
    data= {'promotionnamedip' : list(Promotions.objects.filter(PromotionType__icontains=promotype).order_by('PromotionType').values_list('PromotionName' , flat=True).distinct())}
    # print(data)
    return JsonResponse(data)

def productnamedisplay(request):
    category = request.GET.get('CategoryName')
    data= {'productnamedisplay' : list(Products.objects.filter(CategoryName__icontains=category).order_by('CategoryName').values_list('Name' , flat=True).distinct())}
    # print(data)
    return JsonResponse(data)


def execution(request):
    if not request.session.get('user'):
        return redirect('login')
    userid = Users.get_userid(request.session.get('user'))
    productslist = Products.objects.order_by('Name').filter(UserId=userid).values('id','Name','UPC','ProductPrice','CategoryName','SubDeptName').filter(UserId=userid).distinct()
    categoryexe = Products.objects.order_by('CategoryName').filter(UserId=userid).values('CategoryName').distinct()
    subdeptexe = Products.objects.order_by('SubDeptName').filter(UserId=userid).values('SubDeptName').distinct()
    productnameexe = Products.objects.order_by('Name').filter(UserId=userid).values('Name').distinct()
    upcexe= Products.objects.order_by('UPC').filter(UserId=userid).values('UPC').distinct()
    print (userid)
    if request.method == 'POST':
        form = ExecutionSearchForm(request.POST)
        print(form)
        if form.is_valid():
            print("form is valid")
            product_name = request.POST['product_name']
            upc = request.POST['upc']
            sub_department = request.POST['sub_department']
            category = request.POST['category']
            print(form)
            dict = {}
            if userid:
                dict['UserId'] = userid
            if not product_name=='':
                dict['Name__icontains']=product_name
                print (dict['Name__icontains'])
            else:
                None
            if not upc== '':
                dict['UPC__endswith'] = upc
                print (dict['UPC__endswith'])
            else:
                None
            if not category=='CATEGORY':
                dict['CategoryName']=category
                print (dict['CategoryName'])
            else:
                None
            if not sub_department=='SUB DEPARTMENT':
                dict['SubDeptName'] = sub_department
                print (dict['SubDeptName'])
            else:
                None
            print(dict)
            productids = list(Products.objects.order_by('id').filter(UserId=userid).values_list('id',flat=True).filter(**dict).distinct())
            display_cat_names = list(Products.objects.order_by('id').filter(id__in=productids).values_list('Name',flat=True))
            display_present = list(Display.objects.order_by('ProductId').filter(ProductId__in=productids).values_list('DisplayPresentPercent',flat=True))
            authdisplay = list(Display.objects.order_by('ProductId').filter(ProductId__in=productids).values_list('AuthDisplayPercent',flat=True))
            division = {}
            division_data = Region.objects.filter(ProductId__in=productids, UserId=userid).values()
            #print(division_data)
            division_list = list(division_data.values_list('Division', flat=True).distinct())
            #print(division_list)
            for i in division_list:
                division[i] = {}
                stores = list(division_data.filter(Division=i).values_list('Stores', flat=True))
                division[i]['Store_sum'] = sum([int(i) for i in stores])
                displayavg = list(division_data.filter(Division=i).values_list('DisplayPresent', flat=True))
                division[i]['Display_avg'] = sum([int(i) for i in displayavg])/len(displayavg)
                regioncount = list(division_data.filter(Division=i).values_list('Region', flat=True).distinct())
                division[i]['Region_count'] = len(regioncount)
                if len(regioncount)== 1:
                    division[i]['Region_name']= regioncount[0]
                else:
                    division[i]['Region_name'] = ""
                #print(regioncount, regioncount[0])
                #print(division)
            division_drilldown = {}
            for i in division_list:
                division_drilldown[i] = []
                region_data = division_data.filter(Division=i).values()
                for j in region_data:
                    dict_data = {}
                    dict_data['region']= j['Region']
                    dict_data['store']= j['Stores']
                    dict_data['display']= j['DisplayPresent']
                    division_drilldown[i].append(dict_data)
            #print(division_drilldown)
            saleslift_location = {}
            saleslift_data = Location.objects.filter(ProductId__in=productids, UserId=userid).values()
            # print(saleslift_data)
            saleslift_list = list(saleslift_data.values_list('Location', flat=True).distinct())
            # print(saleslift_list)
            for i in saleslift_list:
                saleslift_location[i] = {}
                saleslift = list(saleslift_data.filter(Location=i).values_list('SalesLift', flat=True))
                saleslift_location[i]['Saleslift'] = sum([int(i) for i in saleslift])/len(saleslift)
                displaypercent = list(saleslift_data.filter(Location=i).values_list('DisplayPercent', flat=True))
                saleslift_location[i]['Displaypercent'] = sum([int(i) for i in displaypercent])/len(displaypercent)
                sales = list(saleslift_data.filter(Location=i).values_list('Sales', flat=True))
                saleslift_location[i]['Sales'] = sum([int(i) for i in sales])/len(sales)
                # print(saleslift_location)
            saleslift_type = {}
            saleslift_typedata = Type.objects.filter(ProductId__in=productids, UserId=userid).values()
            print(saleslift_typedata)
            saleslifttype_list = list(saleslift_typedata.values_list('Type', flat=True).distinct())
            print(saleslifttype_list)
            for i in saleslifttype_list:
                saleslift_type[i] = {}
                saleslift = list(saleslift_typedata.filter(Type=i).values_list('SalesLift', flat=True))
                saleslift_type[i]['Saleslift'] = sum([int(i) for i in saleslift])/len(saleslift)
                displaypercent = list(saleslift_typedata.filter(Type=i).values_list('DisplayPercent', flat=True))
                saleslift_type[i]['Displaypercent'] = sum([int(i) for i in displaypercent])/len(displaypercent)
                sales = list(saleslift_typedata.filter(Type=i).values_list('Sales', flat=True))
                saleslift_type[i]['Sales'] = sum([int(i) for i in sales])/len(sales)
                print(saleslift_type)
        print(productids,display_cat_names, display_present,authdisplay)
        return render(request, 'execution.html', {'form':form, 'categoryexe': categoryexe,'subdeptexe': subdeptexe,
                     'productnameexe':productnameexe, 'upcexe':upcexe,'display_cat_names':display_cat_names,'display_present':display_present,
                     'authdisplay':authdisplay, 'division':division, 'division_drilldown':division_drilldown, 'saleslift_location':saleslift_location, 'saleslift_type':saleslift_type })
    else:
        form = ExecutionSearchForm()
        display_cat_names, display_present, authdisplay = [], [], []
        division ={}
        division_drilldown = {}
        saleslift_location = {}
        saleslift_type = {}
    return render(request, 'execution.html', {'form':form, 'categoryexe':categoryexe, 'subdeptexe':subdeptexe,
                 'productnameexe':productnameexe, 'upcexe':upcexe, 'display_cat_names':display_cat_names, 'display_present':display_present,
                 'authdisplay':authdisplay, 'division':division, 'division_drilldown':division_drilldown, 'saleslift_location':saleslift_location, 'saleslift_type':saleslift_type })