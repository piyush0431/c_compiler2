# c_compiler/urls.py

from django.urls import path
from .views import compile_code, index

urlpatterns = [
    path('', index, name='index'),
    path('compile/', compile_code, name='compile_code'),
]
