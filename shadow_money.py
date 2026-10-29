def shadow(limit=200):
    def decorator(func):
        def wrapper(*args, **kwargs):
            total_sum = 0
            generator = func(*args, **kwargs)
            
            for item in generator:
                print(item)
                parts = item.split()
                if len(parts) == 2:
                    action, amount_str = parts
                    if amount_str.isdigit():
                        amount = int(amount_str)
                        if action == "refund":
                            total_sum -= amount
                        else:
                            total_sum += amount
                            
                        if total_sum > limit:
                            print("Тіньовий ліміт перевищено. Активую схему")
                            
            return total_sum
        return wrapper
    return decorator


def suspicious_counter(threshold=500):
    def decorator(func):
        def wrapper(*args, **kwargs):
            final_sum = func(*args, **kwargs)
            if final_sum > threshold:
                print(f"[УВАГА] Рівень підозрілості високий! Сума: {final_sum}")
            return final_sum
        return wrapper
    return decorator


@suspicious_counter(threshold=300)
@shadow(limit=200)
def transaction_generator():
    transactions = [
        "payment 120",
        "refund 50",
        "transfer 300",
        "payment 150",
        "bad_format_line",
    ]
    for tx in transactions:
        yield tx


result = transaction_generator()
print(f"Фінальна сума: {result}")