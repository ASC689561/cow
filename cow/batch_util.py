
def batch(iterable, n=1):
    """
    Nhóm iterable theo batch
    :param iterable:
    :param n: batch_size
    """
    current_batch = []
    for item in iterable:
        current_batch.append(item)
        if len(current_batch) == n:
            yield current_batch
            current_batch = []
    if current_batch:
        yield current_batch
