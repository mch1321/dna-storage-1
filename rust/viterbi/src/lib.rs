use std::collections::HashMap;

use pyo3::prelude::*;
mod constraints;
mod conv;

// Public types
pub type Constraints = (f32, f32, usize, Vec<String>);
pub type FSM = (usize, usize, String, conv::Table);
pub type Path = (usize, String, String);

// Returns an FSM for a 1/2 encoding.
#[pyfunction]
fn one_half() -> FSM {
    let mut table: conv::Table = HashMap::new();
    let states = ["00", "01", "10", "11"];
    let inputs = ["0", "1"];
    let transitions = [
        [("00", "00"), ("10", "11")],
        [("00", "11"), ("10", "00")],
        [("01", "01"), ("11", "10")],
        [("10", "10"), ("11", "01")],
    ];

    for (s, state) in states.iter().enumerate() {
        table.insert(state.to_string(), HashMap::new());
        for (i, input) in inputs.iter().enumerate() {
            let t = transitions[s][i];
            table
                .get_mut(&state.to_string())
                .unwrap()
                .insert(input.to_string(), (String::from(t.0), String::from(t.1)));
        }
    }

    return (1, 2, String::from("00"), table);
}

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
    m.add_function(wrap_pyfunction!(one_half, m)?)?;
    m.add_function(wrap_pyfunction!(encode, m)?)?;
    m.add_function(wrap_pyfunction!(decode, m)?)?;
    m.add_function(wrap_pyfunction!(constraint_decode, m)?)?;
    Ok(())
}
