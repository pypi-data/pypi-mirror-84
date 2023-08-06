#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from itertools import cycle

from . import arg, StreamCipherUnit


class rc4mod(StreamCipherUnit):
    """
    Implements a modifiably version of the RC4 stream cipher where the size of
    the RC4 table can be altered.
    """

    def __init__(
        self, key, *,
        size: arg.number('-t', help='Table size, {default} by default.', bound=(0x100, None)) = 0x100
    ):
        super().__init__(key=key, size=size)

    def keystream(self):
        size = self.args.size
        tablerange = range(size)
        b, table = 0, bytearray(k & 0xFF for k in tablerange)
        for a, keybyte in zip(tablerange, cycle(self.args.key)):
            b = (b + keybyte + table[a]) % size
            table[a], table[b] = table[b], table[a]
        b, a = 0, 0
        while True:
            a = (a + 1) % size
            b = (b + table[a]) % size
            table[a], table[b] = table[b], table[a]
            yield table[(table[a] + table[b]) % size]
