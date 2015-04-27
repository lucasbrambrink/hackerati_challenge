__author__ = 'lb'

def numbers_are_consecutive(slice):
    """
    :param slice: ``list`` of ``int``
    :return: ``bool`` specifying if the slice contains consecutive numbers
    """
    is_ascending = slice[0] + 1 == slice[1]
    item = slice[0]
    for next_item in slice[1:]:
        next_projected_number = item + 1 if is_ascending else item - 1
        if not next_projected_number == next_item:
            return False
        item = next_item
    return True

def find_consecutive_runs(array):
    """
    :param array: ``list`` of ``int``
    :return: ``list`` of indexes marking the start of a ascending- or descending triplet of consecutive integers
    """
    indexes_of_runs = []
    for index in range(len(array) - 3):
        triplet = array[index:index + 3]
        if numbers_are_consecutive(slice=triplet):
            indexes_of_runs.append(index)
    return indexes_of_runs


if __name__ == '__main__':
    example = [1, 2, 3, 5, 10, 9, 8, 9, 10, 11, 7]
    print find_consecutive_runs(example)






