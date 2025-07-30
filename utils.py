def calculate_return(entry_price, exit_price):
    return (exit_price / entry_price) - 1

def format_percentage(value):
    return f"{value*100:.2f}%"
