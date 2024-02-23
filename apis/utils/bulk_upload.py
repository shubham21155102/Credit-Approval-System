from ..models import Customer,Loan
from django.core.exceptions import ObjectDoesNotExist
import pandas as pd
import math
def add_bulk_customers_f(request):
    x=pd.read_excel("customer_data.xlsx")
    customerId= x["Customer ID"].tolist()
    firstName= x["First Name"].tolist()
    lastName= x["Last Name"].tolist()
    name= [firstName[i]+ " "+ lastName[i] for i in range(len(firstName))]
    age= x["Age"].tolist()
    phone= x["Phone Number"].tolist()
    monthlyIncome= x["Monthly Salary"].tolist()
    approvedLimit= x["Approved Limit"].tolist()
    data= []
    for i in range(len(name)):
        try:
            customer= Customer.objects.get(customer_id=customerId[i])
            if customer is not None:
                print("Customer already exists")
        except:
            customer= Customer(customer_id=customerId[i],first_name=firstName[i],last_name=lastName[i],age=age[i],phone_number=phone[i],monthly_salary=monthlyIncome[i],approved_limit=approvedLimit[i])
            print("Customer does not exist",customer)
            customer.save()
        data.append({"customerId":customerId[i],"name": name[i], "age": age[i], "phone": phone[i], "monthlyIncome": monthlyIncome[i], "approvedLimit": approvedLimit[i]})
    return data;
def add_bulk_loans_f(request):
    try:
        loan_data = pd.read_excel("loan_data.xlsx")
        loan_data_columns = [
            "Loan ID", "Customer ID", "Loan Amount", "Tenure", 
            "Interest Rate", "Monthly payment", "EMIs paid on Time", 
            "Date of Approval", "End Date"
        ]
        loan_data = loan_data[loan_data_columns]

        data = []
        for index, row in loan_data.iterrows():
            try:
                customer_id = row["Customer ID"]
                customer = Customer.objects.get(pk=customer_id)
                calculated_emi = calculate_emi(
                    row["Loan Amount"], 
                    row["Tenure"], 
                    row["Interest Rate"]
                )
                loan = Loan.objects.create(
                    loan_id=row["Loan ID"],
                    customer_id=customer,
                    loan_amount=row["Loan Amount"],
                    tenure=row["Tenure"],
                    interest_rate=row["Interest Rate"],
                    monthly_payment=row["Monthly payment"],
                    emis_paid_on_time=row["EMIs paid on Time"],
                    start_date=row["Date of Approval"],
                    end_date=row["End Date"],
                    calculated_emi=calculated_emi
                )
                print("New loan created:", loan)
                data.append({
                    "loanId": row["Loan ID"],
                    "customerId": customer_id,
                    "loanAmount": row["Loan Amount"],
                    "tenure": row["Tenure"],
                    "interestRate": row["Interest Rate"],
                    "monthlyIncome": row["Monthly payment"],
                    "emiPaidOnTime": row["EMIs paid on Time"],
                    "dateOfApproval": row["Date of Approval"],
                    "endDate": row["End Date"]
                })
            except ObjectDoesNotExist:
                print(f"Customer with ID {customer_id} does not exist")
        
        return data;
    except Exception as e:
        return {"error": str(e)}
def calculate_emi(principal, annual_interest_rate, tenure_months):
    monthly_interest_rate = (annual_interest_rate / 12) / 100
    emi = (principal * monthly_interest_rate) / (1 - math.pow(1 + monthly_interest_rate, -tenure_months))
    return round(emi)

    