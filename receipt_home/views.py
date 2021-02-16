from django.contrib.auth import (login as auth_login,  authenticate, logout)
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
import json
import string
import math
import random
from django.db.utils import IntegrityError
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Drug, Treatment, Prescription, History
from datetime import datetime, date, timedelta 
from django.utils import timezone
from django.core.exceptions import ValidationError
import pandas as pd
import openpyxl
import os
# Create your views here.


export_var_check = ''

@login_required
def print_home(request):
    content = {}
    return render(request, 'cart_home.html', content)

@login_required
def history_view(request):
    content = {}
    return render(request, 'cart_history.html', content)

@login_required
def add_catalog(request):
    try:
        drugs = Drug.objects.all().values_list('name')
        illments = Treatment.objects.all()
        content = {
            "drugs":drugs,
            "illments":illments
            }
    except TypeError as e:
        print(e)
    return render(request, 'add_product.html', content)

@login_required
def delete_prescription_via_ajax(request):
    if request.is_ajax and request.method == 'POST':
        illness = request.POST['illness']
        try:
            treatment = Treatment.objects.get(
                name=illness
            )
            Prescription.objects.filter(
                treating = treatment
            ).delete()
            treatment.delete()
            content = {
                'data': True,
                'success': '%s Prescription has been removed'%illness
            }

        except:
            content = {
                'data': False,
                'error': 'Could not save Prescription to Database'
            }
        return JsonResponse(content)

@login_required
def add_catalog_ajax(request):
    if request.is_ajax and request.method == 'POST':
        illness = request.POST['illness']
        updatable = request.POST['updatable']
        table = request.POST['table']
        if updatable == 'true':
            try:
                treatment = Treatment.objects.get(
                    name=illness
                )
                Prescription.objects.filter(
                    treating = treatment
                ).delete()
            except:
                content = {
                    'data': False,
                    'error': 'Could not save Prescription to Database'
                }
                return JsonResponse(content)
    
            for k in json.loads(table):
                quantity = k['quantity'].replace("x", "").strip(" ")
                subtotal = k['subtotal'].replace("₦", "").strip(" ")
                product = k['product'].strip(" ")
                # print("The quantity is %s | the subtotal is %s | the product is %s "%(quantity, subtotal, product))
                try:
                    add_drug = Drug.objects.get(name=product) 
                except:
                    content = {
                        'data': False,
                        'error': 'Could not find %s in Database'%product
                    }
                    return JsonResponse(content)
                try:
                    Prescription.objects.create(
                        treating = treatment,
                        drug = add_drug,
                        amount = quantity,
                        added_by = request.user
                    )
                    # print('done')
                except:
                    content = {
                        'data': False,
                        'error': 'Could not save Prescription to Database'
                    }
                    return JsonResponse(content)
            content = {
                'data': True,
                'success': '%s Precription has updated successfully'%illness,
            }
            return JsonResponse(content)

        if updatable == 'false':
            # drug_test = request.POST['drug_test']
            try:
                treatment = Treatment.objects.create(
                    name=illness,
                    added_by=request.user
                )
            except:
                content = {
                    'data': False,
                    'error': 'Could not save Prescription to Database'
                }
                return JsonResponse(content)

            for k in json.loads(table):
                quantity = k['quantity'].replace("x", "").strip(" ")
                subtotal = k['subtotal'].replace("₦", "").strip(" ")
                product = k['product'].strip(" ")
                print("The quantity is %s | the subtotal is %s | the product is %s "%(quantity, subtotal, product))
                try:
                    add_drug = Drug.objects.get(name=product) 
                except:
                    content = {
                        'data': False,
                        'error': 'Could not find %s in Database'%product
                    }
                    return JsonResponse(content)
                try:
                    Prescription.objects.create(
                        treating = treatment,
                        drug = add_drug,
                        amount = quantity,
                        added_by = request.user
                    )
                except:
                    treatment.delete()
                    content = {
                        'data': False,
                        'error': 'Could not save Prescription to Database'
                    }
                    return JsonResponse(content)
        
            content = {
                'data': True,
                'success': 'Precription has entered successfully',
            }
            return JsonResponse(content)

