from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Customer,Loan
from .utils.bulk_upload import add_bulk_customers_f, add_bulk_loans_f
import math
from django.http import JsonResponse
@api_view(['GET'])
def test(request):
    person= {"name": "John", "age": 30, "city": "New York"}
    return Response(person)
@api_view(['POST'])
def post(request):
    name= request.data.get("name")
    age= request.data.get("age")
    city= request.data.get("city")
    return Response({"name": name, "age": age, "city": city})
@api_view(['POST'])
def add_bulk_customers(request):
    return  Response(add_bulk_customers_f(request))

@api_view(['POST'])
def add_bulk_loans(request):
    return  Response(add_bulk_loans_f(request))
@api_view(['POST'])
def register(request):
        try:
            first_name = request.data.get('first_name')
            last_name = request.data.get('last_name')
            age = request.data.get('age')
            monthly_income = request.data.get('monthly_income')
            phone_number = request.data.get('phone_number')
            approved_limit = round(36 * int(monthly_income) / 100000) * 100000
            if Customer.objects.filter(phone_number=phone_number).exists():
                return JsonResponse({"message": "Customer with the same phone number already exists"}, status=409)
            try:   
                last_customer_id = Customer.objects.latest('customer_id').customer_id
                last_customer_id = last_customer_id + 1
                Customer.objects.create(
                    customer_id=last_customer_id,
                    first_name=first_name,
                    last_name=last_name,
                    age=age,
                    monthly_salary=monthly_income,
                    approved_limit=approved_limit,
                    current_debt=0,
                    credit_score=100,
                    phone_number=phone_number
                )
                return JsonResponse({"message": "New user created"}, status=201)
            except Exception as e:
                return JsonResponse({"message": str(e)}, status=500)
        except Exception as e:
            return JsonResponse({"message": str(e)}, status=500)