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
        steps.append({"type": "compare", "indices": [i], "array": arr.copy(), "target": target})
        if arr[i] == target:
            steps.append({"type": "found", "indices": [i], "array": arr.copy(), "target": target})
            return steps

    steps.append({"type": "not_found", "indices": [], "array": arr.copy(), "target": target})

    return steps


def binary_search(arr: list[int], target: int) -> list[dict]:
    arr.sort()
    steps = []
    left = 0
    right = len(arr) - 1

    while left <= right:
        mid = (left + right) // 2
        steps.append({"type": "compare", "indices": [mid], "array": arr.copy(), "target": target, "left": left, "right": right})

        if arr[mid] == target:
            steps.append({"type": "found", "indices": [mid], "array": arr.copy(), "target": target, "left": left, "right": right})
            return steps
        elif arr[mid] < target:
            steps.append({"type": "eliminate", "indices": list(range(left, mid + 1)), "array": arr.copy(), "target": target, "left": left, "right": right})
            left = mid + 1
        else:
            steps.append({"type": "eliminate", "indices": list(range(mid, right + 1)), "array": arr.copy(), "target": target, "left": left, "right": right})
            right = mid - 1
    steps.append({"type": "not_found", "indices": [], "array": arr.copy(), "target": target})

    return steps


#=======================================number theory section

def gcd(a: int, b: int) -> int:
    return math.gcd(a, b)

def lcm(a: int, b: int) -> int:
    return math.lcm(a, b)

def division_algorithm(a: int, b: int) -> dict:
    if b == 0:
        raise ValueError("The divisor cannot be zero.")

    remainder = a % abs(b)
    quotient = (a - remainder) // b

    return {"quotient": quotient, "remainder": remainder, "equation": f"{a} = ({b})({quotient}) + {remainder}"}

def divisibility(a: int, b: int) -> dict:
    if a == 0:
        raise ValueError("The divisor cannot be zero.")

    divisible = b % a == 0
    return {"divisible": divisible, "message": (
            f"{a} divides {b}" if divisible else f"{a} does not divide {b}")}


def extended_gcd(a: int, b: int) -> dict:
    old_r, r = abs(a), abs(b)
    old_s, s = 1, 0
    old_t, t = 0, 1

    while r:
        q = old_r // r
        old_r, r = r, old_r - q * r
        old_s, s = s, old_s - q * s
        old_t, t = t, old_t - q * t

    x = old_s if a >= 0 else -old_s
    y = old_t if b >= 0 else -old_t

    return {"gcd": old_r,
        "x": x,
        "y": y,
        "equation": f"{old_r} = ({a})({x}) + ({b})({y})"
    }

def binomial_coefficient(n: int, k: int) -> int:
    if n < 0 or k < 0 or k > n:
        raise ValueError("Require n >= 0 and 0 <= k <= n.")

    return math.comb(n, k)

def binomial_term(n: int, k: int, a: int, b: int) -> dict:
    if n < 0 or k < 0 or k > n:
        raise ValueError("Require n >= 0 and 0 <= k <= n.")

    coefficient = math.comb(n, k)
    value = coefficient * (a ** k) * (b ** (n - k))

    return {
        "coefficient": coefficient,
        "value": value,
        "term": f"{coefficient} * ({a})^{k} * ({b})^{n-k}"
    }

def linear_congruence(a: int, b: int, m: int) -> dict:
    if m <= 0:
        raise ValueError("The modulus must be a positive integer.")

    divisor = math.gcd(a, m)

    if b % divisor != 0:
        return {
            "equation": f"{a}x ≡ {b} (mod {m})",
            "message": (
                f"No solution exists because gcd({a}, {m}) = {divisor}, "
                f"and {divisor} does not divide {b}."
            ),
            "gcd": divisor,
            "condition": f"{divisor} does not divide {b}",
            "has_solution": False,
            "solutions": []
        }

    reduced_a = a // divisor
    reduced_b = b // divisor
    reduced_m = m // divisor

    if reduced_m == 1:
        base_solution = 0
        inverse = None
    else:
        inverse = pow(reduced_a % reduced_m, -1, reduced_m)
        base_solution = (inverse * reduced_b) % reduced_m

    solutions = sorted(
        (base_solution + k * reduced_m) % m
        for k in range(divisor)
    )

    return {
        "equation": f"{a}x ≡ {b} (mod {m})",
        "message": f"There are {divisor} distinct solution(s) modulo {m}.",
        "gcd": divisor,
        "condition": f"{divisor} divides {b}",
        "has_solution": True,
        "reduced_equation": f"{reduced_a}x ≡ {reduced_b} (mod {reduced_m})",
        "inverse": inverse if inverse is not None else "Not needed (reduced modulus is 1)",
        "base_solution": base_solution,
        "solution_count": len(solutions),
        "solutions": solutions
    }


