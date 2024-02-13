def format_price(val):
    return f'US$ {val:.2f}'

def cart_total_qty(cart):
    return sum([item['amount'] for item in cart.values()])