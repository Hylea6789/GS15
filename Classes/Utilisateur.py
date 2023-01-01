import random

from Classes.feistel import FeistelEncoder, FeistelDecoder
from Cle import Cle
from RatchetKey import RatchetKey
from utils import exponentiation_rapide, bourrage_zero


class Utilisateur:
    sk: int
    cle_ratchet: RatchetKey

    def __init__(self, p, g, nb_cle_otk, name):
        """
        Initialise les valeur des clés pour un utilisateur
        """
        self.id = Cle(p, g)  # Clé preuve pour une utilisation long terme
        self.pk = Cle(p, g)  # pré-clé signée
        self.otpk = [Cle(p, g) for _ in range(nb_cle_otk)]
        self.eph = Cle(p, g)  # Clé éphémère
        self.name = name  # nom de l'utilisateur

        # self.pk.signature() TODO ecrire la fonction de signature

    def publication_cle(self) -> tuple[int, int, Cle]:
        key = random.choice(self.otpk)
        return self.id.id_pub, self.pk.id_pub, key

    def calcul_sk_emetteur_x3dh(
            self, id_a: int, pk_a: int, otpk_a: int, p: int, g: int
    ):
        """
        Calcul de la clé partagée SK pour Bob

        :param id_a: ?
        :param pk_a: ?
        :param otpk_a: ?
        :param p: ?
        :param g: ?
        :return: ?
        """
        # TODO : vérification de la signature ajouter sig_pk_a: int auix paramètres
        self.eph = Cle(p, g)

        dh1: int = exponentiation_rapide(pk_a, self.id.id_priv, p)
        dh2: int = exponentiation_rapide(id_a, self.eph.id_priv, p)
        dh3: int = exponentiation_rapide(pk_a, self.eph.id_priv, p)
        dh4: int = exponentiation_rapide(otpk_a, self.eph.id_priv, p)

        self.sk = (dh1 + dh2 + dh3 + dh4) % p

        self.cle_ratchet = RatchetKey(self.sk)

        return self.id.id_pub, self.eph.id_pub

    def calcul_sk_destinataire_x3dh(self, id_pub_b, eph_pub_b, key: Cle, p: int):
        dh1: int = exponentiation_rapide(id_pub_b, self.pk.id_priv, p)
        dh2: int = exponentiation_rapide(eph_pub_b, self.id.id_priv, p)
        dh3: int = exponentiation_rapide(eph_pub_b, self.pk.id_priv, p)
        dh4: int = exponentiation_rapide(eph_pub_b, key.id_priv, p)

        self.sk = (dh1 + dh2 + dh3 + dh4) % p  # TODO définir la fonction de calcul

        self.cle_ratchet = RatchetKey(self.sk)

    def publication_cle_dh(self) -> str:
        self.kdf_ratchet()
        encoder = FeistelEncoder(self.cle_ratchet.cle_message)
        eph_pub_r_bin = encoder.encode(format(self.eph.id_pub, "b"))
        print("Clé éphémère publique recepteur")
        print("recepteur :", format(self.eph.id_pub, "b"))

        return eph_pub_r_bin

    def calcul_rachet_emetteur_dh(self, eph_pub_r_bin: str, p: int, g: int) -> int:
        self.kdf_ratchet()
        decoder = FeistelDecoder(self.cle_ratchet.cle_message)

        eph_pub_r = int(decoder.decode(eph_pub_r_bin), 2)

        self.kdf_ratchet()

        self.cle_ratchet = RatchetKey(exponentiation_rapide(eph_pub_r, self.eph.id_priv, p))
        self.eph = Cle(p, g)

        return self.eph.id_pub

    def calcul_rachet_recepteur_dh(self, eph_pub_e_bin: str, p: int, g: int):
        self.kdf_ratchet()
        decoder = FeistelDecoder(self.cle_ratchet.cle_message)
        eph_pub_e = int(decoder.decode(eph_pub_e_bin), 2)
        self.cle_ratchet = RatchetKey(exponentiation_rapide(eph_pub_e, self.eph.id_priv, p))
        self.eph = Cle(p, g)

    def kdf_ratchet(self):
        self.cle_ratchet.fonction_derivation()

    def envoie_message(self, message: str) -> str:
        message_bin = "".join(bourrage_zero(format(ord(i), 'b'), 7) for i in message)
        print(message_bin)
        encoder = FeistelEncoder(self.cle_ratchet.cle_message)
        self.kdf_ratchet()
        return encoder.encode(message_bin)

    def reception_message(self, message_chiffre) -> str:
        self.kdf_ratchet()
        decoder = FeistelDecoder(self.cle_ratchet.cle_message)

        message_dechiffre = decoder.decode(message_chiffre)
        print(message_dechiffre)
        message = ''.join(chr(int(message_dechiffre[x * 7:x * 7 + 7], 2)) for x in range(len(message_dechiffre) // 7))

        return message


"""
Mise à jour de la clé partagée via Diffie Hellman, une seule clé suffit

Envoie "classique de message" de Bob à Alice

Bob calcul une nouvelle clé
"""
