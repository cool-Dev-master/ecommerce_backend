from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict
import json
from products.models import Product, Category

# Create your views here.
@csrf_exempt
def Home(req):
    msg = "Welcome server is running"
    return HttpResponse(msg)

def noDataFound():
    return JsonResponse({ 'result': [], 'msg': 'No Data Found' }, status = 404)

def getFileData(request, key, default=None):
    return request.FILES.get(key, default)

def getPostData(request, key, default = False):
    return request.POST.get(key, default)

@csrf_exempt
def ProductsCreate(request, pk = None):
    if(request.method == 'POST'):
        # Check the size of the uploaded file
        if 'image' in request.FILES:
                uploaded_file = getFileData(request, 'image')
                max_size = 4 * 1024 * 1024  # 4 MB in bytes
                if uploaded_file.size > max_size:
                    return JsonResponse({'response': 'Upload Images below 4mb'}, status=400)

        name = getPostData(request, 'name')
        price = getPostData(request, 'price', 0)
        image = getFileData(request, 'image')
        description = getPostData(request, 'description')
        category_id = getPostData(request, 'category')
        

        try:
            # Your user creation logic here
            category = Category.objects.get(id=category_id)
            category_details = {
                'id': category.id,
                'name': category.name,
            }
        except Category.DoesNotExist:
            return JsonResponse({ 'response': 'Category not found' }, status = 400)

        product = Product(
            name=name,
            price=price,
            image=image,
            category=category,
            description=description
        )
        product.save()
        product_dict = model_to_dict(product)

        if product.image:
            product_dict['image'] = product.image.url
        if product.category:
            product_dict['category'] = category_details

        try:
            return JsonResponse({ 'result': product_dict, "response": 'Successfully created' }, status = 201)
        except Exception as e:
            print(f"Exception: {e}")
            return JsonResponse({ 'response': 'Failed to create product.' }, status = 400)

@csrf_exempt
def ProductsUpdate(request, pk = None):
    # update api
    # if '_method' in request.GET:
    #     overridden_method = request.GET.get('_method', '').upper()
    #     if overridden_method in ('GET', 'POST', 'PUT', 'PATCH', 'DELETE'):
    #         request.method = overridden_method
    #     else:
    #         return JsonResponse({ 'response': 'Method not allowed' }, status = 405)
    if(request.method == 'POST'):
        try:
            try:
                product = Product.objects.get(id=pk)
            except Product.DoesNotExist:
                return JsonResponse({ 'response': 'Product not exist' }, status = 400)
            # Check the size of the uploaded file
            if 'image' in request.FILES:
                uploaded_file = request.FILES['image']
                print('images size checking')
                uploaded_file = getFileData(request, 'image')
                max_size = 4 * 1024 * 1024  # 4 MB in bytes
                if uploaded_file.size > max_size:
                    return JsonResponse({'response': 'Upload Images below 4mb'}, status=400)

            name = getPostData(request, 'name', product.name)
            price = getPostData(request, 'price', product.price)
            image = getFileData(request, 'image', product.image)
            print(image, product.image, "image")
            description = getPostData(request, 'description', product.description)
            category_id = getPostData(request, 'category', None)

            if category_id is not None:
                try:
                    category = Category.objects.get(id=category_id)
                    product.category = category
                except Category.DoesNotExist:
                    return JsonResponse({'response': 'Category not found'}, status=400)

            product.name = name
            product.price = price
            product.image = image
            product.description = description
            product.save()
            product_dict = model_to_dict(product)

            if product.image:
                product_dict['image'] = product.image.url
            if product.category:
                category_details = {
                    'id': product.category.id,
                    'name': product.category.name,
                }
                product_dict['category'] = category_details
            print(product_dict, "dictt")
            return JsonResponse({'result': product_dict, 'response': 'Successfully updated'}, status=200)
        except Exception as e:
            print(e)
            return JsonResponse({'response': 'Failed to update product'}, status=400)

@csrf_exempt
def ProductsView(request, pk = None):
    if(request.method == 'GET'):
        if(pk):
            try:
                data = list(Product.objects.all().filter(id = pk, isDeleted = False).values())
                if data:
                    image_full_url = request.build_absolute_uri(settings.MEDIA_URL) + data[0]['image'] if 'image' in data[0] else None;
                    data[0]['image_full_url'] = image_full_url
                    return JsonResponse({ 'result': data }, status = 200)
                else:
                    return noDataFound()
            except Product.DoesNotExist:
                return noDataFound()
        else:
            try:
                data = list(Product.objects.all().values())
                print(data)
                return JsonResponse({ 'result': data, 'records': len(data) }, status = 200)
            except Product.DoesNotExist:
                return noDataFound()


# category apis

@csrf_exempt
def CategoryView(request, pk = None):
    if(request.method == 'GET'):
        if pk:
            try:
                category = Category.objects.get(id=pk)
                category = model_to_dict(category)
                return JsonResponse({ 'result': category }, status = 200)
            except Category.DoesNotExist:
                return noDataFound()
        else:
            try:
                category = list(Category.objects.all().values())
                return JsonResponse({ 'result': category, 'records': len(category) }, status = 200)
            except Category.DoesNotExist:
                return noDataFound()

@csrf_exempt
def CategoryCreate(request):
    if(request.method == 'POST'):
        data = json.loads(request.body)
        if 'name' not in data:
            return JsonResponse({ 'response': 'Name required' }, status = 400)

        name = data['name']
        try:
            # check exist category
            category = Category.objects.get(name=name)
            if category:
                return JsonResponse({ 'response': 'Category already exist' }, status = 400)
        except Category.DoesNotExist:
            pass

        category = Category(
            name=name
        )
        category.save()
        product_dict = model_to_dict(category)

        try:
            return JsonResponse({ 'result': product_dict, "response": 'Successfully created' }, status = 201)
        except Exception as e:
            print(f"Exception: {e}")
            return JsonResponse({ 'response': 'Failed to create category.' }, status = 400)
        

@csrf_exempt
def CategoryUpdate(request, pk = None):
    if(request.method == 'PUT'):
        if pk:
            data = json.loads(request.body)
            if 'name' not in data:
                return JsonResponse({ 'response': 'Name required' }, status = 400)

            name = data['name']
            try:
                # check exist category
                category = Category.objects.get(id=pk)
            except Category.DoesNotExist:
                return JsonResponse({ 'response': 'Category not exist' }, status = 400)

            category.name = name
            category.save()
            product_dict = model_to_dict(category)

            try:
                return JsonResponse({ 'result': product_dict, "response": 'Successfully updated' }, status = 201)
            except Exception as e:
                print(f"Exception: {e}")
                return JsonResponse({ 'response': 'Failed to update category.' }, status = 400)