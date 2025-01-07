from django.shortcuts import render # type: ignore
from .models import FileSave

def index(request):
  FileSave.objects.create (
    file_passport = request.FILES.get('file_passport'),
    file_snils = request.FILES.get('file_snils'),
    file_lvplc = request.FILES.get('file_lvplc')
  )
  return render(request, 'blank/index.html')
