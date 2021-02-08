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
from .models import Drug, Treatment, Prescription
from datetime import datetime
# Create your views here.



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
        drug_test = request.POST['drug_test']
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
                'success': 'Precription has entered successfuly',
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
def search_prescription_ajax(request):
    try:
        prescription = Prescription.objects.values().values_list('treating__name','amount')
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
    print(product)
    try:
        # if drug_test == 'medication':
        #     drug_test = Prescription.objects.values().values_list('treating__name','amount')
        if drug_test == 'test_medic':
            drug_test = Drug.objects.filter(name=product).values().values_list('name','amount','drug_test')
        drug_test = json.dumps(list(drug_test))
        content = {
            'data': True,
            'drug_test': drug_test
        }
    except:
        content = {
            'data': False,
            'error': 'Could not grab drugs from to Database'
        }
    return JsonResponse(content)


@login_required
def search_drug_table_ajax(request):
    # drug_search = request.GET.get('drug_search', None)
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
