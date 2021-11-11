# Author: Zachary Wong
# Date: 8/18/2020
# Purpose: Write a sort function using the quick sort algorithm


# Comparison function for integers

def compare_int(a, b):
    return a <= b


# Comparison function for strings

def compare_str(a, b):
    return a.lower() <= b.lower()


# A function that inputs a specific comparison function and returns which parameter is smaller than the other

def do_it(compare_func, x, y):

    if compare_func(x, y):
       # print(x, "is less than", y)
        return True
    else:
        # print(y, "is less than", x)
        return False


# A helper function to swap elements in the list called in the partition function

def swap(the_list, i, j):
    temp = the_list[i]
    the_list[i] = the_list[j]
    the_list[j] = temp


# Assigns the pivot in the sublist and returns the index of the pivot where all numbers to its left is smaller
# and all numbers to its right are bigger. It takes the sublist, first and last indexes of the sublist,
# and the comparison function as parameters.

def partition(the_list, p, r, compare_func):
    pivot = the_list[r]
    i = p-1
    j = p
    while j < r:
        if compare_func(the_list[j], pivot):
            i += 1
            swap(the_list, i, j)
        j += 1
    swap(the_list, i + 1, r)
    return i + 1


# A function that calls the partition function on each sublist within the entire list. It takes the list, first
# and last indexes of the list, and the comparison function as parameters.

def quicksort(the_list, p, r, compare_func):
    if p < r:
        q = partition(the_list, p, r, compare_func)
        quicksort(the_list, p, q-1, compare_func)
        quicksort(the_list, q+1, r, compare_func)
        return the_list


# A function that calls quicksort and inputs the first and last indexes of the list as p and r in quicksort.

def sort(the_list, compare_func):
    output = quicksort(the_list, 0, len(the_list)-1, compare_func)
    return output





