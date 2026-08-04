#Example 1

a = int(input('Enter a number: ' ))
b = int(input('Enter another number: '))

print("Sum of the numbers is: ", a+b)

#Example 2
first_name= input('Enter your first name: ')
last_name = input('Enter your last name: ')

print('Username is ' + first_name + last_name)
print('Email is ' + first_name + last_name + '@gmail.com')


#Example 3
saved_password = 'Test@123#'
entered_password = input('Enter your password: ')

print(saved_password == entered_password)
if saved_password == entered_password:
  print('Welcome back !')
else:
  print('incorrect password !')