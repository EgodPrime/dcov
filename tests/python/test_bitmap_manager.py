import subprocess
import ctypes

import pytest

from dcov import BitmapManager
from dcov.python import bitmap_manager


def test_basic():
    """
    $ ipcs -m

    ------ Shared Memory Segments --------
    key        shmid      owner      perms      bytes      nattch     status
    0x0000112f 2          lisy       666        131072     632        dest
    """
    test_key = 1234
    cmd = ["ipcs", "-m"]
    bm = BitmapManager(test_key)
    # ipcs -m should show the shm segment
    result = subprocess.run(cmd, capture_output=True, text=True)
    lines = result.stdout.split("\n")
    keys = [int(line.split()[0], 16) for line in lines[3:] if line.strip() != ""]
    assert test_key in keys
    bm.set_bit(10)
    bm.add_edge(20)
    count = bm.count_bitmap()
    assert count == 2
    bm.clear_bitmap()
    count = bm.count_bitmap()
    assert count == 0
    bm.close_bitmap()

    # ipcs -m should not show the shm segment anymore
    # 拆分所有行, 过滤掉空行, 取出第1列，转换为整数列表
    cmd = ["ipcs", "-m"]
    result = subprocess.run(cmd, capture_output=True, text=True)
    lines = result.stdout.split("\n")
    keys = [int(line.split()[0], 16) for line in lines[3:] if line.strip() != ""]
    assert test_key not in keys


def test_2_bitmaps():
    bm1 = BitmapManager(2001)
    bm2 = BitmapManager(2002)

    bm1.set_bit(5)
    bm1.add_edge(15)

    bm2.set_bit(10)
    bm2.add_edge(20)

    count1 = bm1.count_bitmap()
    count2 = bm2.count_bitmap()

    assert count1 == 2
    assert count2 == 2

    bm1.close_bitmap()
    bm2.close_bitmap()

    cmd = ["ipcs", "-m"]
    result = subprocess.run(cmd, capture_output=True, text=True)
    lines = result.stdout.split("\n")
    keys = [int(line.split()[0], 16) for line in lines[3:] if line.strip() != ""]
    assert 2001 not in keys
    assert 2002 not in keys


def test_count_bitmap_s():
    bm_parent = BitmapManager(2501)
    bm_parent.clear_bitmap()

    import multiprocessing

    def worker():
        bm_child = BitmapManager(2501)
        bm_child.set_bit(30)
        bm_child.write()

    p = multiprocessing.Process(target=worker)
    p.start()
    p.join()

    count = bm_parent.count_bitmap_s()
    assert count == 1  # 30
    bm_parent.close_bitmap()


def test_subprocess_read_multiprocessing():
    bm_parent = BitmapManager(3001)
    bm_parent.clear_bitmap()
    bm_parent.set_bit(5)
    bm_parent.set_bit(6)
    bm_parent.set_bit(7)
    bm_parent.write()

    import multiprocessing

    def worker(bm: BitmapManager):
        bm.read()
        bm.set_bit(8)
        bm.write()

    p = multiprocessing.Process(target=worker, args=(bm_parent,))
    p.start()
    p.join()

    bm_parent.read()
    count = bm_parent.count_bitmap()
    assert count == 4
    bm_parent.close_bitmap()


def test_subprocess_read_multiprocessing_no_pass():
    bm_parent = BitmapManager(4001)
    bm_parent.clear_bitmap()
    bm_parent.set_bit(17)
    bm_parent.write()

    import multiprocessing

    def worker():
        bm_child = BitmapManager(4001)
        bm_child.set_bit(18)
        bm_child.write()

    p = multiprocessing.Process(target=worker)
    p.start()
    p.join()

    bm_parent.read()
    count = bm_parent.count_bitmap()
    assert count == 2  # 17,18
    bm_parent.close_bitmap()


