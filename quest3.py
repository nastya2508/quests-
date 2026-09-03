raw_input = input("Введіть вираз: ").strip()

if raw_input.endswith("="):
    raw_input = raw_input[:-1]

expr = raw_input.replace(" ", "")


def calculate_no_brackets(s):
    tokens = []
    curr = ""
    for ch in s:
        if ch in "+-*/":
            if curr:
                tokens.append(float(curr))
                curr = ""
            tokens.append(ch)
        else:
            curr += ch
    if curr:
        tokens.append(float(curr))

    i = 0
    while i < len(tokens):
        if tokens[i] in ("*", "/"):
            op = tokens[i]
            left = tokens[i - 1]
            right = tokens[i + 1]
            if op == "/" and right == 0:
                print("Помилка: ділення на нуль!")
                exit()
            res = left * right if op == "*" else left / right
            tokens[i - 1 : i + 2] = [res]
            i -= 1
        else:
            i += 1

    i = 0
    while i < len(tokens):
        if tokens[i] in ("+", "-"):
            op = tokens[i]
            left = tokens[i - 1]
            right = tokens[i + 1]
            res = left + right if op == "+" else left - right
            tokens[i - 1 : i + 2] = [res]
            i -= 1
        else:
            i += 1

    return tokens[0]


while "(" in expr:
    right = expr.find(")")
    left = expr.rfind("(", 0, right)
    sub = expr[left + 1 : right]
    tokens_res = calculate_no_brackets(sub)
    expr = expr[:left] + str(tokens_res) + expr[right + 1 :]

total = calculate_no_brackets(expr)
print("Результат:", total)