from django.contrib import admin
from .models import CarMake, CarModel

@admin.register(CarMake)
class CarMakeAdmin(admin.ModelAdmin):
    list_display = ("name", "description")
    search_fields = ("name",)

@admin.register(CarModel)
class CarModelAdmin(admin.ModelAdmin):
    list_display = ("name", "make", "type", "year", "dealer_id")
    list_filter = ("make", "type", "year")
    search_fields = ("name", "make__name")
