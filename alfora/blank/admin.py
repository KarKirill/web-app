from django.contrib import admin # type: ignore
from .models import Clinic

class ClinicAdmin(admin.ModelAdmin):
  list_display = ('id', 'surname', 'name', 'middle_name', 'gender', 'date_of_birth', 'passport_date', 'passport_place', 'departament_code', 'place_of_residence', 'snils')

admin.site.register(Clinic, ClinicAdmin)