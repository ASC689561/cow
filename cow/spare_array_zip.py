import math


def zip_spare_array(arr):
    for v in range(0, len(arr)):
        arr[v] = (arr[v], 1)
    v = 0
    while v < len(arr) - 1:
        if arr[v][0] == arr[v + 1][0] or (math.isnan(arr[v][0]) and math.isnan(arr[v + 1][0])):  # same value
            arr[v] = (arr[v][0], arr[v][1] + 1)
            arr.pop(v + 1)
            continue
        else:
            v += 1

    for v in range(0, len(arr)):
        if arr[v][1] == 1:
            arr[v] = arr[v][0]

    return arr
