from django.shortcuts import render, redirect
import json
from .models import Employee, Company, CompanyRating, EmployeeRating
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q

# Create your views here.

def home(request):
    return render(request, 'main/home.html')


@login_required(login_url='account:login')
def add_employee(request):
    if request.method == 'POST':
        name = request.POST['name']
        company = request.POST['address']
        if Company.objects.filter(name=company).exists():
            company = Company.objects.get(name=company)
        else:
            company = Company.objects.create(name=company)
            company.save()
        email = request.POST['email']
        photo = request.FILES.get('photo')
        about = request.POST['about']
        employee_type = request.POST['employee_type']
        social_media_link = request.POST['social_media_link']
        attributes = request.POST['attributes']
        attributes = json.loads(attributes)

        employee = Employee.objects.create(name=name, company=company, email=email, photo=photo, about=about,
                            social_media_link=social_media_link, employee_type=employee_type, created_by=request.user)
        employee.save()

        for attribute in attributes:
            if not attribute['name']:
                continue
            employee_rating = EmployeeRating.objects.create(
                user=request.user,
                employee=employee,
                attribute=attribute['name'],
                rating=attribute['rating'],
            )
            employee_rating.save()

        messages.success(request, 'Employee added successfully')
        return render(request, 'main/add_employee.html')
    default_attributes = EmployeeRating.objects.filter(is_default=True)
    all_addresses = Company.objects.all()
    return render(request, 'main/add_employee.html', {'default_attributes': default_attributes, 'all_addresses': all_addresses})



@login_required(login_url='account:login')
def add_address(request):
    if request.method == 'POST':
        name = request.POST['name']
        address = request.POST['address']
        photo = request.FILES.get('photo')
        about = request.POST['about']
        attributes = request.POST['attributes']
        attributes = json.loads(attributes)

        company = Company.objects.get_or_create(name=name)[0]
        company.photo = photo
        company.about = about
        company.address = address
        company.created_by = request.user
        company.save()

        for attribute in attributes:
            if not attribute['name']:
                continue
            company_rating = CompanyRating.objects.create(
                user=request.user,
                company=company,
                attribute=attribute['name'],
                rating=attribute['rating']
            )
            company_rating.save()

        messages.success(request, 'Company added successfully')
        return render(request, 'main/add_address.html')
    default_attributes = CompanyRating.objects.filter(is_default=True)
    return render(request, 'main/add_address.html', {'default_attributes': default_attributes})


def employee(request, employee_id):
    employee = Employee.objects.get(id=employee_id)
    ratings = EmployeeRating.objects.filter(employee=employee)
    rating_objects = []
    rated_by = []
    for rating in ratings:
        if rating.user in rated_by:
            continue
        rated_by.append(rating.user)
        all_ratings = EmployeeRating.objects.filter(user=rating.user, employee=employee)
        average = 0
        if all_ratings:
            total = 0
            for rating in all_ratings:
                total += rating.rating
            average = float("{:.1f}".format(total / len(all_ratings)))
        star = []
        for i in range(1, 6):
            if i <= average:
                star.append('fas fa-star')
            elif i - average < 1:
                star.append('fas fa-star-half-alt')
            else:
                star.append('far fa-star')
        rating_object = {
            'user': rating.user,
            'ratings': all_ratings,
            'average': average,
            'star': star,
        }
        rating_objects.append(rating_object)
    default_attributes = EmployeeRating.objects.filter(is_default=True)
    context = {
        'employee': employee,
        'ratings': rating_objects,
        'default_attributes': default_attributes,
    }
    return render(request, 'main/employee.html', context)


