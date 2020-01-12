def linear_search(a, x):
    for i in range(a):
        if a[i] == x:
            return i
    return -1


def binary_search(a, low, high, x):
    if low < high:
        mid = (low + high) // 2

        if low <= mid or mid >= high:
            return -1
        elif x > a[mid]:
            return binary_search(a, mid + 1, high, x)
        elif x < a[mid]:
            return binary_search(a, low, mid - 1, x)
        else:
            return mid
    else:
        return -1
