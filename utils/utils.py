def format_price(val):
    return f'US$ {val:.2f}'

def cart_total_qty(cart):
    return sum([item['amount'] for item in cart.values()])

def cart_totals(cart):
    return sum([
        item.get('price_quantitative_promotional') 
        if item.get('price_quantitative_promotional')
        else item.get('price_quantitative')
        for item 
        in cart.values()
    ])