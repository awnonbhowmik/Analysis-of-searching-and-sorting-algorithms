def swap(a, i, j):
    if i != j:
        a[i], a[j] = a[j], a[i]


def bubblesort(a):
    if len(a) == 1:
        return

    swapped = True
    for i in range(len(a) - 1):
        if not swapped:
            break
        swapped = False
        for j in range(len(a) - 1 - i):
            if a[j] > a[j + 1]:
                swap(a, j, j + 1)
                swapped = True
            yield a


def insertionsort(a):
    for i in range(1, len(a)):
        j = i
        while j > 0 and a[j] < a[j - 1]:
            swap(a, j, j - 1)
            j -= 1
            yield a


def mergesort(a, start, end):
    if end <= start:
        return

    mid = start + ((end - start + 1) // 2) - 1
    yield from mergesort(a, start, mid)
    yield from mergesort(a, mid + 1, end)
    yield from merge(a, start, mid, end)
    yield a


def merge(a, start, mid, end):
    merged = []
    left = start
    right = mid + 1

    while left <= mid and right <= end:
        if a[left] < a[right]:
            merged.append(a[left])
            left += 1
        else:
            merged.append(a[right])
            right += 1

    while left <= mid:
        merged.append(a[left])
        left += 1

    while right <= end:
        merged.append(a[right])
        right += 1

    for i, sorted_val in enumerate(merged):
        a[start + i] = sorted_val
        yield a


def quicksort(a, start, end):
    if start >= end:
        return

    pivot = a[end]
    pivot = start

    for i in range(start, end):
        if a[i] < pivot:
            swap(a, i, pivot)
            pivot += 1
        yield a
    swap(a, end, pivot)
    yield a

    yield from quicksort(a, start, pivot - 1)
    yield from quicksort(a, pivot + 1, end)


def selectionsort(a):
    if len(a) == 1:
        return

    for i in range(len(a)):
        minVal = a[i]
        minIdx = i
        for j in range(i, len(A)):
            if a[j] < minVal:
                minVal = a[j]
                minIdx = j
            yield a
        swap(a, i, minIdx)
        yield a