# formula

NUMBER_THEORY_FORMULAS = {
    "gcd": {
        "function": gcd,
        "fields": ["a", "b"]
    },
    "lcm": {
        "function": lcm,
        "fields": ["a", "b"]
    },
    "division": {
        "function": division_algorithm,
        "fields": ["a", "b"]
    },
    "divisibility": {
        "function": divisibility,
        "fields": ["a", "b"]
    },
    "extended_gcd": {
        "function": extended_gcd,
        "fields": ["a", "b"]
    },
    "binomial_coefficient": {
        "function": binomial_coefficient,
        "fields": ["n", "k"]
    },
    "binomial_term": {
        "function": binomial_term,
        "fields": ["n", "k", "a", "b"]
    }, 
    "linear_congruence": {
        "function": linear_congruence,
        "fields": ["a", "b", "m"]
    }, 
}

NUMBER_THEORY_METADATA = {
    "gcd": {
        "name": "Greatest Common Divisor (GCD)",
        "description": "Find the greatest positive integer that divides both a and b.",
        "fields": [
            {"id": "a", "label": "First Integer", "default": 252},
            {"id": "b", "label": "Second Integer", "default": 198}
        ]
    },

    "lcm": {
        "name": "Least Common Multiple (LCM)",
        "description": "Find the smallest positive integer that is a multiple of both a and b.",
        "fields": [
            {"id": "a", "label": "First Integer", "default": 12},
            {"id": "b", "label": "Second Integer", "default": 18}
        ]
    },

    "division": {
        "name": "Division Algorithm",
        "description": "Express a as bq + r, where 0 ≤ r < |b|.",
        "fields": [
            {"id": "a", "label": "Dividend (a)", "default": -157},
            {"id": "b", "label": "Divisor (b)", "default": 23}
        ]
    },

    "divisibility": {
        "name": "Divisibility",
        "description": "Determine whether a divides b. In other words, whether b = ak for some integer k.",
        "fields": [
            {"id": "a", "label": "Divisor (a)", "default": 7},
            {"id": "b", "label": "Number (b)", "default": 84}
        ]
    },

    "extended_gcd": {
        "name": "Extended Euclidean Algorithm",
        "description": "Find gcd(a, b) and integers x and y such that gcd(a, b) = ax + by.",
        "fields": [
            {"id": "a", "label": "First Integer", "default": 252},
            {"id": "b", "label": "Second Integer", "default": 198}
        ]
    },

    "binomial_coefficient": {
        "name": "Binomial Coefficient",
        "description": "Calculate the binomial coefficient C(n, k), also written as n choose k.",
        "fields": [
            {"id": "n", "label": "n", "default": 8},
            {"id": "k", "label": "k", "default": 5}
        ]
    },

    "binomial_term": {
        "name": "Binomial Expansion Term",
        "description": "Find the coefficient of x^k in the expansion of (ax + b)^n.",
        "fields": [
            {"id": "n", "label": "Exponent (n)", "default": 8},
            {"id": "k", "label": "Power of x (k)", "default": 5},
            {"id": "a", "label": "Coefficient of x (a)", "default": 2},
            {"id": "b", "label": "Constant (b)", "default": -3}
        ]
    }, 

    "linear_congruence": {
        "name": "Linear Congruence",
        "description": "Solve ax ≡ b (mod m). A solution exists exactly when gcd(a, m) divides b. The calculator returns every distinct solution modulo m.",
        "fields": [
            {"id": "a", "label": "Coefficient (a)", "default": 6},
            {"id": "b", "label": "Right-hand Side (b)", "default": 8},
            {"id": "m", "label": "Modulus (m)", "default": 14}
        ]
    }, 
}

#export function
def calculate_number_theory(operation: str, values: dict):
    formula = NUMBER_THEORY_FORMULAS.get(operation)

    if formula is None:
        raise ValueError("Unknown number theory operation.")

    fields = formula["fields"]

    try:
        args = [int(values[field]) for field in fields]
    except (KeyError, TypeError, ValueError):
        raise ValueError("Please provide valid integer inputs.")

    return formula["function"](*args)
