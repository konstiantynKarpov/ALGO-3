def uniform_binary_search(sorted_keys, target):
    low = 0
    high = len(sorted_keys) - 1
    comparisons = 0

    while low <= high:
        mid = (low + high) // 2
        comparisons += 1
        if sorted_keys[mid] == target:
            return mid, comparisons
        elif sorted_keys[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return None, comparisons
