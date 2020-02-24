# Data Analytics - Multi-Paradigm Programming
# Gerard O'Mahony G00364737@gmit.ie
#
# Written in Python 3.7.3
# 12.12.2019

from functools import reduce

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Q1. Sum of an array. Given an array of numbers
# return it’s sum (all the numbers addedtogether).
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# This function sums an array of
# numbers [1, ..... ,n].
#
# It does this by recursivly slicing
# the array in sucessive calls to
# itself, reducing the array by the
# first entry and passing itself the
# remaining array working down to the
# base case.

# The base case is when the array is
# reduced down to either one or no elements.
# The array length could be zero and returns
# zero or once the array has only one element
# return the value of that element as the sum
# of that one element array.

# As the recursion function returns up
# the recursive call stack it sums the
# array as:

# [n]
# [n-1 + n]
# [n-2 + (n-1 + n)]
# [n-n + .... (n-2 + n-1 + n)]

def sumArray(array):
    # stop condition
    # array of one entry length
    if len(array) == 1:
        return array[0]
    else:
        #                 pass array slice
        #                 to itself [1=>n]
        #                 progressivly reducing
        #                 array by removing [0]
        #                 at each recursive call
        return array[0] + sumArray(array[1:])

sum_arr = [1, 4, 6, 9, 23, 5, 2, 3]

result = reduce((lambda x, y: x + y), sum_arr)

if sumArray(sum_arr) == result:
    print("Array is summed")
else:
    print("Array is not summed")


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Q2. Product of an array. Given an array
# of numbers return it’s product
# (all the numbers multiplied together).
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# This function works the same as the previous one
# Works toward the base case by passing sucessive
# slices of the array to itself until the base case
# of a one element array is reached. removing the
# first element in the array [0] by passing [1=>n]
#
# As the recursion function returns up
# the recursive call stack it multiplies the
# array as:

# [n]
# [n-1 x n]
# [n-2 x (n-1 x n)]
# [n-n x .... (n-2 x n-1 x n)]

def arrayProduct(arr):
    # stop condition
    # array of one entry length
    if len(arr) == 1:
        return arr[0]
    else:
        return arr[0] * arrayProduct(arr[1:])

arr_prod = [2, -5, -8, 12, 4, 2, 75]

result = reduce((lambda x, y: x * y), arr_prod)

if arrayProduct(arr_prod) == result:
    print("Array elements are multiplied")
else:
    print("Array elements are not multiplied")


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Q3. Remove all odd numbers. Given an array of
# numbers return an array with all the odd
# numbers removed.
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# This function works the same as previously
# Works toward the base case by passing sucessive
# slices of the array to itself until the base case
# of an empty array is reached. removing the
# first element in the array [0] by passing [1=>n]
#
# The function uses the intrinsic modulo operator
# denoted by the % division to check if an array
# entry is an odd number. The modulo operation
# returns the remainder of the quotient so an
# odd number will not be evenly divisable by 2

def oddArrayRemove(arr):
    # stop condition
    # Empty list array
    if len(arr) == 0:
        # Return an empty array
        return []
    # Modulo the array entry to
    # check if even and if so
    # return an array with this
    # entry and concatenate
    # the other even array entries
    # as the fuction returns up
    # the recursion stack
    if (arr[0] % 2) == 0:
        return [arr[0]] + oddArrayRemove(arr[1:])
    # Otherwise the arr[0] is an odd number
    # so slice array and pass to self [1=>n]
    return oddArrayRemove(arr[1:])


odd_arr = [3, 1, 3, 4, 5]

print(oddArrayRemove(odd_arr))


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Q4.Remove all even numbers. Given an array of
# numbers return an array with all the even
# numbers removed.
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Exact same operation as the previous function
# except that the modulo is checking for a remainder
# to signify an odd number which is to be retained
# in the output array.

def evenArrayRemove(arr):
    # stop condition
    # Empty list array
    if len(arr) == 0:
        return []
    # Modulo odd: a % b == 1
    if (arr[0] % 2) == 1:
        return [arr[0]] + evenArrayRemove(arr[1:])
    return evenArrayRemove(arr[1:])

even_arr = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13]

print(evenArrayRemove(even_arr))


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Q5. Replace a given character with '*'.
# Given a string, and a character to replace,
# return a string where each occurance of the
# character is replaced with '*'.
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Function passes sucessive slices of the string to
# itself [1=>n]. Checks for the replacement character
# and replaces the fist character if it matches as it
# returns up teh recursion stack concatenating the
# string as it goes.

def replaceChar(string_in, rep_str):
    # stop condition
    # Empty input string
    if string_in == '':
        # return an empty string
        return ''
    # Check if the character matches
    # the character to be replaced
    if (string_in[0] == rep_str):
        # if it matches, return a '*' char and concatenate
        # with the rest of the string
        return '*' + replaceChar(string_in[1:], rep_str)
    # otherwise just return the next part of the string
    # recursivly slicing down the string to the base case
    # zero length string 
    return string_in[0] + replaceChar(string_in[1:], rep_str)

in_str = 'asdfjhdfgodiuert'

print(replaceChar(in_str, 'd'))


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Q6. Find index in array for item.
# Given an array, and an element to search for
# return the index of the element in the array
# or -1 if the element is not present in the array.
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# This function works the same as previously
# Works toward the base case by passing sucessive
# slices of the array to itself until the base case
# is reached. The base case(s) are different this time
# as we need to cater for the fact that the array may
# not contain the element we are looking for. This is
# one base case, where we have progressivly sliced the 
# array, removing the first element in the array [0] 
# by passing [1=>n] checking array[0] against the search
# element. If we reach the end of the array without finding
# the element, we return -1 as required. The second base
# case is where we match the element in the array and return
# zero. The return value is saved in 'ret' and checked to see
# if it's negative. If so, continue to return -1 up the recursive
# stack until done to indicate no element is found.
# The second base case returns up the recursive stack when the 
# element is found. 'ret' becomes the counter for the array elements
# starting at zero for the matched element and returning +1 as it
# returns up the stack for the previous unmatched elements returning
# the index of the matched element as the final count.