@login_required
def search_drug_ajax(request):
    try:
        drug = Drug.objects.values().values_list('name','amount')
        drugs = json.dumps(list(drug))
        content = {
            'data': True,
            'drugs': drugs
        }
    except:
        content = {
            'data': False,
            'error': 'Could not grab drugs from to Database'
        }
    return JsonResponse(content)

@login_required
def search_drug_test_ajax(request):
    value = request.GET.get('drug_test',None)
    try:
        drug = Drug.objects.filter(drug_test = value).values().values_list('name','amount')
        drugs = json.dumps(list(drug))
        content = {
            'data': True,
            'drugs': drugs
        }
    except:
        content = {
            'data': False,
            'error': 'Could not grab drugs from to Database'
        }
    return JsonResponse(content)

@login_required
def history_table_ajax(request):
    try:
        drug = Drug.objects.filter(drug_test = value).values().values_list('name','amount')
        drugs = json.dumps(list(drug))
        content = {
            'data': True,
            'drugs': drugs
        }
    except:
        content = {
            'data': False,
            'error': 'Could not grab drugs from to Database'
        }
    return JsonResponse(content)


@login_required
def export_and_print(request):
    table = request.POST['table']
    mode_of_payment = request.POST['mode_of_payment']
    received_from = request.POST['received_from']
    email_address = '%s@paiyeborhospital.com'%received_from
    try:
        user = User.objects.get(username__iexact=received_from)
    except User.DoesNotExist:
        user = User.objects.create_user(
                received_from, 
                email_address,
                received_from 
            )
        user.is_active = False
        user.is_staff = False
        user.save()

    for k in json.loads(table):
        quantity = k['quantity'].replace("x", "").strip(" ")
        subtotal = k['subtotal'].replace("₦", "").strip(" ")
        product = k['product'].strip(" ")
        History.objects.create(
            qty = quantity,
            product = product,
            received_by = user,
            mode_of_payment = mode_of_payment,
            created_on = timezone.now(),
            issued_by = request.user,
            amount = subtotal
        ).save()
        # print("The quantity is %s | the subtotal is %s | the product is %s "%(quantity, subtotal, product))

    try:
        content = {
            'data': True,
            'success': "Printing"
        }
    except:
        content = {
            'data': False,
            'error': 'Unable to complete task'
        }
    return JsonResponse(content)


@login_required
def search_prescription_ajax(request):
    try:
        prescription = Treatment.objects.values().values_list('name')
        prescription = json.dumps(list(prescription))
        content = {
            'data': True,
            'prescription': prescription
        }
    except:
        content = {
            'data': False,
            'error': 'Could not grab drugs from to Database'
        }
    return JsonResponse(content)

@login_required
def search_drug_prescription_ajax(request):
    product = request.GET.get('product', None)
    drug_test = request.GET.get('drug_test', None)
    er_string = ''
    try:
        if drug_test == 'test_medic':
            er_string = 'Drug'
            drug_test = Drug.objects.filter(name=product, drug_test='Drug').values().values_list('name','amount','drug_test')
        if drug_test == 'Test':
            er_string = 'Test'
            drug_test = Drug.objects.filter(name=product, drug_test='Test').values().values_list('name','amount')
        if drug_test == 'medication':
            er_string = 'Medication'
            tr = Treatment.objects.get(name=product)
            drug_test = Prescription.objects.filter(treating=tr).values().values_list('drug__name', 'drug__amount','amount')
        value = drug_test.count()
        drug_test = json.dumps(list(drug_test))

        content = {
            'data': True,
            'drug_test': drug_test,
            'length': value,
            'error': 'Could not find %s under %s'%(product, er_string)
        }
    except:
        content = {
            'data': False,
            'error': 'Could not grab drugs from to Database'
        }
    return JsonResponse(content)


