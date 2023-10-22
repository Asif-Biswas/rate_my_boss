from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.home, name='home'),
    path('add-employee/', views.add_employee, name='add_employee'),
    path('add-address/', views.add_address, name='add_address'),
    path('employee/<int:employee_id>/', views.employee, name='employee'),
    path('address/<int:address_id>/', views.address, name='address'),
    path('address-employees/<int:address_id>/', views.address_employees, name='address_employees'),
    path('search-employee/', views.search_employee, name='search_employee'),
    path('search-address/', views.search_address, name='search_address'),
    path('rate-existing-employee/<int:employee_id>/', views.rate_existing_employee, name='rate_existing_employee'),
    path('rate-existing-address/<int:address_id>/', views.rate_existing_address, name='rate_existing_address'),
    path('all-employees/', views.all_employees, name='all_employees'),
    path('all-addresses/', views.all_addresses, name='all_addresses'),
]