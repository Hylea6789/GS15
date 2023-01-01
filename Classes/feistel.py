"""
Pour la génération de sous-clé de Feistel, on divise la clé d'entrée en N sous-clés.
La taille de la sous-clé correspond à la taille du bloc à chiffrer

PISTE AMELIORATION : Hasher la clé pour qu'elle soit plus petite
"""
from utils import bourrage_zero


# TODO Faire en sorte que (faire en sorte que quoi ?)


class Feistel:
    NB_ITERATIONS = 32

    def __init__(self, key: int):
        self.key = key
        self.key_size = key.bit_length()

    def copy(self):
        return Feistel(self.key)

    def feistel_function(self, d):
        """
        F(d) = d + cle mod taille_cle
        """
        return (d + self.key) % 2**self.key_size

    def shift_key(self):
        """
        décale la cle de deux bits et place les deux bits de poids fort à
        l'emplacement des deux bits de poids faible.
        """
        bin_key = bourrage_zero(self.key, self.key_size)
        bin_key = bin_key[2:] + bin_key[:2]
        self.key = int(bin_key, 2)

    def prepare_dg(self, nbr: int) -> tuple[int, int]:
        nbr_bin = bourrage_zero(nbr, self.key_size * 2)
        d = int(nbr_bin[:self.key_size], 2)
        if len(nbr_bin) <= self.key_size:
            g = 0
        else:
            g = int(nbr_bin[self.key_size:], 2)

        return d, g

    def split_message_to_blocks(self, msg):
        chunk_size = self.key_size * 2
        divided_msg = []
        for i in range(0, len(msg), chunk_size):
            divided_msg.append(int(msg[i: i + chunk_size], 2))
        return divided_msg


class FeistelEncoder(Feistel):
    def __encode_block(self, nbr: int) -> str:
        iter_key = self.copy()
        d, g = self.prepare_dg(nbr)
        for i in range(Feistel.NB_ITERATIONS):
            d, g = g ^ iter_key.feistel_function(d), d
            iter_key.shift_key()

        d_bin = bourrage_zero(d, self.key_size)
        g_bin = bourrage_zero(g, self.key_size)

        return d_bin + g_bin

    def encode(self, msg: str):
        """
        Divise le message binaire en N sous blocs de 2048 bits
        Chiffre chacun de ces blocs à l'aide d'un schéma à 32 tournées de Feistel
        """

        message_divise = self.split_message_to_blocks(msg)
        res = ""
        for i, block in enumerate(message_divise):
            message_chiffre_partiel = self.__encode_block(block)
            if len(msg[self.key_size * 2 * i:]) < self.key_size * 2:
                message_chiffre_partiel = message_chiffre_partiel[
                    (self.key_size - len(msg[self.key_size * 2 * i:])):
                ]
            res += message_chiffre_partiel
        return res


class FeistelDecoder(Feistel):
    def __decode_block(self, nbr: int) -> str:
        iter_key = self.copy()
        d, g = self.prepare_dg(nbr)

        for i in range(Feistel.NB_ITERATIONS - 1):
            iter_key.shift_key()

        for i in range(Feistel.NB_ITERATIONS):
            d, g = g, d ^ iter_key.feistel_function(g)
            cle_bin = format(iter_key.key, "b")
            cle_bin = bourrage_zero(cle_bin, iter_key.key_size)
            cle_bin = (
                cle_bin[iter_key.key_size - 2:] + cle_bin[: iter_key.key_size - 2]
            )
            iter_key.key = int(cle_bin, 2)

        d_bin = bourrage_zero(d, self.key_size)
        g_bin = bourrage_zero(g, self.key_size)

        return d_bin + g_bin

    def decode(self, msg: str):
        """
        Divise le message binaire en N sous blocs de 2048 bits
        Chiffre chacun de ces blocs à l'aide d'un schéma à 32 tournées de Feistel
        """
        message_divise = self.split_message_to_blocks(msg)
        res: str = ""
        for i, block in enumerate(message_divise):
            message_dechiffre_partiel = self.__decode_block(block)
            msg_len = len(msg[self.key_size * 2 * i:])
            if msg_len < self.key_size * 2:
                message_dechiffre_partiel = message_dechiffre_partiel[
                    self.key_size - msg_len:
                ]
            res += message_dechiffre_partiel
        return res
