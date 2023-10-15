from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict
import json
from products.models import Product

# Create your views here.
@csrf_exempt
def Home(req):
    msg = "Welcome server is running"
    return HttpResponse(msg)

def noDataFound():
    return JsonResponse({ 'result': [], 'msg': 'No Data Found' }, status = 404)

def getFileData(request, key, default=None):
    return request.FILES.get(key, default)

def getPostData(request, key, default = None):
    return request.POST.get(key, default)

@csrf_exempt
def ProductsCreateUpdate(request, pk = None):
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

        # data = json.loads(request.body)
        # name = data.get('name', '')
        # price = data.get('price', 0)
        # image = data.get('image', None)
        # description = data.get('description', None)

        product = Product(
            name=name,
            price=price,
            image=image,
            description=description
        )
        product.save()
        product_dict = model_to_dict(product)
        print(product.image.url)
        if product.image:
            product_dict['image'] = product.image.url
        try:
            return JsonResponse({ 'result': product_dict, "response": 'Successfully created' }, status = 201)
        except Exception as e:
            print(f"Exception: {e}")
            return JsonResponse({ 'response': 'Failed to create product.' }, status = 400)


@csrf_exempt
def ProductsView(request, pk = None):
    if(request.method == 'GET'):
        if(pk):
            try:
                data = list(Product.objects.all().filter(id = pk, isDeleted = False).values())
                #  'image_url': request.build_absolute_uri(product.image.url) if product.image else None,
                print(data)
                if data:
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
