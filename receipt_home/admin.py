from django.contrib import admin
from .models import Drug, Treatment, Prescription
# Register your models here.

admin.site.register(Drug)
admin.site.register(Treatment)
admin.site.register(Prescription)