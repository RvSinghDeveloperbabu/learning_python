'''
Tuples are data structures which are similar to lists,
but the major difference between a list and a tuple is that lists are mutable,
which means you could change the contents of a list.
However, you cannot change the content of a tuple once the tuple is declared.
'''

people = ('Ravi', 'Rashmi', 'Vijay', 'Ruchi', 'Suman')

print(people)
print(people[1])

## Type error we get. it immutable.
# people[1] = 'Rahul'

#slice
print(people[1:3])

# -ev indexing
print(people[-1])