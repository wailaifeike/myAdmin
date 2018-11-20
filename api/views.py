from django.shortcuts import render

# Create your views here.

from Stark import stark
def test(request):
    print(stark.sites._registry)