def elementIndex(arr, search_str):
    # Base case for no match
    if len(arr) == 0:
        return -1
    # Base case for element match
    elif arr[0] == search_str:
        return 0
    # return value counter
    ret = elementIndex(arr[1:], search_str)

    # Check for no match
    if ret < 0:
        # no match so keep 
        # returning -1
        return ret
    # match case so
    # return += 1 as
    # index counter
    return 1 + ret


#elem_idx = ['a', 'b', 'n', 's', 'g', 'w', 't', 'u', 'r']
elem_idx = [1, 3, 5, 7, 9]

print(elementIndex(elem_idx, 7))

print(elementIndex(elem_idx, 50))


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Q7. Sum of Digits. Given a whole, number such
# as 23, return the sum of the digits in the
# number i.e. 2 + 3 = 5.
# For this would be useful to convert the number
# to a string then break it apart into digits.
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# This function converts the input number passed in
# to a string. This happens the first time as the 
# recursive call to itself passes the truncated 
# string [1=>n] is sucessive slices so is converting
# a string to a string on subsequent calls.
# the base case is an empty string which returns zero.
# As the function returns up the stack it returns the 
# integer value of teh first digit in the string
# which are summed up the stack.

def sumDigits(num):
    # convert to string(first time only)
    num_str = str(num)
    # stop condition
    # Empty input string
    if num_str == '':
        return 0
    else:
        # return the integer value of the single digit
        # therefore summing the return value integers
        # when returning up the recursion stack
        return int(num_str[0]) + sumDigits(num_str[1:])


print(sumDigits(123409864))


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Q8. Print an array. Given an array of integers
# print all the elements one per line.
# This is a little bit different as there is no
# need for a 'return' statement just to print
# and recurse.
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Similar to previous functions. Passes slices of 
# the array to itself in recursive calls, reducing
# array each time until empty array base case printing 
# the first element of the array as it slices it down.

def printArray(arr):
    # stop condition
    # Empty input string
    if len(arr) == 0:
        return ''
    else:
        # Print the first array elemet
        print(arr[0])
        # Pass the array slice[1=>n]
        return printArray(arr[1:])


pa = [1, 5, 6, 9, 7, 3]

printArray(pa)


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Q9. Find the minimum element in an array of
# integers. You can carry some extra information
# through method arguments such as minimum value.
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# This function works the same as previously
# Works toward the base case by passing sucessive
# slices of the array to itself until the base case
# of a one element array is reached. removing the
# first element in the array [0] by passing [1=>n]
#
# The minimum value from the comparison of the min
# value between the neighbouring pairs is returned
# as the function returns up the recursion stack.
# Base case returns last element[n]. Next, 
# return min(n,n-1) = r1
# return min(r1,n-2) = r2
# return min(r2,n-3) ...... always returning the
# lowest value from the pair comparison.
 
def arrayMinVal(arr):
    # Base case of array
    # of one element length
    # return that elemet 
    if len(arr) == 1:
        return arr[0]
    else:
        return min(arr[0], arrayMinVal(arr[1:]))


amv = [3, 5, 8, 7, 4, 6, 9, 1, 2]
amnv = [-1, -3, 5, 4, 8, 6, 3, 9]

print(arrayMinVal(amv))
print(arrayMinVal(amnv))


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Q10. Verify the parentheses. Given a string,
# return true if it is a nesting of zero or more
# pairs of parenthesis, like "(())" or "((()))".
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Function passes sucessive slices of the string to
# itself [1=>n]. Check for brackets in the string
# as it's sliced. Updating a bracket balance counters
# as it calls itself. Lefthand bracket + 1, righthand
# bracket -1. Balanced brackets, balance is zero.
 
def balanceBrackets(string_in, b1=0, b2=0, b3=0):
    # Base case, empty string
    if string_in == '':
        # When the string is empty
        # check if brackets are balanced
        # i.e, lefthand + righthand sum
        # to zero.  
        # Is balance counter equal zero?
        return b1 == b2 == b3 == 0
    # If balance counter is
    # not zero, brackets are unbalanced
    if (b1 or b2 or b3) < 0:
        return False
    # check for lefthand bracket and count in balance counter
    if string_in[0] == "(":
        # Slicing down string [1=>n]
        return balanceBrackets(string_in[1:], b1+1,b2,b3)
    elif string_in[0] == "{":
        # Slicing down string [1=>n]
        return balanceBrackets(string_in[1:], b1, b2+1, b3)
    elif string_in[0] == "[":
        # Slicing down string [1=>n]
        return balanceBrackets(string_in[1:], b1, b2, b3+1)

    # check for righthand bracket and remove from balance counter
    elif string_in[0] == ")":
        # Slicing down string [1=>n]
        return balanceBrackets(string_in[1:], b1-1,b2,b3)
    elif string_in[0] == "}": 
        # Slicing down string [1=>n]
        return balanceBrackets(string_in[1:], b1, b2-1, b3)
    elif string_in[0] == "]":
        # Slicing down string [1=>n]
        return balanceBrackets(string_in[1:], b1, b2, b3-1)

    # No bracket case
    return balanceBrackets(string_in[1:], b1, b2, b3)


print(balanceBrackets('((]]'))
print(balanceBrackets('{[((x+y))'))
print(balanceBrackets('{}{(()[])}'))

print(balanceBrackets('(()))'))
print(balanceBrackets('({({})}(()))'))
