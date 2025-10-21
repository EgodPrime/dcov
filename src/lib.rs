use pyo3::prelude::*;

mod bitmap;

use bitmap::{open_bitmap_py, close_bitmap_py, clear_bitmap_py, count_bitmap_py, set_bit_py, add_edge_py, get_bytemap_size, get_bitmap_size};



#[pymodule]
fn _core(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(open_bitmap_py, m)?)?;
    m.add_function(wrap_pyfunction!(close_bitmap_py, m)?)?;
    m.add_function(wrap_pyfunction!(clear_bitmap_py, m)?)?;
    m.add_function(wrap_pyfunction!(count_bitmap_py, m)?)?;
    m.add_function(wrap_pyfunction!(set_bit_py, m)?)?;
    m.add_function(wrap_pyfunction!(add_edge_py, m)?)?;
    m.add_function(wrap_pyfunction!(get_bytemap_size, m)?)?;
    m.add_function(wrap_pyfunction!(get_bitmap_size, m)?)?;
    Ok(())
}