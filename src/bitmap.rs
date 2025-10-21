
use pyo3::prelude::*;
use rayon::prelude::*;
use ahash::AHasher;
use std::{hash::Hasher, ptr};
use libc::{shmat, shmctl, shmdt, shmget, IPC_CREAT, IPC_RMID};

const BITMAP_SIZE: u32 = 1 << 20;
const BYTEMAP_SIZE: usize = (BITMAP_SIZE >> 3) as usize;
const SHM_KEY_PY: i32 = 4399;

static mut SHMID: i32 = -1;
static mut M_DATA_PY: *mut u8 = ptr::null_mut();
static mut PREVIOUS_INDEX_PY: u32 = 0xABCD1234;


#[inline]
fn count_bits(m_data: *const u8) -> u32 {
    let slice: &[u8];
    unsafe {
        slice = std::slice::from_raw_parts(m_data, BYTEMAP_SIZE);
    }
    slice.par_iter().map(|&byte| {
        let mut c = byte;
        c = ( c & 0x55 ) + ( (c >> 1)  & 0x55 ) ;
        c = ( c & 0x33 ) + ( (c >> 2)  & 0x33 ) ;
        c = ( c & 0x0f ) + ( (c >> 4)  & 0x0f ) ;
        c as u32
    }).sum()
}

#[inline]
unsafe fn set_bit(m_data: *mut u8, index: u32) {
    let byte_index = (index >> 3) as isize;
    let bit_offset = index & 0x07;
    let byte_ptr = m_data.offset(byte_index);
    let byte = ptr::read(byte_ptr);
    ptr::write(byte_ptr, byte | (1 << bit_offset));
}

#[inline]
fn hash_edge(src: u32, dst: u32) -> u32 {
    /*uint32_t h1 = hasher(a);
    uint32_t h2 = hasher(b);
    uint32_t r = h1 ^ (h2 + 0x9e3779b9 + (h1 << 6) + (h1 >> 2));
    r = r % bitmap_size; */
    let mut hasher = AHasher::default();
    hasher.write_u32(src);
    hasher.write_u32(dst);
    (hasher.finish() as u32) % BITMAP_SIZE
}

#[pyfunction]
pub unsafe fn open_bitmap_py() -> PyResult<i32> {
    SHMID = shmget(SHM_KEY_PY, BYTEMAP_SIZE, IPC_CREAT | 0o666);
    if SHMID < 0 {
        return Err(pyo3::exceptions::PyRuntimeError::new_err(format!("shmget failed of key {}", SHM_KEY_PY)));
    }
    M_DATA_PY = shmat(SHMID, ptr::null(), 0) as *mut u8;
    if M_DATA_PY == ptr::null_mut() {
        return Err(pyo3::exceptions::PyRuntimeError::new_err(format!("shmat failed of key {}, id {}", SHM_KEY_PY, SHMID)));
    }
    Ok(SHMID)
}

#[pyfunction]
pub unsafe fn close_bitmap_py() -> PyResult<()> {
    if M_DATA_PY != ptr::null_mut() {
        if shmdt(M_DATA_PY as *const _) < 0 {
            return Err(pyo3::exceptions::PyRuntimeError::new_err(format!("shmdt failed of id {}", SHMID)));
        }
        M_DATA_PY = ptr::null_mut();
    }
    if shmctl(SHMID, IPC_RMID, ptr::null_mut()) < 0 {
        return Err(pyo3::exceptions::PyRuntimeError::new_err(format!("shmctl({}, IPC_RMID, 0) failed.", SHMID)));
    }
    Ok(())
}

#[pyfunction]
pub unsafe fn clear_bitmap_py() -> PyResult<()> {
    if M_DATA_PY != ptr::null_mut() {
        ptr::write_bytes(M_DATA_PY, 0, BYTEMAP_SIZE);
    }
    Ok(())
}

#[pyfunction]
pub unsafe fn count_bitmap_py() -> PyResult<u32> {
    if M_DATA_PY == ptr::null_mut() {
        return Err(pyo3::exceptions::PyRuntimeError::new_err("bitmap not opened."));
    }
    let count = count_bits(M_DATA_PY as *const u8);
    Ok(count)
}

#[pyfunction]
pub unsafe fn set_bit_py(index: u32) -> PyResult<()> {
    if M_DATA_PY == ptr::null_mut() {
        return Err(pyo3::exceptions::PyRuntimeError::new_err("bitmap not opened."));
    }
    if index >= BITMAP_SIZE {
        return Err(pyo3::exceptions::PyValueError::new_err(format!("index {} out of range.", index)));
    }
    set_bit(M_DATA_PY, index);
    Ok(())
}

#[pyfunction]
pub unsafe fn add_edge_py(index: u32) -> PyResult<()> {
    if M_DATA_PY == ptr::null_mut() {
        return Err(pyo3::exceptions::PyRuntimeError::new_err("bitmap not opened."));
    }
    if index >= BITMAP_SIZE {
        return Err(pyo3::exceptions::PyValueError::new_err(format!("index {} out of range.", index)));
    }
    let edge_idx = hash_edge(PREVIOUS_INDEX_PY, index);
    set_bit(M_DATA_PY, edge_idx);
    PREVIOUS_INDEX_PY = index;
    Ok(())
}
   
#[pyfunction]
pub fn get_bytemap_size() -> PyResult<usize> {
    Ok(BYTEMAP_SIZE)
}

#[pyfunction]
pub fn get_bitmap_size() -> PyResult<u32> {
    Ok(BITMAP_SIZE)
}

#[cfg(test)]

mod tests {
    use super::*;

    #[test]
    fn test_hash_edge() {
        let h1 = hash_edge(1, 2);
        let h2 = hash_edge(2, 1);
        assert_ne!(h1, h2);
    }

    #[test]
    fn test_count_bits() {
        // BYTEMAP_SIZE length
        let mut bitmap: Vec<u8> = vec![0; BYTEMAP_SIZE];
        let count = count_bits(bitmap.as_ptr());
        assert_eq!(count, 0);
        // set some bits
        bitmap[0] = 0b10101010; // 4 bits
        bitmap[1] = 0b11110000; // 4 bits
        let count = count_bits(bitmap.as_ptr());
        assert_eq!(count, 8);
    }

    #[test]
    fn test_set_bit() {
        let mut bitmap: Vec<u8> = vec![0; BYTEMAP_SIZE];
        unsafe {
            set_bit(bitmap.as_mut_ptr(), 0);
            assert_eq!(bitmap[0], 0b00000001);
            set_bit(bitmap.as_mut_ptr(), 7);
            assert_eq!(bitmap[0], 0b10000001);
            set_bit(bitmap.as_mut_ptr(), 8);
            assert_eq!(bitmap[1], 0b00000001);
            set_bit(bitmap.as_mut_ptr(), 15);
            assert_eq!(bitmap[1], 0b10000001);
            set_bit(bitmap.as_mut_ptr(), (BYTEMAP_SIZE+7) as u32  );
            assert_eq!(bitmap[BYTEMAP_SIZE -1], 0b00000000);
        }
    }
}