def decorator(func):
  def wrapper(*args):
    print("wrapper before function")
    func(*args)
    print("wrapper after function")

  return wrapper

def chocolate():
  print("chocolate")

## One way of wrapper function to call
decorator(chocolate)()

## Another way or better to use the wrapper function.
@decorator
def hello(name):
  print(f"Hello! I am inside wrapper, {name}")

hello("Ravi")



## Decorator which return the values

def summer_discount_decorator(func):
  def wrapper(price):
    func(price)
    return func(price/2)
  return wrapper

@summer_discount_decorator
def total(price):
  return price

print(total(100))

