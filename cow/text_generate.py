def __p(text, dic):
    for k, v in dic.items():
        for r in v:
            text1 = text.replace(k, r)

            d1 = dic.copy()
            d1.pop(k)
            if len(d1) > 0:
                for xx in __p(text1, d1):
                    yield xx
            else:
                yield text1


def generate_permutation(text):
    import re
    all_p = list(re.finditer('\((.*?)\)', text, re.MULTILINE))
    d = {}
    if len(all_p) == 0:
        yield text
    for k in all_p:
        match_str = text[k.span()[0]:k.span()[1]]
        d[match_str] = match_str.replace('(', '').replace(')', '').split('|')

    for k in __p(text, d):
        while '  ' in k:
            k = k.replace('  ', ' ')
        k = k.strip()
        yield k
