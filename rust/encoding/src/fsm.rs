use crate::constraints::Constraints;
use crate::mapping::bits_to_dna;
use core::panic;
use std::collections::HashMap;

pub(crate) type FSM = (usize, usize, String, Table);
type Table = HashMap<String, HashMap<String, (String, String)>>;

fn populate_space(size: usize) -> Vec<String> {
    let mut space: Vec<String> = Vec::new();
    let dim = usize::pow(2, size as u32);
    for i in 0..dim {
        let bin = format!("{i:b}");
        let padding = size - bin.len();
        space.push("0".repeat(padding) + &bin);
    }
    return space;
}

fn construct_table(
    input_size: usize,
    output_size: usize,
    constraints: Constraints,
    mut mechanism: impl FnMut(&str, &str, Vec<String>) -> String,
) -> Table {
    assert!(input_size < output_size);

    let mut table: Table = HashMap::new();

    let reserved_size = output_size - input_size;
    let states = populate_space(output_size);
    let inputs = populate_space(input_size);
    let reserved = populate_space(reserved_size);

    for s in &states {
        table.insert(s.clone(), HashMap::new());
        for i in &inputs {
            let mut candidates: Vec<String> = Vec::new();
            for r in &reserved {
                if constraints.satisfied(bits_to_dna(&(s.to_owned() + r + i))) {
                    candidates.push(r.to_string());
                }
            }
            if candidates.is_empty() {
                panic!("Impossible to meet constraints!");
            }

            let chosen = mechanism(&s, &i, candidates);
            let output = chosen + &i;
            table
                .get_mut(s)
                .unwrap()
                .insert(i.to_string(), (output.clone(), output));
        }
    }

    return table;
}

pub(crate) fn construct_fsm(
    input_size: usize,
    output_size: usize,
    init_state: String,
    constraints: Constraints,
    mechanism: impl FnMut(&str, &str, Vec<String>) -> String,
) -> FSM {
    return (
        input_size,
        output_size,
        init_state,
        construct_table(input_size, output_size, constraints, mechanism),
    );
}
