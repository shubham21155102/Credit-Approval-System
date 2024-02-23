from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Customer,Loan
from .utils.bulk_upload import add_bulk_customers_f, add_bulk_loans_f
from django.http import JsonResponse
from .users import check_eligible
from django.utils import timezone
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
                return JsonResponse({"message": "New user created","userDetails":{
                    "customer_id": last_customer_id,
                    "first_name": first_name,
                    "last_name": last_name,
                    "age": age,
                    "monthly_income": monthly_income,
                    "phone_number": phone_number,
                    "approved_limit": approved_limit
                }}, status=201)
            except Exception as e:
                return JsonResponse({"message": str(e)}, status=500)
        except Exception as e:
            return JsonResponse({"message": str(e)}, status=500)
@api_view(['GET'])
def check_eligibility(request):
    customer_id= request.data.get('customer_id')
    tenure= request.data.get('tenure')
    loan_amount= request.data.get('loan_amount')
    interest_rate= request.data.get('interest_rate')
    return Response(check_eligible(customer_id, tenure, loan_amount, interest_rate))
@api_view(['POST'])
def create_loan(request):
        data= request.data
        try:
            customer = Customer.objects.get(customer_id=data.get('customer_id'))
            if customer.credit_score is None:
                customer.credit_score = calculate_credit_score(customer, data.get('monthly_installment'))
                customer.save()
                return JsonResponse({'error': 'Credit score not available try after sometines'}, status=400)
            else :
                if customer.approved_limit < float(data.get('loan_amount')):
                    return JsonResponse({'error': 'Loan not approved because loan amount is more than approved limit'}, status=400)
            
        except Customer.DoesNotExist:
            return JsonResponse({'error': 'Customer not found'}, status=404)
        
        customer_id = data.get('customer_id')
        tenure = int(data.get('tenure'))
        loan_amount = float(data.get('loan_amount'))
        interest_rate = float(data.get('interest_rate'))
        
        eligibility_info = check_eligible(customer_id, tenure, loan_amount, interest_rate)
        
        if eligibility_info['eligible']:

            start_date = timezone.now()
            end_date = start_date + timezone.timedelta(months=tenure)
            new_loan = Loan.objects.create(
                customer_id=customer_id,
                loan_id=1234555,
                loan_amount=loan_amount,
                interest_rate=eligibility_info['interest_rate'],
                emis_paid_on_time=0,
                tenure=tenure,
                monthly_payment=eligibility_info['monthly_installment'],
                start_date=start_date,
                end_date=end_date,
                calculated_emi=eligibility_info['monthly_installment']
            )
            
            return JsonResponse({'message': 'New loan created', 'loan': new_loan.serialize()})
        else:
            return JsonResponse(eligibility_info)

from datetime import datetime

def calculate_credit_score(loan, new_emi):
    # Define the variables to track various factors
    total_emis_paid = loan['EMIs paid on Time']
    total_tenure = loan.tenure
    current_year_activity_points = 0

    # Check for current year loan activity (modify the current year condition as needed)
    current_date = datetime.now()

    # Define the loan start date
    loan_start_date = loan.start_date

    # Calculate the time difference in months
    months_difference = (current_date.year - loan_start_date.year) * 12 + current_date.month - loan_start_date.month

    # Check if the loan was taken more than 12 months ago
    if months_difference >= 12:
        current_year_activity_points += 10

    # Calculate the average ratio of EMIs paid on time to total tenure
    average_ratio = total_emis_paid / total_tenure

    # Calculate the credit score based on the factors
    credit_score = 0
    credit_score += average_ratio * 70  # Adjust based on the average ratio
    credit_score += current_year_activity_points
    return round(credit_score)
