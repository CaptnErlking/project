from django.shortcuts import render
import random
import json
import time 

def insertion_sort_t(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key

def bubble_sort_t(arr):
    n = len(arr)
    for i in range(n - 1):
        for j in range(n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]

def quick_sort_t(arr):
    def partition(low, high):
        pivot = arr[high]
        i = low - 1
        for j in range(low, high):
            if arr[j] <= pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        return i + 1

    def quick_sort_rec(low, high):
        if low < high:
            pi = partition(low, high)
            quick_sort_rec(low, pi - 1)
            quick_sort_rec(pi + 1, high)

    quick_sort_rec(0, len(arr) - 1)

def merge_sort_t(arr):
    if len(arr) > 1:
        mid = len(arr) // 2
        left_half = arr[:mid]
        right_half = arr[mid:]

        merge_sort(left_half)
        merge_sort(right_half)

        i = j = k = 0
        while i < len(left_half) and j < len(right_half):
            if left_half[i] < right_half[j]:
                arr[k] = left_half[i]
                i += 1
            else:
                arr[k] = right_half[j]
                j += 1
            k += 1

        while i < len(left_half):
            arr[k] = left_half[i]
            i += 1
            k += 1

        while j < len(right_half):
            arr[k] = right_half[j]
            j += 1
            k += 1

def cycle_sort_t(arr):
    n = len(arr)
    for cycle_start in range(0, n - 1):
        item = arr[cycle_start]
        pos = cycle_start

        for i in range(cycle_start + 1, n):
            if arr[i] < item:
                pos += 1

        if pos == cycle_start:
            continue

        while item == arr[pos]:
            pos += 1
        arr[pos], item = item, arr[pos]

        while pos != cycle_start:
            pos = cycle_start
            for i in range(cycle_start + 1, n):
                if arr[i] < item:
                    pos += 1
            while item == arr[pos]:
                pos += 1
            arr[pos], item = item, arr[pos]

def heap_sort_t(arr):
    def heapify(n, i):
        largest = i 
        l = 2 * i + 1  
        r = 2 * i + 2 

        if l < n and arr[l] > arr[largest]:
            largest = l

        if r < n and arr[r] > arr[largest]:
            largest = r

        if largest != i:
            arr[i], arr[largest] = arr[largest], arr[i]
            heapify(n, largest)

    n = len(arr)

    for i in range(n // 2 - 1, -1, -1):
        heapify(n, i)

    for i in range(n - 1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i] 
        heapify(i, 0)

def radix_sort_t(arr):
    def counting_sort(arr, exp):
        n = len(arr)
        output = [0] * n 
        count = [0] * 10 

        for i in range(n):
            index = (arr[i] // exp) % 10
            count[index] += 1

        for i in range(1, 10):
            count[i] += count[i - 1]

        i = n - 1
        while i >= 0:
            index = (arr[i] // exp) % 10
            output[count[index] - 1] = arr[i]
            count[index] -= 1
            i -= 1

        for i in range(n):
            arr[i] = output[i]

    max_val = max(arr)
    exp = 1 
    while max_val // exp > 0:
        counting_sort(arr, exp)
        exp *= 10

def counting_sort_t(arr):
    max_val = max(arr)
    min_val = min(arr)
    range_val = max_val - min_val + 1

    count = [0] * range_val
    output = [0] * len(arr)

    for num in arr:
        count[num - min_val] += 1

    for i in range(1, range_val):
        count[i] += count[i - 1]

    for num in reversed(arr):
        output[count[num - min_val] - 1] = num
        count[num - min_val] -= 1

    for i in range(len(arr)):
        arr[i] = output[i]

def insertion_sort(arr, callback):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
        callback(arr.copy())

def bubble_sort(arr, callback):
    n = len(arr)
    for i in range(n - 1):
        for j in range(n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                callback(arr.copy())

def quick_sort(arr, callback):
    def partition(low, high):
        pivot = arr[high]
        i = low - 1
        for j in range(low, high):
            if arr[j] <= pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
                callback(arr.copy())
        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        callback(arr.copy())
        return i + 1

    def quick_sort_rec(low, high):
        if low < high:
            pi = partition(low, high)
            quick_sort_rec(low, pi - 1)
            quick_sort_rec(pi + 1, high)

    quick_sort_rec(0, len(arr) - 1)

def merge_sort(arr, callback):
    
    global_array = arr.copy()

    def merge(left, right, start_index):
        result = []
        i = 0
        j = 0

        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                result.append(left[i])
                global_array[start_index] = left[i]
                i += 1
            else:
                result.append(right[j])
                global_array[start_index] = right[j]
                j += 1
            start_index += 1
            callback(global_array.copy()) 

        while i < len(left):
            result.append(left[i])
            global_array[start_index] = left[i]
            i += 1
            start_index += 1
            callback(global_array.copy())

        while j < len(right):
            result.append(right[j])
            global_array[start_index] = right[j]
            j += 1
            start_index += 1
            callback(global_array.copy())

        return result

    def merge_sort_rec(arr, start_index=0):
        if len(arr) <= 1:
            return arr

        mid = len(arr) // 2
        left = merge_sort_rec(arr[:mid], start_index)
        right = merge_sort_rec(arr[mid:], start_index + mid)
        return merge(left, right, start_index)

    merge_sort_rec(arr)

def heap_sort(arr, callback):
    def heapify(n, i):
        largest = i
        l = 2 * i + 1
        r = 2 * i + 2
        if l < n and arr[l] > arr[largest]:
            largest = l
        if r < n and arr[r] > arr[largest]:
            largest = r
        if largest != i:
            arr[i], arr[largest] = arr[largest], arr[i]
            callback(arr.copy())
            heapify(n, largest)

    n = len(arr)
    for i in range(n // 2 - 1, -1, -1):
        heapify(n, i)
    for i in range(n - 1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]
        callback(arr.copy())
        heapify(i, 0)

def cycle_sort(arr, callback):
    n = len(arr)
    for cycle_start in range(0, n - 1):
        item = arr[cycle_start]
        pos = cycle_start
        for i in range(cycle_start + 1, n):
            if arr[i] < item:
                pos += 1
        if pos == cycle_start:
            continue
        while item == arr[pos]:
            pos += 1
        arr[pos], item = item, arr[pos]
        callback(arr.copy())
        while pos != cycle_start:
            pos = cycle_start
            for i in range(cycle_start + 1, n):
                if arr[i] < item:
                    pos += 1
            while item == arr[pos]:
                pos += 1
            arr[pos], item = item, arr[pos]
            callback(arr.copy())

def radix_sort(arr, callback):
    def counting_sort(exp):
        n = len(arr)
        output = [0] * n
        count = [0] * 10
        for i in range(n):
            index = (arr[i] // exp) % 10
            count[index] += 1
        for i in range(1, 10):
            count[i] += count[i - 1]
        i = n - 1
        while i >= 0:
            index = (arr[i] // exp) % 10
            output[count[index] - 1] = arr[i]
            count[index] -= 1
            i -= 1
        for i in range(n):
            arr[i] = output[i]
            callback(arr.copy())

    max1 = max(arr)
    exp = 1
    while max1 // exp > 0:
        counting_sort(exp)
        exp *= 10

def counting_sort(arr, callback):
    max_val = max(arr)
    count = [0] * (max_val + 1)
    for num in arr:
        count[num] += 1
    index = 0
    for i, freq in enumerate(count):
        for _ in range(freq):
            arr[index] = i
            index += 1
            callback(arr.copy())

algorithm_map = {
    "Insertion Sort": insertion_sort,
    "Bubble Sort": bubble_sort,
    "Quick Sort": quick_sort,
    "Merge Sort": merge_sort,
    "Heap Sort": heap_sort,
    "Cycle Sort": cycle_sort,
    "Radix Sort": radix_sort,
    "Counting Sort": counting_sort,
}

time_map = {
    "Insertion Sort": insertion_sort_t,
    "Bubble Sort": bubble_sort_t,
    "Quick Sort": quick_sort_t,
    "Merge Sort": merge_sort_t,
    "Heap Sort": heap_sort_t,
    "Cycle Sort": cycle_sort_t,
    "Radix Sort": radix_sort_t,
    "Counting Sort": counting_sort_t,
}

def execute_sorting_with_time_and_steps(algorithm, arr, callback):
    steps = []  

    def step_callback(current_arr):
        steps.append(current_arr)

    def time_callback(current_arr):
        return time.time()

    start_time = time.time()
    algorithm(arr, step_callback)
    time_taken = time.time() - start_time

    return steps, time_taken

def home(request):
    if request.method == 'POST':
        size = int(request.POST.get('size'))
        algorithm = request.POST.get('algorithm')
        arr = [random.randint(1, 100) for _ in range(size)]

        steps = []

        def callback(current_arr):
            steps.append(current_arr)

        algorithm_function = algorithm_map.get(algorithm)
        if not algorithm_function:
            return render(request, 'visualizer/home.html', {
                'error': "Invalid algorithm selected."
            })

        steps, time_taken = execute_sorting_with_time_and_steps(algorithm_function, arr.copy(), callback)

        return render(request, 'visualizer/result.html', {
            'steps': json.dumps(steps),
            'algorithm': algorithm,
            'time_taken': f"{time_taken: }",
            'arr' : arr, 
        })

    return render(request, 'visualizer/home.html')
