from OSRSBytes import Items

items = Items()

# Lets get information on this item
print('Is Members:',    items.isMembers('rune dagger'))
print("Item ID:",         items.getItemID('rune dagger'))

print('Sell Average:',  items.getSellAverage('rune dagger'))
print('Sell Quantity:', items.getSellQuantity('rune dagger'))

print('Buy Average:',  items.getBuyAverage('rune dagger'))
print('Buy Quantity:', items.getBuyQuantity('rune dagger'))
print('Buy Limit:',    items.getBuyLimit('fire rune'))

print('Shop Price:',      items.getShopPrice('rune dagger'))
print('High Alch Value:', items.getHighAlchValue('rune dagger'))
print('Low Alch Value:',  items.getLowAlchValue('rune dagger'))

# In addition, all items can be called by Item ID as well
print('Item Name:',       items.getName('1213'))
print('Sell Average:',    items.getSellAverage('1213'))


# Lets get some new, up-to-date information
print('Sell Average:', items.getSellAverage('rune dagger'))
