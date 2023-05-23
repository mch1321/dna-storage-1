use pyo3::prelude::*;
mod conv;

// Public types
pub type FSM = (usize, usize, String, conv::Table);
pub type Path = (usize, String, String);

// Convolutional encoder.
#[pyfunction]
fn encode(fsm: FSM, msg: String) -> String {
    return conv::conv(
        &conv::FSM {
            input_size: fsm.0,
            output_size: fsm.1,
            init_state: fsm.2,
            table: fsm.3,
        },
        msg,
    );
}

// Viterbi decoder.
#[pyfunction]
fn decode(fsm: FSM, msg: String) -> Path {
    let path = conv::viterbi(
        &conv::FSM {
            input_size: fsm.0,
            output_size: fsm.1,
            init_state: fsm.2,
            table: fsm.3,
        },
        msg,
    );
    return (path.length, path.sequence, path.observations);
}

/// A Python module for convolutional codes implemented in Rust.
#[pymodule]
fn viterbi(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(encode, m)?)?;
    m.add_function(wrap_pyfunction!(decode, m)?)?;
    Ok(())
}
