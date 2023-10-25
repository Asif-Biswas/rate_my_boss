from django.db import models
from django.contrib.auth.models import User

# Create your models here.
    

class Employee(models.Model):
    EMPLOYEE_TYPE = (
        ('Boss', 'Boss'),
        ('Manager', 'Manager'),
        ('Employee', 'Employee'),
    )
    name = models.CharField(max_length=100)
    company = models.ForeignKey('Company', on_delete=models.SET_NULL, blank=True, null=True)
    employee_type = models.CharField(max_length=100, choices=EMPLOYEE_TYPE, default='Employee')
    email = models.CharField(max_length=100, blank=True, null=True)
    photo = models.ImageField(upload_to='images/', blank=True, null=True)
    about = models.TextField(blank=True, null=True)
    social_media_link = models.CharField(max_length=500, blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name} - {self.company}'
    
    def get_total_rating(self):
        ratings = EmployeeRating.objects.filter(employee=self)
        return len(ratings)
    
    def get_average_rating(self):
        ratings = EmployeeRating.objects.filter(employee=self)
        if ratings:
            total = 0
            for rating in ratings:
                total += rating.rating
            return float("{:.1f}".format(total / len(ratings)))
        else:
            return 0
        
    def get_star(self):
        average_rating = self.get_average_rating()
        stars = []
        for i in range(1, 6):
            if i <= average_rating:
                stars.append('fas fa-star')
            elif i - average_rating < 1:
                stars.append('fas fa-star-half-alt')
            else:
                stars.append('far fa-star')

        return stars
    
    def get_top_two_ratings(self):
        ratings = EmployeeRating.objects.filter(employee=self).order_by('-rating')
        if len(ratings) < 2:
            return ratings
        top_two = []
        top_two.append(ratings[0])
        top_two.append(ratings[len(ratings)-1])
        return top_two
    
    def get_total_user_rated(self):
        ratings = EmployeeRating.objects.filter(employee=self)
        users = []
        for rating in ratings:
            if rating.user not in users:
                users.append(rating.user)
        return len(users)
    
    def all_ratings(self):
        ratings = EmployeeRating.objects.filter(employee=self)
        return ratings



class EmployeeRating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    attribute = models.CharField(max_length=100)
    rating = models.IntegerField()
    text = models.TextField(blank=True, null=True)
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'{self.employee.name} - {self.attribute} - {self.rating}'
    
    def get_percentage(self):
        ratings = EmployeeRating.objects.filter(employee=self.employee, attribute=self.attribute)
        total = 0
        for rating in ratings:
            total += rating.rating
        return int((total / (len(ratings)*5)) * 100)
    
    def get_this_percentage(self):
        return int((self.rating / 5) * 100)
    
    def get_star(self):
        stars = []
        for i in range(1, 6):
            if i <= self.rating:
                stars.append('fas fa-star')
            elif i - self.rating < 1:
                stars.append('fas fa-star-half-alt')
            else:
                stars.append('far fa-star')

        return stars
    


class Company(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='images/', blank=True, null=True)
    about = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    def get_total_rating(self):
        ratings = CompanyRating.objects.filter(company=self)
        return len(ratings)
    
    def get_average_rating(self):
        ratings = CompanyRating.objects.filter(company=self)
        if ratings:
            total = 0
            for rating in ratings:
                total += rating.rating
            return float("{:.1f}".format(total / len(ratings)))
        else:
            return 0
        
    def get_star(self):
        average_rating = self.get_average_rating()
        stars = []
        for i in range(1, 6):
            if i <= average_rating:
                stars.append('fas fa-star')
            elif i - average_rating < 1:
                stars.append('fas fa-star-half-alt')
            else:
                stars.append('far fa-star')

        return stars
    
    def get_top_two_ratings(self):
        ratings = CompanyRating.objects.filter(company=self).order_by('-rating')
        if len(ratings) < 2:
            return ratings
        top_two = []
        top_two.append(ratings[0])
        top_two.append(ratings[len(ratings)-1])
        return top_two
    
    def get_total_user_rated(self):
        ratings = CompanyRating.objects.filter(company=self)
        users = []
        for rating in ratings:
            if rating.user not in users:
                users.append(rating.user)
        return len(users)
    
    def all_ratings(self):
        ratings = CompanyRating.objects.filter(company=self)
        return ratings

    def get_all_employees(self):
        employees = Employee.objects.filter(company=self)
        return employees


class CompanyRating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    attribute = models.CharField(max_length=100)
    rating = models.IntegerField()
    text = models.TextField(blank=True, null=True)
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'{self.company.name} - {self.attribute} - {self.rating}'
    
    def get_percentage(self):
        ratings = CompanyRating.objects.filter(company=self.company, attribute=self.attribute)
        total = 0
        for rating in ratings:
            total += rating.rating
        return int((total / (len(ratings)*5)) * 100)
    
    def get_this_percentage(self):
        return int((self.rating / 5) * 100)
    
    def get_star(self):
        stars = []
        for i in range(1, 6):
            if i <= self.rating:
                stars.append('fas fa-star')
            elif i - self.rating < 1:
                stars.append('fas fa-star-half-alt')
            else:
                stars.append('far fa-star')

        return stars