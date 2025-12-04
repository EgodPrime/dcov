use pyo3::prelude::*;

mod bitmap;

use bitmap::{BitmapManager};


#[pymodule]
fn _core(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<BitmapManager>()?;
    Ok(())
}