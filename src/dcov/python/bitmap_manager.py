"""ctypes-based fallback implementation of BitmapManager.

This mirrors the behaviour of the Rust/pyo3 implementation but uses
sysv shared memory calls via ``ctypes`` so Python-only environments
can still use ``BitmapManager``.
"""

from contextlib import contextmanager

import ctypes

BITMAP_SIZE_DEFAULT = 1 << 20
BYTEMAP_SIZE_DEFAULT = BITMAP_SIZE_DEFAULT >> 3
PREVIOUS_INDEX_DEFAULT = 0xABCD1234

# Precompute popcount lookup for fallback
_POPCOUNT_TABLE = tuple(bin(i).count("1") for i in range(256))

# Constants from <sys/ipc.h>
IPC_CREAT = 0o1000
IPC_RMID = 0

_libc = ctypes.CDLL("libc.so.6")
_libc.shmget.argtypes = (ctypes.c_int, ctypes.c_size_t, ctypes.c_int)
_libc.shmget.restype = ctypes.c_int
_libc.shmat.argtypes = (ctypes.c_int, ctypes.c_void_p, ctypes.c_int)
_libc.shmat.restype = ctypes.c_void_p
_libc.shmdt.argtypes = (ctypes.c_void_p,)
_libc.shmdt.restype = ctypes.c_int
_libc.shmctl.argtypes = (ctypes.c_int, ctypes.c_int, ctypes.c_void_p)
_libc.shmctl.restype = ctypes.c_int


class BitmapManager:
    """BitmapManager for managing System-V shared memory bitmaps."""

    def __init__(self, shm_key: int) -> None:
        self.shm_key = int(shm_key)
        self.bitmap_size = BITMAP_SIZE_DEFAULT
        self.m_data = bytearray(BYTEMAP_SIZE_DEFAULT)
        self.previous_index = PREVIOUS_INDEX_DEFAULT
        self.read()
        

    def clear_bitmap(self) -> None:
        self.m_data[:] = b"\x00" * len(self.m_data)

    def close_bitmap(self) -> None:
        shmid = _libc.shmget(self.shm_key, self.bitmap_size >> 3, 0o666)
        if shmid < 0:
            raise RuntimeError(f"shmget failed of key {self.shm_key}")
        if _libc.shmctl(shmid, IPC_RMID, None) < 0:
            raise RuntimeError(
                f"shmctl(IPC_RMID) failed of key {self.shm_key}, id {shmid}"
            )
        self.m_data.clear()
        self.previous_index = PREVIOUS_INDEX_DEFAULT

    def count_bitmap(self) -> int:
        # fast popcount: use integer bit_count on the whole buffer when
        # available (very fast in CPython). 
        return int.from_bytes(self.m_data, "little").bit_count()

    def count_bitmap_s(self) -> int:
        self.read()
        return self.count_bitmap()

    def set_bit(self, index: int) -> None:
        if index < 0 or index >= self.bitmap_size:
            raise ValueError(f"index {index} out of range.")
        byte_index = (index >> 3) & ((1 << 63) - 1)
        bit_offset = index & 0x07
        self.m_data[byte_index] |= 1 << bit_offset

    def _mix32(self, x: int) -> int:
        x &= 0xFFFFFFFF
        x = (x ^ (x >> 16)) * 0x85EBCA6B & 0xFFFFFFFF
        x = (x ^ (x >> 13)) * 0xC2B2AE35 & 0xFFFFFFFF
        x = x ^ (x >> 16)
        return x & 0xFFFFFFFF

    def _hash_edge(self, src: int, dst: int) -> int:
        h1 = self._mix32(src)
        h2 = self._mix32(dst)
        r = (
            h1 ^ ((h2 + 0x9E3779B9 + ((h1 << 6) & 0xFFFFFFFF) + (h1 >> 2)) & 0xFFFFFFFF)
        ) & 0xFFFFFFFF
        return r % self.bitmap_size

    def add_edge(self, index: int) -> None:
        if index < 0 or index >= self.bitmap_size:
            raise ValueError(f"index {index} out of range.")
        edge_idx = self._hash_edge(self.previous_index, index)
        self.set_bit(edge_idx)
        self.previous_index = index

    @contextmanager
    def _open_shm(self, shm_key: int):
        shmid = _libc.shmget(int(shm_key), self.bitmap_size >> 3, IPC_CREAT | 0o666)
        if shmid < 0:
            raise RuntimeError(f"shmget failed of key {shm_key}")
        addr = _libc.shmat(shmid, None, 0)
        if addr == ctypes.c_void_p(-1).value:
            raise RuntimeError(f"shmat failed of key {shm_key}, id {shmid}")
        try:
            yield addr
        finally:
            if _libc.shmdt(ctypes.c_void_p(addr)) < 0:
                raise RuntimeError("shmdt failed")

    def sync_from(self, shm_key: int) -> None:
        size = self.bitmap_size >> 3
        with self._open_shm(shm_key) as addr:
            buf = ctypes.string_at(addr, size)
            self.m_data[:size] = buf

    def sync_to(self, shm_key: int) -> None:
        size = self.bitmap_size >> 3
        with self._open_shm(shm_key) as addr:
            ctypes.memmove(addr, bytes(self.m_data[:size]), size)

    def read(self) -> None:
        self.sync_from(self.shm_key)

    def write(self) -> None:
        self.sync_to(self.shm_key)

    def merge_from(self, shm_key: int) -> None:
        size = self.bitmap_size >> 3
        with self._open_shm(shm_key) as addr:
            buf = ctypes.string_at(addr, size)
            for i in range(size):
                self.m_data[i] |= buf[i]
