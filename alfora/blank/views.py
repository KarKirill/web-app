from django.shortcuts import render # type: ignore
from .models import FileSave

def index(request):
  FileSave.objects.create (
    file = request.FILES.get('file')
  )
  return render(request, 'blank/index.html')
