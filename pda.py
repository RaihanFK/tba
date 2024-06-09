import dfa

def tokenize(html: str) -> list[str]:
    html = html.strip()
    tokens = []

    while html:
        html = html[html.find('<'):]
        tag = html[:html.find('>')+1]

        if not dfa.matches(tag):
            return []

        tokens.append(tag)
        html = html[html.find('>')+1:]

    return tokens

pt = {
    'S': [
        ["<html>", 'A', "</html>"]
    ],
    'A': [
        ["<head>", 'B', "</head>", 'C' ],
        ["<body>", 'D', "</body>"],
        [""]
    ],
    'B': [
        ["<title>", "</title>"],
        [""]
    ],
    'C': [
        ["<body>", 'D', "</body>"],
        [""]
    ],
    'D': [
        ["<h1>", 'D', "</h1>"],
        ["<p>", 'D', "</p>"],
        [""]
    ],
}

def has_epsilon(alpha: str) -> bool:
    global pt
    return pt[alpha][-1][0] == ""

def is_alpha(x: str) -> bool:
    global pt
    return x in pt

def find_product(alpha: str, token: str) -> list[str]:
    global pt

    for product in pt[alpha]:
        if product[0] == token:
            return product
    
    return []

def next_alpha(alpha_before: str, product: list[str]):
    for p in product:
        if is_alpha(p):
            return p

    return alpha_before

def matches(html):
    stack = ['#']
    alpha = 'S'
    i = 1

    tokens = tokenize(html)
    if not tokens: return False

    product = find_product(alpha, tokens[0])
    if not product: return False

    alpha = next_alpha(alpha, product)
    stack.extend(reversed(product[1:]))

    while i < len(tokens):
        current_str = tokens[i]
        top = stack.pop()

        if is_alpha(top):
            product = find_product(top, current_str)

            if not product and has_epsilon(top):
                # current / tokens[i] := </h1>
                # stack               := [... </h1> epsilon
                #                             ^ should always be it's tag closer
                if stack.pop() != current_str:
                    return False
                
                i += 1
                continue

            if not product:
                return False

            alpha = next_alpha(alpha, product)
            stack.extend(reversed(product))
            continue

        if top == current_str:
            i += 1
            continue

        product = find_product(alpha, current_str)
        if not product and top != current_str: return False

        stack.append(top)
        stack.extend(reversed(product[1:]))
        i += 1

    return stack.pop() == '#'

for n, expected in enumerate([True, False, True, False, False, False], start=1):
    with open(f"html/{n}.html", "r") as f:
        html = f.read()
        f.close()

        assert matches(html) == expected
