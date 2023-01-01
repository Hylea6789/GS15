import unittest

from Classes.feistel import *


class FonctionFeistelTest(unittest.TestCase):
    def test_1(self):
        res = Feistel(0x228).feistel_function(263)
        self.assertEqual(res, 815)

    def test_2(self):
        res = Feistel(0xa2).feistel_function(359)
        self.assertEqual(9, res)

    def test_3(self):
        f = Feistel(0xa2)
        f.key_size = 10
        res = f.feistel_function(263)
        self.assertEqual(425, res)


class DecalageFeistelTest(unittest.TestCase):
    def test_1(self):
        feistel = Feistel(0b1100010)
        feistel.shift_key()
        self.assertEqual(feistel.key, 0b1011)


class ShiftKeyTest(unittest.TestCase):
    def test_1(self):
        f = Feistel(0x228)
        f.shift_key()
        self.assertEqual(162, f.key)

    def test_2(self):
        f = Feistel(0xa2)
        f.shift_key()
        self.assertEqual(138, f.key)

    def test_3(self):
        f = Feistel(0xa2)
        f.key_size = 10
        f.shift_key()
        self.assertEqual(648, f.key)


class BlockDividerTest(unittest.TestCase):
    def test_1(self):
        key = Feistel(0x228)
        msg = format(0x13bb319c3f8f1c077823552af94, "b")
        res = key.split_message_to_blocks(msg)
        self.assertEqual(res, [646552, 844284, 495107, 770330, 693628, 20])


class FeistelDgPreparationTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.feistel = Feistel(0x228)

    def test_1(self):
        res = self.feistel.prepare_dg(646552)
        self.assertEqual(res, (631, 408))

    def test_2(self):
        res = self.feistel.prepare_dg(770330)
        self.assertEqual(res, (752, 282))

    def test_incomplete_block(self):
        res = self.feistel.prepare_dg(20)
        self.assertEqual(res, (0, 20))


class FeistelEncoderTest(unittest.TestCase):
    def setUp(self) -> None:
        self.msg = format(0x13bb319c3f8f1c077823552af94, "b")
        self.encoded_msg = format(0x71cb3d2d567139c328591cd60b98c, "b")
        self.encoder = FeistelEncoder(0x228)

    def test_block_encoding(self):
        block = 646552
        res = self.encoder._FeistelEncoder__encode_block(block)
        self.assertEqual(res, "11100011100101100111")

    def test_1(self):
        res = self.encoder.encode(self.msg)
        self.assertEqual(res, self.encoded_msg)


class FeistelDecoderTest(unittest.TestCase):
    def setUp(self) -> None:
        self.msg = format(0x71cb3d2d567139c328591cd60b98c, "b")
        self.decoded_msg = format(0x13bb319c3f8f1c077823552af94, "b")
        self.decoder = FeistelDecoder(0x228)

    def test_1(self):
        res = self.decoder.decode(self.msg)
        self.assertEqual(res, self.decoded_msg)



# TODO : écrire plus de tests
