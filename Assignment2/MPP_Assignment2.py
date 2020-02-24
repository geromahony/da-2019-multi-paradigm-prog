# This function sums an array of 
# numbers [1, ..... n].
# # 
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
# of the one element array.
# As the recursion function returns up
# the recursive call stack it sums the
# array as: 
# sum[n]
# sum[n-1,n]
# sum[n-2,n-1,n]
# sum[n-n,....,n-2,n-1,n]

def sumArray(array):
	# stop condition
	# array of one entry length
	if len(array) == 1:
		return array[0]
	else:
		return array[0] + sumArray(array[1:])


a = [1, 4, 6, 9, 23, 5, 2, 3]

print(sumArray(a))