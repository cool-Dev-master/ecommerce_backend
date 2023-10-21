from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.db import IntegrityError
from django.forms.models import model_to_dict
import json
from bson import ObjectId
from .models import Order
from customers.models import Customer
from products.models import Product
from ecommerce_backend.utils import get_mongodb_collection, replaceObjectID, getCurrentDateTime, getDateConverted
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
                # data = list(Order.objects.all().filter(id = pk, isActive = True).values())
                data = get_mongodb_collection('orders').find_one({'_id': ObjectId(pk)})
                print(data)
                if data:
                    order = replaceObjectID(data)
                    print(order)
                    order['order_date'] = getDateConverted(order['order_date'])
                    return JsonResponse({ 'result': order }, status = 200)
                else:
                    return noDataFound()
            except Exception as e:
                print(e)
                return JsonResponse({ 'Error': 'Error' }, status = 400)
                # return noDataFound()
        else:
            try:
                data = list(Order.objects.all().filter(isActive = True).values())
                # print(request.user.is_authenticated, "user is_authenticated")
                return JsonResponse({ 'result': data, 'records': len(data) }, status = 200)
            except Order.DoesNotExist:
                return noDataFound()

@csrf_exempt
def OrdersCreate(request):
    if(request.method == 'POST'):
        try:
            data = json.loads(request.body)
            customer_id = data.get('customer_id', None)
            # try:
            #     customer = Customer.objects.get(id = customer_id)
            #     print(customer.cart)
            # except Customer.DoesNotExist:
            #     return JsonResponse({ 'response': 'No Customer exist' }, status = 400)

            product_id = data.get('product_id', None)
            # try:
            #     product = Product.objects.get(id = product_id)
            # except Product.DoesNotExist:
            #     return JsonResponse({ 'response': 'No Product exist' }, status = 400)
            quantity = data.get('quantity', 0)
            cancelled = data.get('cancelled', False)
            date = getCurrentDateTime()

            order_data = {
                'customer': customer_id,
                'product': product_id,
                'quantity': quantity,
                'cancelled': cancelled,
                'order_date': date
            }
            result = get_mongodb_collection('orders').insert_one(order_data)
            # print(result)
            if result:
                inserted_id = str(result.inserted_id)
                # orders = replaceObjectID(result)
                return JsonResponse({ 'result': inserted_id }, status = 200)
            else:
                raise 'Error not found'
        # return JsonResponse({ 'result': order, "customer": customer, "response": 'Successfully created' }, status = 201)
        except Exception as e:
            print(f"Exception: {e}")
            return JsonResponse({ 'response': 'Failed to create order.' }, status = 400)
