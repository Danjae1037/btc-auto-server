def calculate_return_rate(entry_price, exit_price):
    return (exit_price / entry_price) - 1

def format_percentage(rate):
    return f"{rate*100:.2f}%"
