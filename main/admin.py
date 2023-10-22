from django.contrib import admin
from .models import Employee, EmployeeRating, Company, CompanyRating

# Register your models here.
admin.site.register(Employee)
admin.site.register(Company)

class EmployeeRatingAdmin(admin.ModelAdmin):
    list_display = ('employee', 'attribute', 'rating', 'is_default')
    list_filter = ('employee', 'attribute', 'rating', 'is_default')
    search_fields = ('employee', 'attribute', 'rating', 'is_default')

admin.site.register(EmployeeRating, EmployeeRatingAdmin)

class CompanyRatingAdmin(admin.ModelAdmin):
    list_display = ('company', 'attribute', 'rating', 'is_default')
    list_filter = ('company', 'attribute', 'rating', 'is_default')
    search_fields = ('company', 'attribute', 'rating', 'is_default')

admin.site.register(CompanyRating, CompanyRatingAdmin)