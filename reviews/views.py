from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.forms.models import model_to_dict
import json
from .models import Review
from customers.models import Customer
from products.models import Product
from ecommerce_backend.utils import getPostData, FieldError

# Create your views here.

def noDataFound():
    return JsonResponse({ 'result': [], 'msg': 'No Data Found' }, status = 404)

@csrf_exempt
def ReviewView(request, pk = None):
    if(request.method == 'GET'):
        if(pk):
            try:
                print(pk)
                review = Review.objects.get(id=pk, isActive=True)
                product = None
                if review.customer_id:
                    try:
                        customer = Customer.objects.get(id=review.customer_id, isActive=True)
                        customer = {
                            'id': customer.id,
                            # 'name': customer.user,
                            'phone': customer.phone_number
                        }
                    except Customer.DoesNotExist:
                        print('Customer not found')
                
                if review.product_id:
                    try:
                        product = Product.objects.get(id=review.product_id)
                        product = {
                            'id': product.id,
                            'name': product.name,
                        }
                    except Product.DoesNotExist:
                        print('Product not found')

                review_details = {
                    'id': review.id,
                    'review': review.review,
                    'customer': customer,
                    'product': product,
                    'date': review.reviewed_date
                }
                return JsonResponse({ 'result': review_details }, status = 200)
            except Review.DoesNotExist:
                return noDataFound()
        else:
            try:
                review = Review.objects.filter(isActive=True).values()
                data = list(review)
                return JsonResponse({ 'result': data, 'records': len(data) }, status = 200)
            except Review.DoesNotExist:
                return noDataFound()

@csrf_exempt
def ReviewCreate(request):
    if(request.method == 'POST'):
        data = json.loads(request.body)
        try:
            customer_id = data['customer_id']
            product_id = data['product_id']
            review = data['review']
        except KeyError as k:
            return FieldError(k)
        try:
            customer = Customer.objects.get(id=customer_id)
        except Customer.DoesNotExist:
            return JsonResponse({ 'response': 'Customer not found' }, status = 400)
        
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return JsonResponse({ 'response': 'Product not found' }, status = 400)

        review = Review(
            customer=customer,
            product=product,
            review=review
        )
        review.save()
        review_dict = model_to_dict(review)
        try:
            return JsonResponse({ 'result': review_dict, "response": 'Successfully created' }, status = 201)
        except Exception as e:
            print(f"Exception: {e}")
            return JsonResponse({ 'response': 'Failed to create review.' }, status = 400)

@csrf_exempt
def ReviewUpdate(request, pk = None):
    if(request.method == 'PATCH'):
        try:
            try:
                review = Review.objects.get(id=pk, isActive=True)
            except Review.DoesNotExist:
                return JsonResponse({ 'response': 'Review not exist' }, status = 400)
            data = json.loads(request.body)
            product_id = data.get('product_id', None)
            customer_id = data.get('customer_id', None)
            review_count = data.get('review', None)
            customer=None
            product=None

            if customer_id:
                try:
                    customer = Customer.objects.get(id = customer_id, isActive=True)
                except Customer.DoesNotExist:
                    return JsonResponse({ 'response': 'No Customer exist' }, status = 400)

            if product_id:
                try:
                    product = Product.objects.get(id = product_id)
                except Product.DoesNotExist:
                    return JsonResponse({ 'response': 'No Product exist' }, status = 400)

            if customer is not None: review.customer = customer
            if product is not None: review.product = product
            if review is not None: review.review = review_count
            # review.isActive = True 
            review.save()
            review_dict = model_to_dict(review)

            return JsonResponse({'result': review_dict, 'response': 'Successfully updated'}, status=200)
        except Exception as e:
            print(e)
            return JsonResponse({'response': 'Failed to update review'}, status=400)


@csrf_exempt
def ReviewDelete(request, pk = None):
    if(request.method == 'DELETE'):
        if(pk is None):
            return JsonResponse({ 'response': 'Review ID is required' }, status = 400)
        
        try:
            review = Review.objects.get(id=pk)
            review.isActive = False
            # review['isActive'] = False
            review.save()
            print('review')
        except Product.DoesNotExist:
            return JsonResponse({ 'response': 'Review not found' }, status = 400)

        # review = Review(
        #     customer=customer,
        #     product=product,
        #     review=review
        # )
        # review.save()
        review_dict = model_to_dict(review)
        try:
            return JsonResponse({ 'result': review_dict, "response": 'Successfully deleted' }, status = 201)
        except Exception as e:
            print(f"Exception: {e}")
            return JsonResponse({ 'response': 'Failed to delete review.' }, status = 400)
