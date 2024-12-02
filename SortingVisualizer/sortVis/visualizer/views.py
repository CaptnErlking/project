from django.shortcuts import render

from django.http import JsonResponse
import random
import json

# Function to generate a random array
def generate_random_array(size):
    return [random.randint(1, 100) for _ in range(size)]

# Home page view
def home(request):
    return render(request, 'visualizer/index.html')

# API to generate an array
def generate_array(request):
    size = int(request.GET.get('size', 50))  # Default size = 50
    array = generate_random_array(size)
    return JsonResponse({'array': array})

# API to simulate sorting (example with bubble sort)
def sort_array(request):
    array = json.loads(request.GET.get('array', '[]'))
    steps = []  # To log sorting steps

    # Bubble Sort Algorithm
    n = len(array)
    for i in range(n):
        for j in range(0, n-i-1):
            if array[j] > array[j+1]:
                array[j], array[j+1] = array[j+1], array[j]
                steps.append({'swap': [j, j+1], 'array': array[:]})

    return JsonResponse({'steps': steps})
