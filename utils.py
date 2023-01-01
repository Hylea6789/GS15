import math


def bourrage_zero(nbr_bin: str | int, size: int) -> str:
    """
    Prend en argument un nombre ou sa représentation binaire
    et renvoie sa représentation binaire, en ajoutant si
    nécessaire des 0 comme bits de poids forts pour que
    le résultat ait exactement `size` bits.
    """
    if isinstance(nbr_bin, int):
        nbr_bin = format(nbr_bin, "b")
    else:
        try:
            int(nbr_bin, 2)
        except ValueError:
            raise ValueError("nbr_bin must be in binary format")
    return nbr_bin.zfill(size)


def exponentiation_rapide(a: int, e: int, p: int) -> int:
    """
    Calcul a^e mod p avec l'exponentiation rapide
    """
    a_pow: int = a
    p_bin = format(e, "b")[::-1]  # Convertit e en binaire et l'inverse
    resultat = a if p_bin[0] == "1" else 1
    for i in p_bin[1:]:  # convertit le nombre e en binaire et l'inverse
        a_pow = a_pow * a_pow % p
        if i == "1":
            resultat = (resultat * a_pow) % p
    return resultat


def bezout(a: int, b: int):
    x0: int = 1
    x1: int = 0
    y0: int = 0
    y1: int = 1
    i: int = 0
    r0 = max(a, b)
    r1 = min(a, b)
    while r1 > 0:
        i += 1
        q = r0 // r1
        r0, r1 = r1, r0 - q * r1
        x0, x1 = x1, q * x1 + x0
        y0, y1 = y1, q * y1 + y0
    if i % 2 == 0:
        y0 *= -1
    else:
        x0 *= -1
    if a >= b:
        return x0, y0
    else:
        return y0, x0


def inverse(a: int, m: int):
    if math.gcd(a, m) != 1:
        x, y = bezout(a, m)
    return x
