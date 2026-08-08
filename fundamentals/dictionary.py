'''
Python is nothing but essentially a data structure similar to LIST,
but you could say that a dictionary is sort of a more comprehensive data structure where you
can store more complex data as compared to a List.
{key: value}
'''

people = {'Ravi': 32, "rashmi": 29}
print(people)
print(f'Age of Ravi is {people['Ravi']}\n')

people['rashmi'] = 35
print(people)

people_id = {1: 'Ford', 2: 'walton'}
print(people_id[1])


## Inbuilt function
people_names = dict(
  rashmi=35,
  ravi=29,
  jay=1.5
)

# Add
people_names['paras'] = 1.5
print(people_names)

#delete
del people_names['jay']
print(people_names)

#get method is used to handle the missing key error it will return none.
print(people_names.get('ravi'))
print(people_names.get('jay'))

new_people_names = {'rahul': 43, 'vijay': 40, 'ravi': 31}
#update method
people_names.update(new_people_names)
print(people_names)

#pop
name = people_names.pop('rahul')
print(people_names)
print(f'this user is deleted {name}')

#get all values and keys from the dictionary
print(people_names.values())
print(people_names.keys())

#get dict in to list
print(people_names.items())