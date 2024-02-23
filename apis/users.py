from .models import Customer,Loan
import math
from django.utils import timezone
def check_eligible(customer_id, tenure, loan_amount, interest_rate):
    try:
        customer = Customer.objects.get(pk=customer_id)
    except Customer.DoesNotExist:
        return {'eligible': False, 'message': 'Customer not found'}

    credit_score = customer.credit_score

    if credit_score is None:
        return {'eligible': False, 'message': 'Credit score not available'}

    if customer.approved_limit < loan_amount:
        return {'eligible': False, 'message': 'Loan not approved because loan amount is more than approved limit'}

    if interest_rate <= 8:
        interest_rate = 8

    if credit_score > 50:
        monthly_installment = calculate_emi(loan_amount, interest_rate, tenure)
        return {'eligible': True, 'interest_rate': interest_rate, 'corrected_interest_rate': interest_rate,
                'tenure': tenure, 'monthly_installment': monthly_installment}
    elif 30 < credit_score <= 50:
        monthly_installment = calculate_emi(loan_amount, 12, tenure)
        return {'eligible': True, 'interest_rate': 12, 'corrected_interest_rate': 12,
                'tenure': tenure, 'monthly_installment': monthly_installment}
    elif 10 < credit_score <= 30:
        monthly_installment = calculate_emi(loan_amount, 16, tenure)
        return {'eligible': True, 'interest_rate': 16, 'corrected_interest_rate': 16,
                'tenure': tenure, 'monthly_installment': monthly_installment}
    else:
        return {'eligible': False, 'message': 'Loan not approved'}

def calculate_emi(principal, annual_interest_rate, tenure_months):
    monthly_interest_rate = (annual_interest_rate / 12) / 100
    emi = (principal * monthly_interest_rate) / (1 - math.pow(1 + monthly_interest_rate, -tenure_months))
    return round(emi)

def create_loan(request):
        data= request.data
        customer_id = data.get('customer_id')
        tenure = int(data.get('tenure'))
        loan_amount = float(data.get('loan_amount'))
        interest_rate = float(data.get('interest_rate'))
        
        eligibility_info = check_eligible(customer_id, tenure, loan_amount, interest_rate)
        
        if eligibility_info['eligible']:

            start_date = timezone.now()
            end_date = start_date + timezone.timedelta(days=tenure * 30)
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
            
            return {'message': 'New loan created', 'loan': new_loan.serialize()}
        else:
            return {eligibility_info}
    
