use mechanisms::{
    gc_tracked_random, gc_tracking, most_different, most_similar, parity, random_choice,
};
use pyo3::prelude::*;
use rand::{rngs::StdRng, SeedableRng};
mod constraints;
mod fsm;
mod mapping;
mod mechanisms;

pub type Constraints = (f32, f32, usize, Vec<String>);

// Converts nucleotides to bits.
#[pyfunction]
fn dna_to_bits(seq: &str) -> String {
    return mapping::dna_to_bits(seq);
}

// Converts bits to nucleotides.
#[pyfunction]
fn bits_to_dna(seq: &str) -> String {
    return mapping::bits_to_dna(seq);
}

// Uses the random choice mechanism to construct an FSM given constraints.
#[pyfunction]
fn random_fsm(
    symbol_size: usize,
    reserved_bits: usize,
    init_state: String,
    constraints: Constraints,
    seed: u64,
) -> fsm::FSM {
    let mut rng: StdRng = SeedableRng::seed_from_u64(seed);

    return generate_fsm(
        symbol_size,
        reserved_bits,
        init_state,
        constraints,
        |_, _, r| random_choice(r, &mut rng),
    );
}

// Uses the GC-tracking mechanism to construct an FSM given constraints.
#[pyfunction]
fn gc_tracking_fsm(
    symbol_size: usize,
    reserved_bits: usize,
    init_state: String,
    constraints: Constraints,
) -> fsm::FSM {
    return generate_fsm(
        symbol_size,
        reserved_bits,
        init_state,
        constraints,
        gc_tracking,
    );
}

// Uses the GC-tracked Random mechanism to construct an FSM given constraints.
#[pyfunction]
fn gc_tracked_random_fsm(
    symbol_size: usize,
    reserved_bits: usize,
    init_state: String,
    constraints: Constraints,
    seed: u64,
) -> fsm::FSM {
    let mut rng: StdRng = SeedableRng::seed_from_u64(seed);

    return generate_fsm(
        symbol_size,
        reserved_bits,
        init_state,
        constraints,
        |s, i, r| gc_tracked_random(s, i, r, &mut rng),
    );
}

// Uses the most similar mechanism to construct an FSM given constraints.
#[pyfunction]
fn most_similar_fsm(
    symbol_size: usize,
    reserved_bits: usize,
    init_state: String,
    constraints: Constraints,
    seed: u64,
) -> fsm::FSM {
    let mut rng: StdRng = SeedableRng::seed_from_u64(seed);

    return generate_fsm(
        symbol_size,
        reserved_bits,
        init_state,
        constraints,
        |s, i, r| most_similar(s, i, r, &mut rng),
    );
}

// Uses the most different mechanism to construct an FSM given constraints.
#[pyfunction]
fn most_different_fsm(
    symbol_size: usize,
    reserved_bits: usize,
    init_state: String,
    constraints: Constraints,
    seed: u64,
) -> fsm::FSM {
    let mut rng: StdRng = SeedableRng::seed_from_u64(seed);

    return generate_fsm(
        symbol_size,
        reserved_bits,
        init_state,
        constraints,
        |s, i, r| most_different(s, i, r, &mut rng),
    );
}

// Uses the parity mechanism to construct an FSM given constraints.
#[pyfunction]
fn parity_fsm(
    symbol_size: usize,
    reserved_bits: usize,
    init_state: String,
    constraints: Constraints,
    seed: u64,
) -> fsm::FSM {
    let mut rng: StdRng = SeedableRng::seed_from_u64(seed);

    return generate_fsm(
        symbol_size,
        reserved_bits,
        init_state,
        constraints,
        |s, i, r| parity(s, i, r, &mut rng),
    );
}

// Constructs an FSM given constraints and a choice mechanism.
fn generate_fsm(
    symbol_size: usize,
    reserved_bits: usize,
    init_state: String,
    constraints: Constraints,
    mechanism: impl FnMut(&str, &str, Vec<String>) -> String,
) -> fsm::FSM {
    let output_size = symbol_size * 2;
    let input_size = output_size - reserved_bits;

    return fsm::construct_fsm(
        input_size,
        output_size,
        init_state,
        constraints::Constraints {
            gc_min: constraints.0,
            gc_max: constraints.1,
            max_run_length: constraints.2,
            reserved: constraints.3,
        },
        mechanism,
    );
}

/// A Python for FSM-based encodings implemented in Rust.
#[pymodule]
fn encoding(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(dna_to_bits, m)?)?;
    m.add_function(wrap_pyfunction!(bits_to_dna, m)?)?;
    m.add_function(wrap_pyfunction!(random_fsm, m)?)?;
    m.add_function(wrap_pyfunction!(gc_tracking_fsm, m)?)?;
    m.add_function(wrap_pyfunction!(gc_tracked_random_fsm, m)?)?;
    m.add_function(wrap_pyfunction!(most_similar_fsm, m)?)?;
    m.add_function(wrap_pyfunction!(most_different_fsm, m)?)?;
    m.add_function(wrap_pyfunction!(parity_fsm, m)?)?;
    Ok(())
}
