'''
set is the datatype which have unique values.
it's looks like the list.
set is also ordered values.
'''

names = {'jimi', 'jerry','ajay','rahul','ravi'}
numbers =  set([1,2,3,4,5,6])

print(names)
print(numbers)

# empty set
empty =set()
print(empty)
print(type(empty))

# set operations
print('ravi' in names)
print('jay' in names)


numbers_b = {4,5,6,7,8,9}

#union
print(numbers | numbers_b)
#intersection
print(numbers & numbers_b)
#difference operation
print(numbers - numbers_b)
#Symmetric difference: removed the common elements
print(numbers ^ numbers_b)

#Add
numbers.add(10)
print(numbers)

#remove
numbers.remove(10)

# numbers.remove(11) give error when the value is not exist.
print(numbers)

# discard
numbers.discard(6)
numbers.discard(16)
print(numbers)

#pop
poped_number = numbers.pop()
print(poped_number)
print(numbers)

#clear
numbers.clear()
print(numbers)