def address(request, address_id):
    address = Company.objects.get(id=address_id)
    ratings = CompanyRating.objects.filter(company=address)
    rating_objects = []
    rated_by = []
    for rating in ratings:
        if rating.user in rated_by:
            continue
        rated_by.append(rating.user)
        all_ratings = CompanyRating.objects.filter(user=rating.user, company=address)
        average = 0
        if all_ratings:
            total = 0
            for rating in all_ratings:
                total += rating.rating
            average = float("{:.1f}".format(total / len(all_ratings)))
        star = []
        for i in range(1, 6):
            if i <= average:
                star.append('fas fa-star')
            elif i - average < 1:
                star.append('fas fa-star-half-alt')
            else:
                star.append('far fa-star')
        rating_object = {
            'user': rating.user,
            'ratings': all_ratings,
            'average': average,
            'star': star,
        }
        rating_objects.append(rating_object)
    default_attributes = CompanyRating.objects.filter(is_default=True)
    context = {
        'address': address,
        'ratings': rating_objects,
        'default_attributes': default_attributes,
    }
    return render(request, 'main/address.html', context)


def address_employees(request, address_id):
    address = Company.objects.get(id=address_id)
    employees = Employee.objects.filter(company=address)
    default_attributes = CompanyRating.objects.filter(is_default=True)
    context = {
        'address': address,
        'employees': employees,
        'default_attributes': default_attributes,
    }
    return render(request, 'main/address_employees.html', context)


def search_employee(request):
    q = request.GET.get('q')
    if q:
        employees = Employee.objects.filter(
            Q(name__icontains=q) |
            Q(company__name__icontains=q) |
            Q(email__icontains=q) |
            Q(about__icontains=q) |
            Q(social_media_link__icontains=q
              )
        ).distinct()
        context = {
            'employees': employees,
        }
        return render(request, 'main/search_employee.html', context)

    messages.error(request, 'Please enter a search query')
    return redirect('main:home')


def search_address(request):
    q = request.GET.get('q')
    if q:
        addresses = Company.objects.filter(
            Q(name__icontains=q) |
            Q(address__icontains=q) |
            Q(about__icontains=q)
        ).distinct()
        context = {
            'addresses': addresses,
        }
        return render(request, 'main/search_address.html', context)

    messages.error(request, 'Please enter a search query')
    return redirect('main:home')


@login_required(login_url='account:login')
def rate_existing_employee(request, employee_id):
    if request.method == 'POST':
        employee = Employee.objects.get(id=employee_id)
        attributes = request.POST['attributes']
        attributes = json.loads(attributes)

        for attribute in attributes:
            if not attribute['name']:
                continue
            if EmployeeRating.objects.filter(user=request.user, employee=employee, attribute=attribute['name']).exists():
                ex = EmployeeRating.objects.get(user=request.user, employee=employee, attribute=attribute['name'])
                ex.rating = attribute['rating']
                ex.save()
                continue
            employee_rating = EmployeeRating.objects.create(
                user=request.user,
                employee=employee,
                attribute=attribute['name'],
                rating=attribute['rating'],
            )
            employee_rating.save()

        messages.success(request, 'Employee rated successfully')
        return redirect('main:employee', employee_id=employee_id)
    return redirect('main:employee', employee_id=employee_id)


@login_required(login_url='account:login')
def rate_existing_address(request, address_id):
    if request.method == 'POST':
        address = Company.objects.get(id=address_id)
        attributes = request.POST['attributes']
        attributes = json.loads(attributes)

        for attribute in attributes:
            if not attribute['name']:
                continue
            if CompanyRating.objects.filter(user=request.user, company=address, attribute=attribute['name']).exists():
                ex = CompanyRating.objects.get(user=request.user, company=address, attribute=attribute['name'])
                ex.rating = attribute['rating']
                ex.save()
                continue
            address_rating = CompanyRating.objects.create(
                user=request.user,
                company=address,
                attribute=attribute['name'],
                rating=attribute['rating']
            )
            address_rating.save()

        messages.success(request, 'Company rated successfully')
        return redirect('main:address', address_id=address_id)
    return redirect('main:address', address_id=address_id)


def all_employees(request):
    employees = Employee.objects.all()
    context = {
        'employees': employees,
    }
    return render(request, 'main/search_employee.html', context)


def all_addresses(request):
    addresses = Company.objects.all()
    context = {
        'addresses': addresses,
    }
    return render(request, 'main/search_address.html', context)


def test(request):
    return render(request, 'main/test.html')






