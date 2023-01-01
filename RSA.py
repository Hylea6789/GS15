from prime_numbers import gen_nbr_premier
from utils import inverse, exponentiation_rapide


def parametre_rsa() -> tuple[int, int, int]:
    """
    Calcul des clés pour rsa
    On génère d'abord p et q premiers qui permettent de déterminer la premier clé n
    Puis on calcul phi et e premier à phi
    n et e sont les clés publiques
    On calcule alors d inverse de e mod phi
    d est la clé secrète"""
    p: int = 120877918482540368743824706748115473639820104245486721086655514775674663101382471591933941218764611662154561102143981501112226323077389982467906837735641384870195766777388872176992003111937256114221632839502641245520456389357038874824302292301025729098051849491021167786247259529421846351170444553506026737079
    q: int = 156846740033582598360587784105027657768402411009914113187252891608877283849836891932291370500271520218415766897310352692636387130651237364114946004715508141566339590153478339709742590300188182777141857939575330245801964240155137313958012035559233959486055480063879048541977389168391692508230790638580090576607
    n = p * q
    phi = (p - 1) * (q - 1)
    e: int = gen_nbr_premier(phi)
    d = inverse(e, phi)
    return n, e, d


def signature_rsa(m: int):
    n, e, d = parametre_rsa()
    sigM: int = exponentiation_rapide(m, d, n)  # signature d'une clé/message
    return sigM


def verification_rsa(sig_m: int, m: int, e: int, n: int):
    verif_m: int = exponentiation_rapide(sig_m, e, n)  # verification de la signature
    return verif_m == m
