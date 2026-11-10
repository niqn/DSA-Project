import math

#sorting algorithms

#operations = {compare, swap, sorted, shift}
#e.g {"type": 'swap', "indices": [0, 1], "array": [5, 3, 1, 2, 4]}

def bubble_sort(arr: list[int]) -> list[dict]:
    steps = []
    for i in range(len(arr)):
        swapped = False
        for j in range(len(arr) - 1 - i):
            steps.append({'type': 'compare', 'indices': [j, j+1], 'array': arr.copy()})
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
                steps.append({'type': 'swap', 'indices': [j, j+1], 'array': arr.copy()})
                swapped = True


        if not swapped:
            break

    steps.append({'type': 'sorted', 'indices': list(range(len(arr))), 'array': arr.copy()})
    return steps

def insertion_sort(arr: list[int]) -> list[dict]:
    steps = []
    for i in range(1,len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0:
            steps.append({'type': 'compare', 'indices': [j, i], 'array': arr.copy()})
            if arr[j] > key:
                arr[j+1] = arr[j]
                steps.append({'type': 'shift', 'indices': [j, j+1], 'array': arr.copy()})
                j -= 1

        arr[j + 1] = key

    steps.append({'type': 'sorted', 'indices': list(range(len(arr))), 'array': arr.copy()})
    return steps

#sorting algorithms
def linear_search(*input):
    pass

def binary_search(*input):
    pass

#number theory

def num_theory_main(choice: int, *args: int) -> int|str|tuple[int, int]:
    match(choice):
        #gcd
        case 1:
            return math.gcd(*args)
        #lcm
        case 2:
            return math.lcm(*args)
        #divisibility
        case 3:
            if len(args) != 2:
                return "Divisibility needs two numbers exactly"
            a, b = args
            if b == 0:
                raise ValueError("Cannot divide by zero")
            q = a // b
            r = a % b
            return q, r
        case _:
            raise ValueError("Invalid operation")

