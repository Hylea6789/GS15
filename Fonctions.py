import random


def exponentiation_rapide(a: int, e: int, p: int) -> int:
    """
    Calcul a^e mod p avec l'exponentiation rapide
    """
    a_pow: int = a
    p_bin = format(e, 'b')[::-1]  # Converti e en binaire et l'inverse
    resultat = a if p_bin[0] == '1' else 1
    for i in p_bin[1:]:  # converti le nombre e en binaire et l'inverse
        a_pow = a_pow * a_pow % p
        if i == '1':
            resultat = (resultat * a_pow) % p
    return resultat


def rabbin_miller(p: int, a: int) -> bool:
    """
    Effectue le test de Rabbin Miller sur un nombre p
    Calcul de s et d tel que p = (2^s)*d+1
    On calcul a^d mod p. On vérifie si a^d = 1 mod p
    On calcule les a^(2^r) mod p successifs.
    Pour chacun d'entre eux, on vérifie que a^(2^r)*a^d = -1
    :param p: le nombre dont on veut tester la parité
    :param a:
    :return: True si p est pair, sinon False
    """
    if (p % 2 == 0) or (p == 1):
        return False
    s: int = 1
    diviseur: int = 2

    # Calcul de s et d tel que p = (2^s)*d+1
    while (p - 1) % (diviseur * 2) == 0:
        s += 1
        diviseur *= 2
    d = (p - 1) // diviseur

    a_d = exponentiation_rapide(a, d, p)  # calcule a^d mod p
    if a_d == 1:  # si a^d = 1 mod p
        return True
    a_pow: int = a_d
    if (s - 1) == 0:  # range(0) donne un tableau vide, on doit l'initialiser manuellement dans ce cas
        liste_r = [0]
    else:
        liste_r = range(s - 1)

    for _ in liste_r:
        if a_pow == p - 1:
            return True
        a_pow = (a_pow * a_pow) % p
    return False


def rabbin_miller_boucle(nb_premier: int) -> bool:
    def get_a():
        a = random.randint(1, nb_premier)
        while (a % nb_premier) == 0:
            a = random.randint(1, nb_premier)
        return a
    return all(rabbin_miller(nb_premier, get_a()) for _ in range(10))


def gen_nbr_premier(max_bound: int) -> int:
    """
    génère un nombre premier plus petit que max_bound
    """
    nb_premier: int
    while True:
        nb_premier = random.randint(3, max_bound)
        if rabbin_miller_boucle(nb_premier):
            return nb_premier


def gen_nbr_premier_produit(bit_max: int) -> tuple[int, int]:
    """
    Génère un nombre premier p tel que p-1 soit le produit de n nombres premier
    :param bit_max: le nombre de bit sur lequel est écrit le nombre premier.
    """

    # On soustrait 1 car on multiplie le nombre p-1 par 2 (pour s'assurer qu'il est pair)
    bit_max -= 1
    max_bound = 2 ** bit_max

    while True:
        p_facteur = gen_nbr_premier(max_bound)
        p = 2 * p_facteur + 1
        est_premier = rabbin_miller_boucle(p)
        if est_premier:
            return p, p_facteur


def generateur_facteur(p: int, p_facteur: int):
    """
    Calule l'élément générateur à partir du théorème de Lagrange
    """
    while True:
        g: int = random.randint(1, p - 1)
        resultat1 = exponentiation_rapide(g, 2, p)
        resultat2 = exponentiation_rapide(g, p_facteur, p)
        if (resultat1 != 1) and (resultat2 != 1):
            return g