@login_required
def search_drug_table_ajax(request):
    # global export_var_check
    # export_var_check = in_search
    data_one = request.GET.get('data_one', None)
    data_two = request.GET.get('data_two', None)
    in_search = request.GET.get('in_search', None)
    pag_num_amount = 10

    if in_search == 'one':
        try:
            history = History.objects.filter(created_on__date=data_one)
            total_page = history.count()
            history = history.values().values_list('qty','product','received_by__username', 'created_on__day', 'created_on__month', 'created_on__year',  'issued_by__username','mode_of_payment', 'amount')
            page = request.GET.get('page', 1)
            paginator = Paginator(history, pag_num_amount)
            try:
                history = paginator.page(page)
            except PageNotAnInteger:
                history = paginator.page(1)
            except EmptyPage:
                history = paginator.page(paginator.num_pages)

            history = json.dumps(list(history))
            if total_page <= pag_num_amount:
                total_page = 1
            else:
                total_page = math.ceil((total_page/pag_num_amount))

            content = {
                'data': True,
                'history': history,
                'total_page': total_page
            }
            return JsonResponse(content)

        except ValidationError:
            content = {
            }
            pass
            return JsonResponse(content)

        except:
            content = {
                'data': False,
                'error': 'Could not grab drugs from to Database'
            }
            return JsonResponse(content)

    if in_search == 'one.five':
        try:
            date_list = []
            date1 = datetime.strptime(data_one, '%Y-%m-%d')
            date2 = datetime.strptime(data_two, '%Y-%m-%d') 
            for dt in daterange(date1, date2):
                date_list.append(dt.strftime('%Y-%m-%d'))
            history = History.objects.filter(created_on__date__in=date_list)
            total_page = history.count()
            history = history.values().values_list('qty','product','received_by__username', 'created_on__day', 'created_on__month', 'created_on__year',  'issued_by__username','mode_of_payment', 'amount')
            page = request.GET.get('page', 1)
            paginator = Paginator(history, pag_num_amount)
            try:
                history = paginator.page(page)
            except PageNotAnInteger:
                history = paginator.page(1)
            except EmptyPage:
                history = paginator.page(paginator.num_pages)

            history = json.dumps(list(history))
            if total_page <= pag_num_amount:
                total_page = 1
            else:
                total_page = math.ceil((total_page/pag_num_amount))

            content = {
                'data': True,
                'history': history,
                'total_page': total_page
            }
            return JsonResponse(content)

        except ValidationError:
            content = {
            }
            pass
            return JsonResponse(content)

        except:
            content = {
                'data': False,
                'error': 'Could not grab drugs from to Database'
            }
            return JsonResponse(content)

    if in_search == 'two':
        try:
            history = History.objects.filter(issued_by__username__icontains=data_one) | History.objects.filter(received_by__username__icontains=data_one) | History.objects.filter(product__icontains=data_one) 
            total_page = history.count()
            history = history.values().values_list('qty','product','received_by__username', 'created_on__day', 'created_on__month', 'created_on__year',  'issued_by__username','mode_of_payment', 'amount')
            page = request.GET.get('page', 1)
            paginator = Paginator(history, pag_num_amount)
            try:
                history = paginator.page(page)
            except PageNotAnInteger:
                history = paginator.page(1)
            except EmptyPage:
                history = paginator.page(paginator.num_pages)

            history = json.dumps(list(history))
            if total_page <= pag_num_amount:
                total_page = 1
            else:
                total_page = math.ceil((total_page/pag_num_amount))

            content = {
                'data': True,
                'history': history,
                'total_page': total_page
            }
            return JsonResponse(content)

        except ValidationError:
            content = {
            }
            pass

        except:
            content = {
                'data': False,
                'error': 'Could not grab drugs from to Database'
            }
            return JsonResponse(content)

    if in_search == 'three':
        try:
            history = History.objects.values().values_list('qty','product','received_by__username', 'created_on__day', 'created_on__month', 'created_on__year',  'issued_by__username','mode_of_payment', 'amount')
            page = request.GET.get('page', 1)
            paginator = Paginator(history, pag_num_amount)
            try:
                history = paginator.page(page)
            except PageNotAnInteger:
                history = paginator.page(1)
            except EmptyPage:
                history = paginator.page(paginator.num_pages)

            history = json.dumps(list(history))
            total_page =  History.objects.all().count()
            if total_page <= pag_num_amount:
                total_page = 1
            else:
                total_page = math.ceil((total_page/pag_num_amount))

            content = {
                'data': True,
                'history': history,
                'total_page': total_page
            }
            return JsonResponse(content)
        except:
            content = {
                'data': False,
                'error': 'Could not grab drugs from to Database'
            }
            return JsonResponse(content)

    try:
        history = History.objects.all().values().values_list('qty','product','received_by__username', 'created_on__day', 'created_on__month', 'created_on__year',  'issued_by__username','mode_of_payment', 'amount')
        page = request.GET.get('page', 1)
        paginator = Paginator(history, pag_num_amount)
        try:
            history = paginator.page(page)
        except PageNotAnInteger:
            history = paginator.page(1)
        except EmptyPage:
            history = paginator.page(paginator.num_pages)

        history = json.dumps(list(history))
        total_page =  History.objects.all().count()
        if total_page <= pag_num_amount:
            total_page = 1
        else:
            total_page = math.ceil((total_page/pag_num_amount))

        content = {
            'data': True,
            'history': history,
            'total_page': total_page
        }
        return JsonResponse(content)
    except:
        content = {
            'data': False,
            'error': 'Could not grab drugs from to Database'
        }
        return JsonResponse(content)

