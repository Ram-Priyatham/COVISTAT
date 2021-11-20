from django.contrib import admin
from django.urls import path
from covistatapp.views import indexview

urlpatterns = [
    path('', indexview),
]
