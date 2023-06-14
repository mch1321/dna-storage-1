use pyo3::prelude::*;
mod constraints;
mod conv;

// Public types
pub type Constraints = (f32, f32, usize, Vec<String>);
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

// Constraint-driven decoder.
#[pyfunction]
fn constraint_decode(fsm: FSM, constraints: Constraints, msg: String) -> Path {
    let path = conv::constraint_viterbi(
        &conv::FSM {
            input_size: fsm.0,
            output_size: fsm.1,
            init_state: fsm.2,
            table: fsm.3,
        },
        constraints::Constraints {
            gc_min: constraints.0,
            gc_max: constraints.1,
            max_run_length: constraints.2,
            reserved: constraints.3,
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
    m.add_function(wrap_pyfunction!(constraint_decode, m)?)?;
    Ok(())
}
