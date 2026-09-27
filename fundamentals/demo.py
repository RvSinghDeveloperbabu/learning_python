# one way to import the module functions
# import module
#
# module.hello()
# module.bye()

# from module import *  ## It will import all the function by doing this we can directly call the functions

from module import hello, bye

hello()
bye()

import random
print(random.randint(1,10))


import datetime
print(datetime.datetime.now())
print(datetime.date.today())


