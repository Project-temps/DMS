from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse

def collect_data(request):
    # Logic to collect data goes here
    return JsonResponse({'status': 'Data collected successfully'})