def daterange(date1, date2):
    for n in range(int ((date2 - date1).days)+1):
        yield date1 + timedelta(n)

@login_required
def export_to_xml(request):
    date_one = request.GET.get('date_one', None)
    date_two = request.GET.get('date_two', None)
    try:
        date_list = []
        date1 = datetime.strptime(date_one, '%Y-%m-%d')
        date2 = datetime.strptime(date_two, '%Y-%m-%d') 
        for dt in daterange(date1, date2):
            date_list.append(dt.strftime('%Y-%m-%d'))
        history = History.objects.filter(created_on__date__in=date_list)
        total_page = history.count()
        history = history.values().values_list('qty','product','received_by__username', 'created_on__day', 'created_on__month', 'created_on__year',  'issued_by__username','mode_of_payment', 'amount')
        # history = json.dumps(list(history))
        final_list = []
        for h in list(history):
            quantity = int(h[0])
            product = h[1]
            received_by = h[2]
            date = '%d-%d-%d'%(h[3], h[4], h[5])
            issued_by = h[6]
            mode_of_payment = h[7]
            amount = h[8]
            __ar = [quantity,product,received_by,date,issued_by,mode_of_payment,amount]
            final_list.append(__ar)
        
        filename = 'pos_report_%s_to_%s(generated_%s).xlsx'%(date_one, date_two, datetime.now())
        new_folder = os.path.expanduser('~/Documents/POS_Report')
        if not os.path.exists(new_folder):
            os.mkdir(new_folder)
        save_to = os.path.join(new_folder,filename)
        # df = pd.DataFrame(final_list, columns=['Quantity', 'Product', 'Received By', 'Date', 'Issued By','Mode Of Payment','Amount'])
        # df.to_excel(save_to, sheet_name='hospital_report')    # print(history)

        content = {
            'data': True,
            'success': 'Report has been saved Successfully',
        }
        return JsonResponse(content)

    except ValidationError:
        content = {
        }
        pass
        return JsonResponse(content)

    except:
        content = {
            'data': False,
            'error': 'Could not grab drugs from to Database'
        }
        return JsonResponse(content)


@login_required
def search_textbox_drug_test_ajax(request):
    try:
        drug = Drug.objects.values().values_list('name','desc','amount', 'code_name', 'drug_test')[0:4]
        total_page = Drug.objects.all().count()
        drugs = json.dumps(list(drug))
        if total_page <= 4:
            total_page = 1
        else:
            total_page = math.ceil((total_page/4))
        content = {
            'data': True,
            'drugs': drugs,
            'total_page': total_page
        }
    except:
        content = {
            'data': False,
            'error': 'Could not grab drugs from to Database'
        }
    return JsonResponse(content)


@login_required
def search_textbox_drug_table_ajax(request):
    drug_search = request.GET.get('drug_search', None)
    try:
        drug = Drug.objects.filter(name__icontains=drug_search) | Drug.objects.filter(desc__icontains=drug_search)
        drug = drug.values().values_list('name','desc','amount', 'code_name', 'drug_test')
        total_page =  drug.count()
        page = request.GET.get('page', 1)
        paginator = Paginator(drug, 4)
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)
        drugs = json.dumps(list(posts))
        if total_page <= 4:
            total_page = 1
        else:
            total_page = math.ceil((total_page/4))
        content = {
            'data': True,
            'drugs': drugs,
            'total_page': total_page
        }
    except:
        content = {
            'data': False,
            'error': 'Could not grab drugs from to Database'
        }
    return JsonResponse(content)


