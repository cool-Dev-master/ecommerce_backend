from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.db import IntegrityError
from django.forms.models import model_to_dict
import json
from .models import Order
from customers.models import Customer
from products.models import Product
# Create your views here.

def getPostData(request, key, default = None):
    return request.POST.get(key, default)

def noDataFound():
    return JsonResponse({ 'result': [], 'msg': 'No Data Found' }, status = 404)

@csrf_exempt
def OrdersView(request, pk = None):
    if(request.method == 'GET'):
        if(pk):
            try:
                data = list(Order.objects.all().filter(id = pk, isActive = True).values())
                print(data)
                if data:
                    return JsonResponse({ 'result': data }, status = 200)
                else:
                    return noDataFound()
            except Order.DoesNotExist:
                return noDataFound()
        else:
            try:
                data = list(Order.objects.all().filter(isActive = True).values())
                print(data)
                return JsonResponse({ 'result': data, 'records': len(data) }, status = 200)
            except Order.DoesNotExist:
                return noDataFound()

@csrf_exempt
def OrdersCreate(request):
    if(request.method == 'POST'):
        try:
            data = json.loads(request.body)
            customer_id = data.get('customer_id', None)
            try:
                customer = Customer.objects.get(id = customer_id)
                print(customer.cart)
            except Customer.DoesNotExist:
                return JsonResponse({ 'response': 'No Customer exist' }, status = 400)

            product_id = data.get('product_id', None)
            try:
                product = Product.objects.get(id = product_id)
            except Product.DoesNotExist:
                return JsonResponse({ 'response': 'No Product exist' }, status = 400)
            quantity = data.get('quantity', 0)
            cancelled = data.get('cancelled', False)

            order = Order(
                customer=customer,
                product=product,
                quantity=quantity,
                cancelled=cancelled
            )
            order.save()
            order = model_to_dict(order)
            customer.cart = {'quantity': quantity, 'active':True, 'orders':[product_id]}
            customer.save()
            customer = model_to_dict(customer)
            print(order)
            return JsonResponse({ 'result': order, "customer": customer, "response": 'Successfully created' }, status = 201)
        except Exception as e:
            print(f"Exception: {e}")
            return JsonResponse({ 'response': 'Failed to create order.' }, status = 400)
