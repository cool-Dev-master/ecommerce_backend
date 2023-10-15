from django.contrib.auth.models import User
from django.forms.models import model_to_dict
from django.contrib.auth import authenticate, login
# from django.shortcuts import render
from django.db import IntegrityError
# from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Customer


def noDataFound():
    return JsonResponse({ 'result': [], 'msg': 'No Data Found' }, status = 404)


@csrf_exempt
@require_POST
def register_customer(request):
    try:
        # print(request)
        data = json.loads(request.body)
        username = data.get('username', '')
        phone_number = data.get('phone', '')
        # username = request.POST.get('username')
        # phone_number = request.POST.get('phone')
        # print(username, phone_number)
        # return JsonResponse({'message': 'Registration failed'}, status=400)
        try:
            try:
                # Your user creation logic here
                user = User.objects.create_user(username=username, password= '')
                user_details = {
                    'id': user.id,
                    'username': user.username,
                }
            except IntegrityError as e:
                # Catch the IntegrityError for duplicate username
                if 'UNIQUE constraint failed: auth_user.username' in str(e):
                    user_exist = User.objects.get(username=username)
                    user_details = {
                        'id': user_exist.id,
                        'username': user_exist.username,
                    }
                    return JsonResponse({'message': 'User with the same username already exists.', 'result': user_details}, status=400)
                    # raise ValidationError({'username': ['User with the same username already exists.']})
            # # Get the User instance by username
            # print(f"user_exist: {user_exist}")
            # if user_exist:
            #     user = user_exist
            # else:
            #     user = User.objects.create_user(username=username, password= '')
            # # Create a new user without a password
            # # Create a Customer instance with the user instance
            # if user_exist:
            #     print(user_exist)
            #     # customer = Customer.objects.create(user=user_exist, other_field='value')
            # else:
            #     user = User.objects.create(username=username)
            #     user.set_unusable_password()
            #     user.save()
            customer = Customer.objects.create(user=user, phone_number=phone_number)
            customer_details = {
                'id': customer.id,
                'name': user_details,
                'phone_number': customer.phone_number,
            }
            print(customer)
            return JsonResponse({'message': 'Registration successful', 'result': customer_details}, status = 201)
        except Exception as e:
            print(f"Error: {e}")
            return JsonResponse({'message': 'Registration failed'}, status=400)
    except:
        return JsonResponse({'message': 'Registration failed'}, status=400)
    

@csrf_exempt
@require_POST
def login_customer(request):
    username = request.POST.get('username')
    phone_number = request.POST.get('phone')

    # Authenticate the user with an empty password
    user = authenticate(request, username=username, password='')
    # print(user)
    # print(f"user: {user}")
    if user is not None:
        # Verify corresponding customer with the provided username and phone number
        try:
            customer = Customer.objects.get(user=user, phone_number=phone_number)
            # print(customer)
            # print(f"customer: {customer}")
        except Customer.DoesNotExist:
            return JsonResponse({'message': 'Login failed - Customer verification failed'}, status=401)


    if user is not None:
        # Log in the user
        login(request, user)
        return JsonResponse({'message': 'Login successful', 'result': {'user': list(user), 'customer': list(customer)}}, status=200)
    else:
        return JsonResponse({'message': 'Login failed'}, status=401)

@csrf_exempt
def CustomersView(request, pk = None):
    if(request.method == 'GET'):
        if(pk):
            try:
                data = list(Customer.objects.all().filter(id = pk, isDeleted = False).values())
                print(data[0], "jjj")
                if data[0]['user_id'] is not None:
                    id = data[0]['user_id']
                    res = User.objects.get(id = id)
                    res = model_to_dict(res)
                    if res:
                        user_detail = {
                            'id': res['id'],
                            'username': res['username'],
                            'email': res['email'],
                            'is_active': res['is_active'],
                            'last_login': res['last_login'],
                        }
                    else:
                        user_detail = None
                    data[0]['user'] = user_detail

                if data:
                    return JsonResponse({ 'result': data }, status = 200)
                else:
                    return noDataFound()
            except Customer.DoesNotExist:
                return noDataFound()
        else:
            try:
                data = list(Customer.objects.all().values())
                # print(data)
                for i in data:
                    id = i['user_id']
                    res = User.objects.get(id = id)
                    res = model_to_dict(res)
                    if res:
                        user_detail = {
                            'id': res['id'],
                            'username': res['username'],
                            'email': res['email'],
                            'is_active': res['is_active'],
                            'last_login': res['last_login'],
                        }
                    else:
                        user_detail = None
                    i['user'] = user_detail
                    
                return JsonResponse({ 'result': data, 'records': len(data) }, status = 200)
            except Customer.DoesNotExist:
                return noDataFound()