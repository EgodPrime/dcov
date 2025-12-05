class BitmapManager:
    """
    BitmapManager for managing shared memory bitmaps.

    BitmapManager instance maintains only a local copy of the shared memory bitmap.
    To ensure the local copy is up-to-date with the shared memory, call `read()` before
    accessing the bitmap. After modifying the local copy, call `write()` to update
    the shared memory.

    The constructor takes a single argument `shm_key`, which is the key for the shared memory segment. `read()` is automatically called during initialization.

    `count_bitmap_s()` is a convenience method that reads the latest bitmap from shared memory and returns the count of set bits in one call.
    """

    def __init__(self, shm_key: int) -> None: ...
    def clear_bitmap(self) -> None:
        """
        sets all bits in the local bitmap to 0.
        """

    def close_bitmap(self) -> None:
        """
        closes the shared memory segment associated with this BitmapManager.

        Be sure to call this method when the BitmapManager is no longer needed to free up system resources.
        """

    def count_bitmap(self) -> int:
        """
        Counts the number of set bits in the local bitmap.
        """

    def count_bitmap_s(self) -> int:
        """
        Reads the latest bitmap from shared memory and returns the count of set bits.

        This is a convenience method that combines `read()` and `count_bitmap()`.
        """

    def set_bit(self, index: int) -> None:
        """
        Sets the bit at the specified index in the local bitmap to 1.
        """

    def add_edge(self, index: int) -> None:
        """
        Adds an edge at the specified index in the local bitmap.

        The edge index is calculated with a special hashing function to minimize collisions.
        """

    def sync_from(self, shm_key: int) -> None:
        """
        Synchronizes the local bitmap with the specified shared memory bitmap.
        """

    def sync_to(self, shm_key: int) -> None:
        """
        Synchronizes the specified shared memory bitmap with the local bitmap.
        """

    def merge_from(self, shm_key: int) -> None:
        """
        Merges the specified shared memory bitmap into the local bitmap using a bitwise OR operation.
        """

    def read(self) -> None:
        """
        Reads the latest bitmap from shared memory into the local bitmap.

        This is equivalent to calling `sync_from(self.shm_key)`.
        """

    def write(self) -> None:
        """
        Writes the local bitmap to shared memory.

        This is equivalent to calling `sync_to(self.shm_key)`.
        """
