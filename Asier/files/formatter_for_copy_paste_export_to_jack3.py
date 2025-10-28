def format_list_of_arrays(arrays):
    """
    Converts a list of arrays (lists of numbers) into a formatted string representation.
    
    Args:
        arrays (list of list of int/float): A list where each element is an array (list of numbers).
    
    Returns:
        str: A string representation of the arrays in the format:
             "list('[1, 2]', '[3, 4]')"
    
    Example:
        >>> format_list_of_arrays([[1, 2], [3, 4]])
        "list('[1, 2]', '[3, 4]')"
    """
    return 'list(' + ', '.join([f"'[{', '.join(map(str, array))}]'" for array in arrays]) + ')'

def format_list_of_strings(strings):
    """
    Formats a list of strings into a specific string representation.
    
    Args:
        strings (list of str): A list of strings to be formatted.
    
    Returns:
        str: A string representation of the list in the format:
             "list('a', 'b', 'c')"
    
    Example:
        >>> format_list_of_strings(['a', 'b', 'c'])
        "list('a', 'b', 'c')"
    """
    return 'list(' + ', '.join([f"'{s}'" for s in strings]) + ')'

def format_list_of_integers(integers):
    """
    Formats a list of integers into a specific string representation.
    
    Args:
        integers (list of int): A list of integers to be formatted.
    
    Returns:
        str: A string representation of the list in the format:
             "list(1, 2, 3)"
    
    Example:
        >>> format_list_of_integers([1, 2, 3])
        "list(1, 2, 3)"
    """
    return 'list(' + ', '.join(map(str, integers)) + ')'


def format_list_of_intervals(intervals):
    """
    Formats a list of intervals (list of tuples) into a formatted string representation.
    
    Args:
        intervals (list of list of tuple): A list where each element is a list of tuples representing intervals.
    
    Returns:
        str: A string representation of the intervals in the format:
             "list('1,2,3,4', '5,6,7,8')"
    
    Example:
        >>> format_list_of_intervals([[(1, 2), (3, 4)], [(5, 6), (7, 8)]])
        "list('1,2,3,4', '5,6,7,8')"
    """
    return 'list(' + ', '.join(
        ["'" + ','.join(f"{x},{y}" for x, y in group) + "'" for group in intervals]
    ) + ')'

def format_list_of_lists_of_strings(lists):
    """
    Formats a list of lists of strings into a specific string representation.
    
    Args:
        lists (list of list of str): A list where each element is a list of strings.
    
    Returns:
        str: A string representation of the lists in the format:
             "list('a,b,c', 'd,e,f')"
    
    Example:
        >>> format_list_of_lists_of_strings([['a', 'b', 'c'], ['d', 'e', 'f']])
        "list('a,b,c', 'd,e,f')"
    """
    return 'list(' + ', '.join([f"'{','.join(map(str, lst))}'" for lst in lists]) + ')'

def format_list_of_values(values):
    """
    Formats a list of scalar values into a formatted string representation.
    
    Args:
        values (list of int/float/str): A list of scalar values (e.g., integers, floats, strings).
    
    Returns:
        str: A string representation of the values in the format:
             "list(1', '2', '3')"
    
    Example:
        >>> format_list_of_values([1, 2, 3])
        "list(1', '2', '3')"
    """
    return 'list(' + ', '.join([f"{v}" for v in values]) + ')'
