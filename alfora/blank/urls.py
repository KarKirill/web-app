from django.urls import path # type: ignore
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    # path('alfora\\media\\upldfile\\docx\\test.docx', views.index, name='doci')
]