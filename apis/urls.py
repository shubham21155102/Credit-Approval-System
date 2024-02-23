from django.urls import path

from . import views

urlpatterns = [
  path("", views.test),
  path("post", views.post),
  path("add_bulk_customers", views.add_bulk_customers),
  path("add_bulk_loans", views.add_bulk_loans),
  path("register", views.register),
  path("check-eligibility", views.check_eligibility),
  path("create-loan", views.create_loan)
 ]