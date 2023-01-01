from utils import exponentiation_rapide


class RatchetKey:
    """
    Clé symétrique Rachet mise à jour régulièrement
    """
    SIZE = 2048

    def __init__(self, cle_chainee):
        self._cle_chainee = cle_chainee
        self._cle_message = 0

    def fonction_derivation(self):
        """
        cle_chainee(n + 1) = cle_chainee(n) * cle_chainee(n)
        cle_message(n + 1) = cle_chainee(n) * cle_chainee(n + 1)
        """
        cle_chainee_suivante = self._cle_chainee * self._cle_chainee % pow(2, RatchetKey.SIZE)

        self._cle_message = cle_chainee_suivante * self._cle_chainee % pow(2, RatchetKey.SIZE)
        self._cle_chainee = cle_chainee_suivante

    @property
    def cle_message(self):
        return self._cle_message

    @property
    def cle_chainee(self):
        return self._cle_chainee
