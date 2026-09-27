
def hello(i):
  print('Hello World', i)

for i in range(0,5):
  hello(i)


#keyword arguments
def speed(distance, time):
  print(distance/time)

## call the function with arguments with this position on argument does not matter
speed(distance=100,time=2)
speed(time=2,distance=100)

## Pass the default value in the function argument
def area(radius, pi=3.14):
  print(radius**2 * pi)

area(radius=100,pi=3.14)
area(radius=100)


## How to  return the values from the functions.
def area(radius, pi=3.14):
  return radius**2 * pi

print(f"Area: {area(radius=100, pi=3.14)}")

## returning the multiple values from the function.
def circle(radius):
  area_c = area(radius)
  circumference = 2 * 3.14 * radius
  return area_c, circumference
a,c = circle(radius=100)
print(f"Area: {a} ; Circumference: {c}")

count = 10 ## Global Variable
def g_add():
  count = 30  ## Local variable
  print( "variables:" ,count)

g_add()