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
        ["<h1>", 'D', "</h1>", 'D'],
        ["<p>", 'D', "</p>", 'D'],
        [""]
    ],
}

def has_epsilon(alpha: str) -> bool:
    global pt

    for prod in pt[alpha]:
        if prod[0] == "":
            return True

    return False

def is_alpha(x: str) -> bool:
    global pt
    return x in pt

def find_product(alpha: str, token: str) -> list[str]:
    global pt

    for product in pt[alpha]:
        if product[0] == token:
            return product

    return []

def push_product(stack: list[str], product: list[str]) -> None:
    for p in product[::-1]:
        stack.append(p)

def matches(html: str) -> bool:
    tokens = tokenize(html)

    stack = ['#', 'S']
    i = 0

    while i < len(tokens):
        tok = tokens[i]
        top = stack.pop()

        if is_alpha(top):
            product = find_product(top, tok)
            push_product(stack, product)

            if not product and not has_epsilon(top): return False
            continue

        if top != tok: return False
        i += 1

    return stack.pop() == '#'

for n, expected in enumerate([True, False, True, False, False, False, True, True], start=1):
    with open(f"html/{n}.html", "r") as f:
        html = f.read()
        f.close()

        assert matches(html) == expected
