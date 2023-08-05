import unittest

from bridgestream import BridgeStream, BridgeSerializer


class MatchInfo(BridgeSerializer):

    def __init__(self):
        self.match_id: int = 1
        self.player_name: str = "test"
        self.power: float = 0.5
        self.active: bool = True

    def write(self, stream: BridgeStream):
        stream.write_int(self.match_id)
        stream.write_string(self.player_name)
        stream.write_float(self.power)
        stream.write_bool(self.active)

    def read(self, stream: BridgeStream):
        self.match_id = stream.read_int()
        self.player_name = stream.read_string()
        self.power = stream.read_float()
        self.active = stream.read_bool()


class BridgeStreamTestCase(unittest.TestCase):

    def test_grows_buffer_size(self):
        expected = 32
        stream = BridgeStream()

        stream.grow(17)

        self.assertEqual(expected, stream._capacity)

    def test_does_not_grows_buffer_size(self):
        expected = 16
        stream = BridgeStream()

        stream.grow(10)

        self.assertEqual(expected, stream._capacity)

    def test_int(self):
        expected = 16
        stream = BridgeStream()
        stream.write_int(expected)

        received_stream = BridgeStream(stream.encode())
        got = received_stream.read_int()

        self.assertEqual(expected, got)

    def test_float(self):
        expected = 16.123123168945312
        stream = BridgeStream()
        stream.write_float(expected)

        received_stream = BridgeStream(stream.encode())
        got = received_stream.read_float()

        self.assertAlmostEqual(expected, got, places=7)

    def test_bool(self):
        stream = BridgeStream()
        stream.write_bool(True)
        stream.write_bool(False)
        received_stream = BridgeStream(stream.encode())

        self.assertTrue(received_stream.read_bool())
        self.assertFalse(received_stream.read_bool())

    def test_string(self):
        stream = BridgeStream()
        stream.write_string("test_data")
        received_stream = BridgeStream(stream.encode())

        self.assertEqual("test_data", received_stream.read_string())

    def test_bytearray(self):
        stream = BridgeStream()
        stream.write_bytearray(b"test_data")
        received_stream = BridgeStream(stream.encode())

        self.assertEqual(b"test_data", received_stream.read_bytearray())

    def test_int_list(self):
        expected = [16, 32, 64,16, 32, 64,16, 32, 64,16, 32, 6416, 32, 6416, 32, 64,16, 32, 64,16, 32, 64,16, 32, 64]
        stream = BridgeStream()
        stream.write_int_list(expected)

        received_stream = BridgeStream(stream.encode())
        got = received_stream.read_int_list()

        self.assertListEqual(expected, got)

    def test_float_list(self):
        expected_list = [16.1231231, 168.9453121, 68945.312161]
        stream = BridgeStream()
        stream.write_float_list(expected_list)

        received_stream = BridgeStream(stream.encode())
        received_list = received_stream.read_float_list()

        for expected, got in zip(expected_list, received_list):
            self.assertAlmostEqual(expected, got, places=3)

    def test_bool_list(self):
        expected = [True, False, True]
        stream = BridgeStream()
        stream.write_bool_list(expected)
        received_stream = BridgeStream(stream.encode())

        self.assertListEqual(expected, received_stream.read_bool_list())

    def test_string_list(self):
        expected = ["test", "da", "ta"]
        stream = BridgeStream()
        stream.write_string_list(expected)
        received_stream = BridgeStream(stream.encode())

        self.assertListEqual(expected, received_stream.read_string_list())

    def test_bytearray_list(self):
        expected = [b"test", b"da", b"ta"]
        stream = BridgeStream()
        stream.write_bytearray_list(expected)
        received_stream = BridgeStream(stream.encode())

        self.assertListEqual(expected, received_stream.read_bytearray_list())

    def test_serializer(self):
        test_obj = MatchInfo()
        stream = BridgeStream()
        stream.write(test_obj)
        received_stream = BridgeStream(stream.encode())

        self.assertTrue(received_stream.read_bool())
        self.assertFalse(received_stream.read_bool())
    
    def test_serializer_list(self):
        test_obj = MatchInfo()
        stream = BridgeStream()
        stream.write_list([test_obj, test_obj])

        received_stream = BridgeStream(stream.encode())
        received_serializers = received_stream.read_list(MatchInfo)
        self.assertEqual(len(received_serializers), 2)

        received_obj: MatchInfo = received_serializers[0]

        self.assertEqual(received_obj.match_id, test_obj.match_id)
        self.assertEqual(received_obj.player_name, test_obj.player_name)
        self.assertEqual(received_obj.power, test_obj.power)
        self.assertEqual(received_obj.active, test_obj.active)

    def test_has_more(self):
        stream = BridgeStream()
        stream.write_int(1)
        received_stream = BridgeStream(stream.encode())
        self.assertTrue(received_stream.has_more())

        received_stream.read_int()
        self.assertFalse(received_stream.has_more())

    def test_stream(self):
        expected = 1
        stream = BridgeStream()
        inner_stream = BridgeStream()
        inner_stream.write_int(expected)
        stream.write_stream(inner_stream)

        received_stream = BridgeStream(stream.encode())
        received_inner_stream = received_stream.read_stream()
        got = received_inner_stream.read_int()

        self.assertEqual(expected, got)

    def test_string_accepts_None(self):
        stream = BridgeStream()
        stream.write_string(None)
        received_stream = BridgeStream(stream.encode())
        self.assertEqual(received_stream.read_string(), "")

    def test_initial_buffer_overrides_write_index(self):
        stream = BridgeStream()
        stream.write_string(None)
        received_stream = BridgeStream(stream.encode())
        self.assertEqual(received_stream._write_index, received_stream._capacity)

if __name__ == '__main__':
    unittest.main()