def test_subprocess_read_subprocess():
    bm_parent = BitmapManager(5001)
    bm_parent.clear_bitmap()
    bm_parent.set_bit(25)
    bm_parent.write()

    cmd = [
        "python3",
        "-c",
        (
            "from dcov import BitmapManager; "
            "bm=BitmapManager(5001); "
            "bm.read(); "
            "bm.set_bit(26); "
            "bm.write()"
        ),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    assert result.returncode == 0

    bm_parent.read()
    count = bm_parent.count_bitmap()
    assert count == 2  # 25,26
    bm_parent.close_bitmap()


def test_sync_from_normal():
    bm_main = BitmapManager(5501)
    bm_main.clear_bitmap()

    bm_sub = BitmapManager(5502)
    bm_sub.clear_bitmap()
    bm_sub.set_bit(40)
    bm_sub.write()

    bm_main.sync_from(5502)

    count = bm_main.count_bitmap()
    assert count == 1  # 40

    bm_sub.close_bitmap()
    bm_main.close_bitmap()


def test_sync_from_multiprocessing():
    bm_main = BitmapManager(5601)
    bm_main.clear_bitmap()

    import multiprocessing

    def worker():
        bm_sub = BitmapManager(5602)
        bm_sub.clear_bitmap()
        bm_sub.set_bit(41)
        bm_sub.write()

    p = multiprocessing.Process(target=worker)
    p.start()
    p.join()

    bm_main.sync_from(5602)

    count = bm_main.count_bitmap()
    assert count == 1  # 41

    bm_main.close_bitmap()


def test_merge_from():
    """
    一个主bitmap，两个子bitmap，子bitmap分别设置不同的位，最后主bitmap合并两个子bitmap的数据。
    """
    bm_main = BitmapManager(6001)
    bm_main.clear_bitmap()

    bm_child1 = BitmapManager(6002)
    bm_child1.clear_bitmap()
    bm_child1.set_bit(33)
    bm_child1.write()

    bm_child2 = BitmapManager(6003)
    bm_child2.clear_bitmap()
    bm_child2.set_bit(34)
    bm_child2.write()

    bm_main.merge_from(6002)
    bm_main.merge_from(6003)

    count = bm_main.count_bitmap()
    assert count == 2  # 33,34

    bm_child1.close_bitmap()
    bm_child2.close_bitmap()
    bm_main.close_bitmap()


def test_merge_from_subprocess_multiprocessing():
    bm_main = BitmapManager(7001)
    bm_main.clear_bitmap()
    bm_child1 = BitmapManager(7002)
    bm_child2 = BitmapManager(7003)

    import multiprocessing
    import random

    def worker(bm: BitmapManager):
        bm.clear_bitmap()
        bm.set_bit(random.randint(0, bm.bitmap_size - 1))
        bm.write()

    p1 = multiprocessing.Process(target=worker, args=(bm_child1,))
    p2 = multiprocessing.Process(target=worker, args=(bm_child2,))
    p1.start()
    p2.start()
    p1.join()
    p2.join()

    bm_main.merge_from(7002)
    bm_main.merge_from(7003)

    count = bm_main.count_bitmap()
    assert count == 2  # 45,46

    bm_main.close_bitmap()


def test_merge_from_subprocess_multiprocessing_no_pass():
    bm_main = BitmapManager(7001)
    bm_main.clear_bitmap()

    import multiprocessing
    import random

    def worker(shm_key: int):
        bm = BitmapManager(shm_key)
        bm.clear_bitmap()
        bm.set_bit(random.randint(0, bm.bitmap_size - 1))
        bm.write()

    p1 = multiprocessing.Process(target=worker, args=(7002,))
    p2 = multiprocessing.Process(target=worker, args=(7003,))
    p1.start()
    p2.start()
    p1.join()
    p2.join()

    bm_main.merge_from(7002)
    bm_main.merge_from(7003)

    count = bm_main.count_bitmap()
    assert count == 2  # 45,46

    bm_main.close_bitmap()


def test_merge_from_subprocess_subprocess():
    bm_main = BitmapManager(7001)
    bm_main.clear_bitmap()

    cmd1 = [
        "python3",
        "-c",
        (
            "from dcov import BitmapManager; "
            "bm=BitmapManager(7002); "
            "bm.clear_bitmap(); "
            "bm.set_bit(45); "
            "bm.write()"
        ),
    ]
    result1 = subprocess.run(cmd1, capture_output=True, text=True)
    assert result1.returncode == 0

    cmd2 = [
        "python3",
        "-c",
        (
            "from dcov import BitmapManager; "
            "bm=BitmapManager(7003); "
            "bm.clear_bitmap(); "
            "bm.set_bit(46); "
            "bm.write()"
        ),
    ]
    result2 = subprocess.run(cmd2, capture_output=True, text=True)
    assert result2.returncode == 0

    bm_main.merge_from(7002)
    bm_main.merge_from(7003)

    count = bm_main.count_bitmap()
    assert count == 2  # 45,46

    bm_main.close_bitmap()
    bm_7002 = BitmapManager(7002)
    bm_7002.close_bitmap()
    bm_7003 = BitmapManager(7003)
    bm_7003.close_bitmap()


def test_count_bitmap_time_cost():
    import time

    bm = BitmapManager(8001)
    bm.clear_bitmap()
    for i in range(1000):
        bm.set_bit(i * 10)

    time_data = []
    # repeat 10 times to get average time
    for _ in range(10):
        start = time.time()
        count = bm.count_bitmap()
        end = time.time()
        time_data.append(end - start)
    avg_time = sum(time_data) / len(time_data)
    print(f"Average time to count bitmap: {avg_time:.6f} seconds")
    assert count == 1000
    bm.close_bitmap()


def test_count_bitmap_equivalence_random():
    import random

    bm = BitmapManager(9001)
    bm.clear_bitmap()
    # set some random bits across the bitmap
    for _ in range(500):
        bm.set_bit(random.randint(0, bm.bitmap_size - 1))

    # reference (slow) implementation
    expected = sum(bin(b).count("1") for b in bm.m_data)
    assert bm.count_bitmap() == expected
    bm.close_bitmap()


def test_set_bit_and_clear_and_count():
    bm = BitmapManager(12345)
    # make bitmap small and resize the backing storage
    bm.bitmap_size = 32
    bm.m_data = bytearray(bm.bitmap_size >> 3)

    try:
        with pytest.raises(ValueError):
            bm.set_bit(-1)

        with pytest.raises(ValueError):
            bm.set_bit(bm.bitmap_size)

        bm.set_bit(5)
        assert bm.count_bitmap() == 1
        bm.clear_bitmap()
        assert bm.count_bitmap() == 0
    finally:
        bm.close_bitmap()


def test_mix_and_hash_edge_and_add_edge():
    bm = BitmapManager(1)
    try:
        bm.bitmap_size = 128
        bm.m_data = bytearray(bm.bitmap_size >> 3)

        v = bm._mix32(0x12345678)
        assert isinstance(v, int) and 0 <= v <= 0xFFFFFFFF

        h = bm._hash_edge(1, 2)
        assert 0 <= h < bm.bitmap_size

        prev = bm.previous_index
        bm.add_edge(3)
        assert bm.previous_index == 3
        # a bit was set
        assert bm.count_bitmap() >= 1
    finally:
        bm.close_bitmap()

def test_close_bitmap_error_shmget(monkeypatch):
    bm = BitmapManager(13579)

    def fake_shmget_fail(key, size, perms):
        return -1

    monkeypatch.setattr(bitmap_manager._libc, "shmget", fake_shmget_fail)
    with pytest.raises(RuntimeError):
        bm.close_bitmap()

def test_close_bitmap_error_shmctl(monkeypatch):
    bm = BitmapManager(24680)

    def fake_shmctl_fail(shmid, cmd, buf):
        return -1

    monkeypatch.setattr(bitmap_manager._libc, "shmctl", fake_shmctl_fail)
    with pytest.raises(RuntimeError):
        bm.close_bitmap()

def test_add_edge_value_error():
    bm = BitmapManager(11223)
    bm.bitmap_size = 64
    bm.m_data = bytearray(bm.bitmap_size >> 3)

    with pytest.raises(ValueError):
        bm.add_edge(-1)

    with pytest.raises(ValueError):
        bm.add_edge(bm.bitmap_size)

    bm.close_bitmap()

def test__open_shm_error_shmget(monkeypatch):
    bm = BitmapManager(33445)

    def fake_shmget_fail(key, size, perms):
        return -1

    monkeypatch.setattr(bitmap_manager._libc, "shmget", fake_shmget_fail)
    with pytest.raises(RuntimeError):
        with bm._open_shm(33445):
            pass

def test__open_shm_error_shmat(monkeypatch):
    bm = BitmapManager(55667)

    def fake_shmat_fail(shmid, addr, flags):
        return ctypes.c_void_p(-1).value

    monkeypatch.setattr(bitmap_manager._libc, "shmat", fake_shmat_fail)
    with pytest.raises(RuntimeError):
        with bm._open_shm(55667):
            pass

def test__open_shm_error_shmdt(monkeypatch):
    bm = BitmapManager(77889)

    def fake_shmdt_fail(addr):
        return -1

    monkeypatch.setattr(bitmap_manager._libc, "shmdt", fake_shmdt_fail)
    with pytest.raises(RuntimeError):
        with bm._open_shm(77889):
            pass