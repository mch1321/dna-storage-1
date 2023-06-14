use std::collections::HashMap;

use crate::constraints::Constraints;
pub(crate) type Table = HashMap<String, HashMap<String, (String, String)>>;

pub(crate) struct FSM {
    pub(crate) input_size: usize,
    pub(crate) output_size: usize,
    pub(crate) init_state: String,
    pub(crate) table: Table,
}

pub(crate) struct Path {
    pub(crate) length: usize,
    pub(crate) sequence: String,
    pub(crate) observations: String,
    // tip: Option<String>,
}

impl Path {
    fn extend(&mut self, dist: usize, input: String, output: String) {
        self.length += dist;
        self.sequence += &input;
        self.observations += &output;
        // self.tip = Option::from(output);
    }
}

impl Clone for Path {
    fn clone(&self) -> Self {
        Path {
            length: self.length,
            sequence: self.sequence.clone(),
            observations: self.observations.clone(),
            // tip: self.tip.clone(),
        }
    }
}

type Paths = HashMap<String, Path>;

fn hamming_dist(one: &str, two: &str) -> usize {
    assert!(one.len() == two.len());
    return one.chars().zip(two.chars()).filter(|(a, b)| a != b).count();
}

pub(crate) fn conv(fsm: &FSM, msg: String) -> String {
    assert!(msg.len() % fsm.input_size == 0);

    let mut state = &fsm.init_state;
    let mut result = String::from("");

    for i in (0..msg.len()).step_by(fsm.input_size) {
        let input = &msg[i..i + fsm.input_size];
        let (next, output) = &fsm.table[state][input];
        result += output;
        state = next;
    }

    return result;
}

fn even_parity(seq: &str) -> bool {
    return seq.chars().filter(|c| *c == '1').count() % 2 == 0;
}

pub(crate) fn viterbi(fsm: &FSM, msg: String) -> Path {
    assert!(msg.len() % fsm.output_size == 0);

    let start_path = Path {
        length: 0,
        sequence: String::from(""),
        observations: String::from(""),
        // tip: None,
    };
    let mut paths: Paths = HashMap::from([(fsm.init_state.to_string(), start_path)]);

    for i in (0..msg.len()).step_by(fsm.output_size) {
        let symbol = &msg[i..i + fsm.output_size];
        let mut extended_paths: Paths = HashMap::new();

        for (tip, path) in paths {
            for (input, (next, output)) in &fsm.table[&tip] {
                let dist = hamming_dist(symbol, output);
                let mut extended = path.clone();
                // let tip: Option<String> = extended.tip.clone();
                extended.extend(dist, input.to_string(), output.to_string());

                // if tip.is_some() && (even_parity(&tip.unwrap()) != even_parity(&output)) {
                //     extended.length += 1000;
                // }

                if !extended_paths.contains_key(next)
                    || extended.length < extended_paths[next].length
                {
                    extended_paths.insert(next.to_string(), extended);
                } else if extended.length == extended_paths[next].length {
                    let len = extended.observations.len();
                    if len > fsm.output_size * 2 {
                        let prev = &extended.observations
                            [len - fsm.output_size * 2..len - fsm.output_size];
                        let curr = &extended.observations[len - fsm.output_size..len];
                        let path_prev = &extended_paths[next].observations
                            [len - fsm.output_size * 2..len - fsm.output_size];
                        let path_curr =
                            &extended_paths[next].observations[len - fsm.output_size..len];

                        if even_parity(path_prev) == even_parity(path_curr)
                            && even_parity(prev) != even_parity(curr)
                        {
                            extended_paths.insert(next.to_string(), extended);
                        }
                    }
                }
            }
        }

        paths = extended_paths;
    }

    return paths
        .values()
        .reduce(|a, b| if a.length < b.length { a } else { b })
        .unwrap()
        .clone();
}

pub(crate) fn constraint_viterbi(fsm: &FSM, constraints: Constraints, msg: String) -> Path {
    assert!(msg.len() % fsm.output_size == 0);

    let start_path = Path {
        length: 0,
        sequence: String::from(""),
        observations: String::from(""),
        // tip: None,
    };
    let mut paths: Paths = HashMap::from([(fsm.init_state.to_string(), start_path)]);

    for i in (0..msg.len()).step_by(fsm.output_size) {
        let symbol = &msg[i..i + fsm.output_size];
        let mut extended_paths: Paths = HashMap::new();

        for (tip, path) in paths {
            for (input, (next, output)) in &fsm.table[&tip] {
                let dist = hamming_dist(symbol, output);
                let mut extended = path.clone();
                // let tip: Option<String> = extended.tip.clone();
                extended.extend(dist, input.to_string(), output.to_string());

                // Add Constraint Penalty
                let len = extended.observations.len();
                if len > fsm.output_size * 2 {
                    if !constraints.satisfied(
                        extended.observations[len - fsm.output_size * 2..len].to_string(),
                    ) {
                        extended.length += 1000;
                    }
                }

                // Add Parity Penalty
                // if tip.is_some() && (even_parity(&tip.unwrap()) != even_parity(&output)) {
                //     extended.length += 1000;
                // }

                if !extended_paths.contains_key(next)
                    || extended.length < extended_paths[next].length
                {
                    extended_paths.insert(next.to_string(), extended);
                } else if extended.length == extended_paths[next].length {
                    let len = extended.observations.len();
                    if len > fsm.output_size * 2 {
                        let prev = &extended.observations
                            [len - fsm.output_size * 2..len - fsm.output_size];
                        let curr = &extended.observations[len - fsm.output_size..len];
                        let path_prev = &extended_paths[next].observations
                            [len - fsm.output_size * 2..len - fsm.output_size];
                        let path_curr =
                            &extended_paths[next].observations[len - fsm.output_size..len];

                        if even_parity(path_prev) == even_parity(path_curr)
                            && even_parity(prev) != even_parity(curr)
                        {
                            extended_paths.insert(next.to_string(), extended);
                        }
                    }
                }
            }
        }

        paths = extended_paths;
    }

    return paths
        .values()
        .reduce(|a, b| if a.length < b.length { a } else { b })
        .unwrap()
        .clone();
}
