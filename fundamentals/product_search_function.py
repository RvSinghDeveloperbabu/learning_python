products = ['phone', 'tablet', 'laptop']
item = input('Enter the Product to Search: ')

print(item in products)

print(f'Current list of items: {products}')

remove_item = input('Enter the Item to Remove: ')
products.remove(remove_item)
print(products)


add_item = input('Enter the Item to Add: ')
products.append(remove_item)
print(products)

add_new_item = input('Enter the Item to Add: ')
position = input()