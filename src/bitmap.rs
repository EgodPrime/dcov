
use pyo3::prelude::*;
use rayon::prelude::*;
use ahash::AHasher;
use std::{hash::Hasher, ptr};
use libc::{shmat, shmctl, shmdt, shmget, IPC_CREAT, IPC_RMID};

const BITMAP_SIZE_DEFAULT: usize = 1 << 20;
const BYTEMAP_SIZE_DEFAULT: usize = BITMAP_SIZE_DEFAULT >> 3;
const PREVIOUS_INDEX_DEFAULT: u32 = 0xABCD1234;

#[inline]
fn hash_edge(src: u32, dst: u32) -> u32 {
    /*uint32_t h1 = hasher(a);
    uint32_t h2 = hasher(b);
    uint32_t r = h1 ^ (h2 + 0x9e3779b9 + (h1 << 6) + (h1 >> 2));
    r = r % bitmap_size; */
    let mut hasher = AHasher::default();
    hasher.write_u32(src);
    hasher.write_u32(dst);
    (hasher.finish() as u32) % BITMAP_SIZE_DEFAULT as u32
}

#[pyclass]
pub struct BitmapManager {
    bitmap_size: usize,
    shm_key: i32,
    m_data: Vec<u8>,
    previous_index: u32,
}

#[pymethods]
impl BitmapManager {
    #[new]
    pub fn new(shm_key: i32) -> Self {
        let mut t = BitmapManager {
            shm_key,
            bitmap_size: BITMAP_SIZE_DEFAULT,
            m_data: vec![0; BYTEMAP_SIZE_DEFAULT],
            previous_index: PREVIOUS_INDEX_DEFAULT,
        };
        t.read().unwrap_or(());
        t
    }

    #[getter]
    pub fn bitmap_size(&self) -> PyResult<usize> {
        Ok(self.bitmap_size)
    }

    pub fn clear_bitmap(&mut self) -> PyResult<()> {
        self.m_data.fill(0);
        Ok(())
    }

    pub fn close_bitmap(&mut self) -> PyResult<()> {
        unsafe {
            let shmid = shmget(self.shm_key, self.bitmap_size >> 3, 0o666);
            if shmid < 0 {
                return Err(pyo3::exceptions::PyRuntimeError::new_err(format!("shmget failed of key {}", self.shm_key)));
            }
            if shmctl(shmid, IPC_RMID, ptr::null_mut()) < 0 {
                return Err(pyo3::exceptions::PyRuntimeError::new_err(format!("shmctl(IPC_RMID) failed of key {}, id {}", self.shm_key, shmid)));
            }
        }
        self.m_data.clear();
        self.previous_index = PREVIOUS_INDEX_DEFAULT;
        Ok(())
    }

    pub fn count_bitmap(&self) -> PyResult<u32> {
        let slice = &self.m_data;
        let count = slice.par_iter().map(|&byte| {
            let mut c = byte;
            c = ( c & 0x55 ) + ( (c >> 1)  & 0x55 ) ;
            c = ( c & 0x33 ) + ( (c >> 2)  & 0x33 ) ;
            c = ( c & 0x0f ) + ( (c >> 4)  & 0x0f ) ;
            c as u32
        }).sum();
        Ok(count)
    }

    pub fn count_bitmap_s(&mut self) -> PyResult<u32> {
        self.read()?;
        self.count_bitmap()
    }


    pub fn set_bit(&mut self, index: u32) -> PyResult<()> {
        if index >= self.bitmap_size as u32{
            return Err(pyo3::exceptions::PyValueError::new_err(format!("index {} out of range.", index)));
        }
        let byte_index = (index >> 3) as usize;
        let bit_offset = (index & 0x07) as usize;
        self.m_data[byte_index] |= 1 << bit_offset;
        Ok(())
    }

    pub fn add_edge(&mut self, index: u32) -> PyResult<()> {
        if index >= self.bitmap_size as u32{
            return Err(pyo3::exceptions::PyValueError::new_err(format!("index {} out of range.", index)));
        }
        let edge_idx = hash_edge(self.previous_index, index);
        self.set_bit(edge_idx)?;
        self.previous_index = index;
        Ok(())
    }

    pub fn sync_from(&mut self, shm_key: i32) -> PyResult<()> {
        unsafe {
            let shmid_from = shmget(shm_key, self.bitmap_size >> 3, IPC_CREAT | 0o666);
            if shmid_from < 0 {
                return Err(pyo3::exceptions::PyRuntimeError::new_err(format!("shmget failed of key {}", shm_key)));
            }
            let m_data_from = shmat(shmid_from, ptr::null(), 0) as *mut u8;
            if m_data_from == ptr::null_mut() {
                return Err(pyo3::exceptions::PyRuntimeError::new_err(format!("shmat failed of key {}, id {}", shm_key, shmid_from)));
            }
            ptr::copy_nonoverlapping(m_data_from, self.m_data.as_mut_ptr(), self.bitmap_size >> 3);
            shmdt(m_data_from as *mut _);
        }
        Ok(())
    }

    pub fn sync_to(&self, shm_key: i32) -> PyResult<()> {
        unsafe {
            let shmid_to = shmget(shm_key, self.bitmap_size >> 3, IPC_CREAT | 0o666);
            if shmid_to < 0 {
                return Err(pyo3::exceptions::PyRuntimeError::new_err(format!("shmget failed of key {}", shm_key)));
            }
            let m_data_to = shmat(shmid_to, ptr::null(), 0) as *mut u8;
            if m_data_to == ptr::null_mut() {
                return Err(pyo3::exceptions::PyRuntimeError::new_err(format!("shmat failed of key {}, id {}", shm_key, shmid_to)));
            }
            ptr::copy_nonoverlapping(self.m_data.as_ptr(), m_data_to, self.bitmap_size >> 3);
            shmdt(m_data_to as *mut _);
        }
        Ok(())
    }

    pub fn read(&mut self) -> PyResult<()> {
        self.sync_from(self.shm_key)
    }

    pub fn write(&self) -> PyResult<()> {
        self.sync_to(self.shm_key)
    }

    pub fn merge_from(&mut self, shm_key: i32) -> PyResult<()> {
        unsafe {
            let shmid_src = shmget(shm_key, self.bitmap_size >> 3, 0o666);
            if shmid_src < 0 {
                return Err(pyo3::exceptions::PyRuntimeError::new_err(format!("shmget failed of key {}", shm_key)));
            }
            let m_data_src = shmat(shmid_src, ptr::null(), 0) as *mut u8;
            if m_data_src == ptr::null_mut() {
                return Err(pyo3::exceptions::PyRuntimeError::new_err(format!("shmat failed of key {}, id {}", shm_key, shmid_src)));
            }

            let slice_src = std::slice::from_raw_parts(m_data_src, self.bitmap_size >> 3);
            let slice_dest = &mut self.m_data;

            // 并行合并
            slice_dest.par_iter_mut().enumerate().for_each(|(i, byte_dest)| {
                let byte_src = slice_src[i];
                *byte_dest |= byte_src;
            });

            shmdt(m_data_src as *mut _);
        }
        Ok(())
    }

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
}