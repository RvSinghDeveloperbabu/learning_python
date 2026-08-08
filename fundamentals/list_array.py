people = ['Ravi','Rahul', 'Sam','Mike']

print('Accessed by index position:',people[1])

for name in people:
  print(name)


any_type_data=[1,3,4.5,5.2,'ravi', True]

print(any_type_data)

# negative indexing it start from -1,-2...-n

print(any_type_data[-1])


#list slicing
print(any_type_data[0:3])

#list slicing
print(any_type_data[0:13])

print(any_type_data[-3:0])
print(any_type_data[-3:-1])
print(any_type_data[-3:])

# in function
print('In function' ,'Ravi' in people)

# not in function
print('not in function', 'Ravi' not in people)

# length of list
print('Length of list:',len(people))

#insert function
people.insert(2,'Rashmi')
print(people)

# append
people.append('Hello')
print(people)

people.append(['Suman','Radha'])
print(people)

#extend
people.extend(['Suman','Radha'])
print(people)

#remove
people.remove(['Suman','Radha'])
print(people)

# people.remove('test')
# print(people)

#pop
people.pop()
print(people)

#index
print(people.index('Rahul'))

numbers = [1,5,3,34,64,345,34,55]
#max
print(max(numbers))
#min
print(min(numbers))
#sum
print(sum(numbers))

#duplication
numbers_b = [5,6,19,20,45,41]
print(numbers + numbers_b)
numbers_b = [5,6,19,20,45,41]
print(numbers_b*3)
