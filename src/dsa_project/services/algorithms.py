import math

#sorting algorithms

#operations = {compare, swap, sorted, shift}
#e.g {"type": 'swap', "indices": [0, 1], "array": [5, 3, 1, 2, 4]}

def bubble_sort(arr: list[int]) -> list[dict]:
    steps = []

    for i in range(len(arr)):
        swapped = False

        for j in range(len(arr) - 1 - i):
            steps.append({'type': 'compare', 'indices': [j, j + 1], 'array': arr.copy()})
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                steps.append({'type': 'swap', 'indices': [j, j + 1], 'array': arr.copy()})
                swapped = True

        if not swapped:
            break
    steps.append({'type': 'sorted', 'indices': list(range(len(arr))), 'array': arr.copy()})

    return steps


def insertion_sort(arr: list[int]) -> list[dict]:
    steps = []

    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0:
            steps.append({'type': 'compare', 'indices': [j, i], 'array': arr.copy()})

            if arr[j] > key:
                arr[j + 1] = arr[j]
                steps.append({'type': 'shift', 'indices': [j, j + 1], 'array': arr.copy()})
                j -= 1
            else:
                break

        arr[j + 1] = key
        steps.append({ 'type': 'insert', 'indices': [j + 1], 'array': arr.copy()})

    steps.append({'type': 'sorted', 'indices': list(range(len(arr))), 'array': arr.copy()})

    return steps

#sorting algorithms
def linear_search(arr: list[int], target: int) -> list[dict]:
    steps = []

    for i in range(len(arr)):
        steps.append({
            "type": "compare",
            "indices": [i],
            "array": arr.copy(),
            "target": target
        })

        if arr[i] == target:
            steps.append({
                "type": "found",
                "indices": [i],
                "array": arr.copy(),
                "target": target
            })
            return steps

    steps.append({
        "type": "not_found",
        "indices": [],
        "array": arr.copy(),
        "target": target
    })

    return steps


def binary_search(arr: list[int], target: int) -> list[dict]:
    # Binary Search requires sorted data
    arr.sort()

    steps = []
    left = 0
    right = len(arr) - 1

    while left <= right:
        mid = (left + right) // 2

        steps.append({
            "type": "compare",
            "indices": [mid],
            "array": arr.copy(),
            "target": target,
            "left": left,
            "right": right
        })

        if arr[mid] == target:
            steps.append({
                "type": "found",
                "indices": [mid],
                "array": arr.copy(),
                "target": target,
                "left": left,
                "right": right
            })
            return steps

        elif arr[mid] < target:
            steps.append({
                "type": "eliminate",
                "indices": list(range(left, mid + 1)),
                "array": arr.copy(),
                "target": target,
                "left": left,
                "right": right
            })

            left = mid + 1

        else:
            steps.append({
                "type": "eliminate",
                "indices": list(range(mid, right + 1)),
                "array": arr.copy(),
                "target": target,
                "left": left,
                "right": right
            })

            right = mid - 1

    steps.append({
        "type": "not_found",
        "indices": [],
        "array": arr.copy(),
        "target": target
    })

    return steps


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

