use std::collections::HashMap;

type Table = HashMap<&'static str, HashMap<&'static str, (&'static str, &'static str)>>;

struct FSM {
    input_size: usize,
    output_size: usize,
    init_state: &'static str,
    table: Table,
}

struct Path {
    length: usize,
    sequence: String,
    observations: String,
}

impl Path {
    fn extend(&mut self, dist: usize, input: &str, output: &str) {
        self.length += dist;
        self.sequence += input;
        self.observations += output;
    }
}

impl Clone for Path {
    fn clone(&self) -> Self {
        Path {
            length: self.length,
            sequence: self.sequence.clone(),
            observations: self.observations.clone(),
        }
    }
}

type Paths = HashMap<&'static str, Path>;

fn hamming_dist(one: &str, two: &str) -> usize {
    assert!(one.len() == two.len());
    return one.chars().zip(two.chars()).filter(|(a, b)| a != b).count();
}

fn one_half() -> FSM {
    return FSM {
        input_size: 1,
        output_size: 2,
        init_state: "00",
        table: HashMap::from([
            (
                "00",
                HashMap::from([("0", ("00", "00")), ("1", ("10", "11"))]),
            ),
            (
                "01",
                HashMap::from([("0", ("00", "11")), ("1", ("10", "00"))]),
            ),
            (
                "10",
                HashMap::from([("0", ("01", "01")), ("1", ("11", "10"))]),
            ),
            (
                "11",
                HashMap::from([("0", ("10", "10")), ("1", ("11", "01"))]),
            ),
        ]),
    };
}

fn conv(fsm: &FSM, msg: &str) -> String {
    assert!(msg.len() % fsm.input_size == 0);

    let mut state = fsm.init_state;
    let mut result = String::from("");

    for i in (0..msg.len()).step_by(fsm.input_size) {
        let input = &msg[i..i + fsm.input_size];
        let (next, output) = fsm.table[state][input];
        result += output;
        state = next;
    }

    return result;
}

fn viterbi(fsm: &FSM, msg: &str) -> Path {
    assert!(msg.len() % fsm.output_size == 0);

    let start_path = Path {
        length: 0,
        sequence: String::from(""),
        observations: String::from(""),
    };
    let mut paths: Paths = HashMap::from([(fsm.init_state, start_path)]);

    for i in (0..msg.len()).step_by(fsm.output_size) {
        let symbol = &msg[i..i + fsm.output_size];
        let mut extended_paths: Paths = HashMap::new();

        for (tip, path) in paths {
            for (input, (next, output)) in &fsm.table[tip] {
                let dist = hamming_dist(symbol, output);
                let mut extended = path.clone();
                extended.extend(dist, input, output);

                if !extended_paths.contains_key(next)
                    || extended.length < extended_paths[next].length
                {
                    extended_paths.insert(next, extended);
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

fn test_conv() {
    let fsm: FSM = one_half();
    let msg: &'static str = "0001101101101100010111010111010101011110110000101001111100100010";
    let enc = conv(&fsm, msg);
    let dec = viterbi(&fsm, enc.as_str());
    println!("Original: {}", msg);
    println!("Encoded : {}", enc);
    println!("Received: {}", dec.observations);
    println!("Decoded : {}", dec.sequence);
    println!("{}", dec.sequence == msg);
}

fn main() {
    test_conv();
}
