from django.db import models

class Customer(models.Model):
    customer_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    age = models.IntegerField()
    phone_number = models.CharField(max_length=15, unique=True)
    monthly_salary = models.IntegerField(null=True, blank=True)
    approved_limit = models.IntegerField(null=True, blank=True)
    current_debt = models.IntegerField(null=True, blank=True)
    credit_score = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'customers'
class Loan(models.Model):
    loan_id = models.AutoField(primary_key=True)
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    loan_amount = models.IntegerField()
    tenure = models.IntegerField()
    interest_rate = models.FloatField()
    monthly_payment = models.IntegerField()
    emis_paid_on_time = models.IntegerField()
    start_date = models.DateField()
    end_date = models.DateField()
    calculated_emi = models.IntegerField()

    class Meta:
        db_table = 'loans'