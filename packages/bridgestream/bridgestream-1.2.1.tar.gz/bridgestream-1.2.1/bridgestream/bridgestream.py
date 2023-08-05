import abc
import struct
from typing import List


class BridgeStream:
    _capacity: int
    _buffer: bytearray

    def __init__(self, buffer=None):
        self._write_index = 0
        if buffer:
            self._capacity = len(buffer)
            self._buffer = bytearray(buffer)
            self._write_index = self._capacity
        else:
            self._capacity = 16
            self._buffer = bytearray(self._capacity)

        self._read_index = 0

    def encode(self) -> bytearray:
        return self._buffer[:self._write_index]

    def append_to_source(self, data):
        length = len(data)
        self.grow(length)
        struct.pack_into(f"{length}s", self._buffer, self._write_index, bytearray(data))
        self._write_index += length

    def grow(self, size):
        is_enough_size = True

        while self._write_index + size > self._capacity:
            self._capacity *= 2
            is_enough_size = False

        if not is_enough_size:
            self._buffer = self._buffer.ljust(self._capacity, b"0")

    def write_int(self, value):
        self.grow(struct.calcsize("i"))
        struct.pack_into("i", self._buffer, self._write_index, value)
        self._write_index += struct.calcsize("i")

    def read_int(self):
        value = struct.unpack_from(
            "i",
            self._buffer,
            self._read_index
        )[0]
        self._read_index += struct.calcsize("i")
        return value

    def write_float(self, value):
        self.grow(struct.calcsize("f"))
        struct.pack_into("f", self._buffer, self._write_index, value)
        self._write_index += struct.calcsize("f")

    def read_float(self):
        value = struct.unpack_from(
            "f",
            self._buffer,
            self._read_index
        )[0]

        self._read_index += struct.calcsize("f")
        return value

    def write_bool(self, value):
        self.grow(struct.calcsize("?"))
        struct.pack_into("?", self._buffer, self._write_index, value)
        self._write_index += struct.calcsize("?")

    def read_bool(self):
        value = struct.unpack_from(
            "?",
            self._buffer,
            self._read_index
        )[0]

        self._read_index += struct.calcsize("?")
        return value

    def write_string(self, value):
        if not value:
            value = ""
        data = bytes(value, "utf-8")
        length = len(data)
        self.write_int(length)
        self.grow(length)
        struct.pack_into(f"{length}s", self._buffer, self._write_index, data)
        self._write_index += length

    def read_string(self):
        length = self.read_int()
        value = struct.unpack_from(
            f"{length}s",
            self._buffer,
            self._read_index
        )[0]

        self._read_index += length
        return value.decode("utf-8")

    def write_bytearray(self, value):
        length = len(value)
        self.write_int(length)
        self.grow(length)
        struct.pack_into(f"{length}s", self._buffer, self._write_index, value)
        self._write_index += length

    def read_bytearray(self):
        length = self.read_int()
        value = struct.unpack_from(
            f"{length}s",
            self._buffer,
            self._read_index
        )[0]

        self._read_index += length
        return value

    def write_int_list(self, values):
        self.write_int(len(values))
        for value in values:
            self.write_int(value)

    def read_int_list(self):
        return [self.read_int() for _ in range(self.read_int())]

    def write_float_list(self, values):
        self.write_int(len(values))
        for value in values:
            self.write_float(value)

    def read_float_list(self):
        return [self.read_float() for _ in range(self.read_int())]

    def write_bool_list(self, values):
        self.write_int(len(values))
        for value in values:
            self.write_bool(value)

    def read_bool_list(self):
        return [self.read_bool() for _ in range(self.read_int())]

    def write_string_list(self, values):
        self.write_int(len(values))
        for value in values:
            self.write_string(value)

    def read_string_list(self):
        return [self.read_string() for _ in range(self.read_int())]

    def write_bytearray_list(self, values):
        self.write_int(len(values))
        for value in values:
            self.write_bytearray(value)

    def read_bytearray_list(self):
        length = self.read_int()
        result = []
        for _ in range(length):
            value = self.read_bytearray()
            result.append(value)
        return result

    def write(self, serializer: 'BridgeSerializer'):
        packet = BridgeStream()
        serializer.write(packet)
        self.write_stream(packet)

    def read(self, cls: 'BridgeSerializer') -> 'BridgeSerializer':
        stream = BridgeStream(self.read_bytearray())
        value = cls()
        value.read(stream)
        return value

    def write_list(self, serializers):
        self.write_int(len(serializers))
        for serializer in serializers:
            self.write(serializer)

    def read_list(self, cls: List['BridgeSerializer']):
        length = self.read_int()
        return [self.read(cls) for _ in range(length)]

    def write_stream(self, stream):
        if not stream:
            self.write_int(0)
            return
        self.write_bytearray(stream.encode())

    def read_stream(self):
        stream = BridgeStream(self.read_bytearray())
        return stream

    def has_more(self):
        return self._write_index > self._read_index

    def check_more(self, need) -> bool:
        return self._write_index >= self._read_index + need


class BridgeSerializer:

    @abc.abstractmethod
    def write(self, stream: BridgeStream):
        raise NotImplementedError()

    @abc.abstractmethod
    def read(self, stream: BridgeStream):
        raise NotImplementedError()
