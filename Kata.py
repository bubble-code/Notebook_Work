def paridad(integers):
    parid = [n%2 for n in integers[:3]]
    cpar = 1 if sum(parid)<2 else 0
    for x in integers:
        if x %2 == cpar:
            return x

print(paridad([21, 4, 13, 11, 45, 19, 2607, 35]))