@login_required
def search_drug_table_pagination_ajax(request):
    drug_search = request.GET.get('drug_search', None)
    try:
        drug = Drug.objects.filter(name__icontains=drug_search) | Drug.objects.filter(desc__icontains=drug_search)
        drug = drug.values().values_list('name','desc','amount', 'code_name', 'drug_test')
        total_page = drug.count()
        page = request.GET.get('page', 1)
        paginator = Paginator(drug, 4)
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)
        drugs = json.dumps(list(posts))

        if total_page <= 4:
            total_page = 1
        else:
            total_page = math.ceil((total_page/4))
        content = {
            'data': True,
            'drugs': drugs,
            'total_page': total_page

        }
    except:
        content = {
            'data': False,
            'error': 'Could not grab drugs from to Database'
        }
    return JsonResponse(content)


@login_required
def get_drugs_via_prescription_ajax(request):
    if request.is_ajax and request.method == 'POST':
        illness = request.POST['illness']
        try:
            tr = Treatment.objects.get(name=illness)
            pr = Prescription.objects.filter(treating=tr).values().values_list('drug__name', 'drug__amount','amount')
            content = {
                'data': True,
                'drugs': json.dumps(list(pr))
            }
        except:
            content = {
                'data': False,
                'error': 'Could not grab drugs from to Database'
            }
        return JsonResponse(content)



@login_required
def add_drug_ajax(request):
    drug_name = request.POST['drug_name']
    drug_test = request.POST['drug_test']
    drug_amount = request.POST['drug_amount']
    drug_description = request.POST['drug_description']
    if drug_name != '' or  drug_amount != '':
        try:
            a_c = string.ascii_letters + string.digits
            # a_c = str(datetime.now()) + str(drug_name) + str(drug_amount)
            invalid_code_name = True
            while invalid_code_name:
                try:
                    c_w = ''.join((random.choice(a_c) for i in range(7)))
                    Drug.objects.get(code_name=c_w)
                except:
                    invalid_code_name = False
                    # pass

            Drug.objects.create(
                name=drug_name,
                amount=drug_amount,
                desc=drug_description,
                drug_test = drug_test,
                code_name=c_w,
                added_by=request.user
            )
            content = {
                'data': True,
                'success': '%s has been saved successfully'%drug_name
            }
        except IntegrityError:
            content = {
                'data': False,
                'error': 'Drug name already exist'
            }
        except:
            content = {
                'data': False,
                'error': 'Drug could not be saved at the moment'
            }

        return JsonResponse(content)
    else:
        print('error')
    

@login_required
def update_drug_ajax(request):
    if request.is_ajax and request.method == 'GET':
        c_s = request.GET.get('drug_cs', None)
        try:
            drug_ins = Drug.objects.get(code_name=c_s)
            content = {
                'data': True,
                'drug_name': drug_ins.name,
                'drug_amount': drug_ins.amount,
                'drug_description': drug_ins.desc,
                'drug_test': drug_ins.drug_test,
            }
        except:
        # except Drug.DoesNotExist:
            content = {
                'data': False,
                'error': 'Unable to find drug'
            }
        return JsonResponse(content)

    if request.is_ajax and request.method == 'POST':
        drug_cs = request.POST['drug_cs']
        drug_name = request.POST['drug_name']
        drug_amount = request.POST['drug_amount']
        drug_test = request.POST['drug_test']
        drug_description = request.POST['drug_description']
        if drug_name != '' or drug_name is not None or drug_amount != '' or drug_amount is not None:
            try:
                drug_ins = Drug.objects.get(code_name=drug_cs.strip(''))
                drug_ins.name=drug_name
                drug_ins.amount=drug_amount
                drug_ins.desc=drug_description
                drug_ins.added_by=request.user
                drug_ins.drug_test=drug_test
                drug_ins.save()
                content = {
                    'data': True,
                    'success': 'Changes has been updated successfully'
                }
            except:
                content = {
                    'data': False,
                    'error': 'Could not complete update now'
                }
        return JsonResponse(content)

@login_required
def delete_drug_ajax(request):
    if request.is_ajax and request.method == 'GET':
        c_s = request.GET.get('drug_cs', None)
        try:
            Drug.objects.get(code_name=c_s).delete()
            content = {
                'data': True,
                'success': 'Drug has been deleted successfully'
            }
        except:
        # except Drug.DoesNotExist:
            content = {
                'data': False,
                'error': 'Unable to delete drug'
            }
        return JsonResponse(content)
