from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(request):
    context = { 'test': "Test"}
    return render(request,'review/index.html', context)