use std::collections::HashMap;
use std::iter::zip;

use rand::rngs::StdRng;
use rand::seq::SliceRandom;

use crate::bits_to_dna;
use crate::constraints::gc_content;
use once_cell::sync::Lazy;

pub(crate) fn random_choice(reserved: Vec<String>, rng: &mut StdRng) -> String {
    return reserved.choose(rng).unwrap().to_string();
}

pub(crate) fn gc_tracking(state: &str, input: &str, reserved: Vec<String>) -> String {
    let mut closest: String = reserved[0].clone();
    let mut min_diff: f32 = 1.0;
    let gc_target: f32 = 0.5;

    for candidate in reserved {
        let concat = state.to_string() + &candidate + input;
        let gc_content = gc_content(&bits_to_dna(&concat));
        let diff = (gc_target - gc_content).abs();

        if diff == 0.0 {
            return candidate;
        }

        if diff < min_diff {
            min_diff = diff;
            closest = candidate;
        }
    }

    return closest;
}

pub(crate) fn gc_tracked_random(
    state: &str,
    input: &str,
    reserved: Vec<String>,
    rng: &mut StdRng,
) -> String {
    let mut closest: Vec<String> = Vec::new();
    let mut min_diff: f32 = 1.0;
    let gc_target: f32 = 0.5;

    for candidate in reserved {
        let concat = state.to_string() + &candidate + input;
        let gc_content = gc_content(&bits_to_dna(&concat));
        let diff = (gc_target - gc_content).abs();

        if diff < min_diff {
            min_diff = diff;
            closest.clear();
            closest.push(candidate);
        } else if diff == min_diff {
            closest.push(candidate);
        }
    }

    return closest.choose(rng).unwrap().to_string();
}

fn hamming_dist(one: &str, two: &str) -> usize {
    assert!(one.len() == two.len());
    return one
        .chars()
        .zip(two.chars())
        .filter(|(a, b)| *a != *b)
        .count();
}

pub(crate) fn most_similar(
    state: &str,
    input: &str,
    reserved: Vec<String>,
    rng: &mut StdRng,
) -> String {
    assert!(input.len() * 2 == state.len());

    let mut closest: Vec<String> = Vec::new();
    let mut min_diff: usize = input.len();

    for candidate in reserved {
        let diff = hamming_dist(input, &candidate);

        if diff < min_diff {
            min_diff = diff;
            closest.clear();
            closest.push(candidate);
        } else if diff == min_diff {
            closest.push(candidate);
        }
    }

    return closest.choose(rng).unwrap().to_string();
}

pub(crate) fn most_different(
    state: &str,
    input: &str,
    reserved: Vec<String>,
    rng: &mut StdRng,
) -> String {
    assert!(input.len() * 2 == state.len());

    let mut closest: Vec<String> = Vec::new();
    let mut max_diff: usize = 0;

    for candidate in reserved {
        let diff = hamming_dist(input, &candidate);

        if diff > max_diff {
            max_diff = diff;
            closest.clear();
            closest.push(candidate);
        } else if diff == max_diff {
            closest.push(candidate);
        }
    }

    return closest.choose(rng).unwrap().to_string();
}

fn str_xor(one: &str, two: &str) -> String {
    assert!(one.len() == two.len());

    let mut res = String::new();

    for (a, b) in zip(one.chars(), two.chars()) {
        res.push(if a == b { '0' } else { '1' });
    }

    return res;
}

pub(crate) fn xor(state: &str, input: &str, reserved: Vec<String>, rng: &mut StdRng) -> String {
    assert!(input.len() * 2 == state.len());

    let mut closest: Vec<String> = Vec::new();
    let mut min_diff: usize = input.len();

    let xor = str_xor(
        str_xor(
            &state[0..state.len() / 2],
            &state[state.len() / 2..state.len()],
        )
        .as_str(),
        input,
    );

    for candidate in reserved {
        let diff = hamming_dist(&xor, &candidate);

        if diff < min_diff {
            min_diff = diff;
            closest.clear();
            closest.push(candidate);
        } else if diff == min_diff {
            closest.push(candidate);
        }
    }

    return closest.choose(rng).unwrap().to_string();
}

fn even_parity(seq: &str) -> bool {
    return seq.chars().filter(|c| *c == '1').count() % 2 == 0;
}

pub(crate) fn parity(state: &str, input: &str, reserved: Vec<String>, rng: &mut StdRng) -> String {
    let mut even: Vec<String> = Vec::new();

    for candidate in &reserved {
        let concat = state.to_string() + &candidate + input;
        if even_parity(&concat) {
            even.push(candidate.to_string());
        }
    }

    if even.is_empty() {
        return random_choice(reserved, rng);
    }

    return even.choose(rng).unwrap().to_string();
}

pub(crate) fn alt_parity(
    state: &str,
    input: &str,
    reserved: Vec<String>,
    rng: &mut StdRng,
) -> String {
    let mut alt: Vec<String> = Vec::new();
    let state_parity = even_parity(state);
    for candidate in &reserved {
        let next_parity = even_parity(&(candidate.to_owned() + input));
        if state_parity != next_parity {
            alt.push(candidate.to_string());
        }
    }

    if alt.is_empty() {
        return random_choice(reserved, rng);
    }

    return alt.choose(rng).unwrap().to_string();
}

// state variable used to track used reserved bit sequences. Bad code - refactor.
pub(crate) static mut USED: Lazy<HashMap<String, Vec<String>>> = Lazy::new(|| HashMap::new());

pub(crate) fn random_unused(input: &str, reserved: Vec<String>, rng: &mut StdRng) -> String {
    let mut diff: Vec<String> = vec![];

    unsafe {
        if !USED.contains_key(input) {
            USED.insert(input.to_string(), Vec::new());
        }

        let used = USED.get(input).unwrap();
        for r in &reserved {
            if !used.contains(r) {
                diff.push(r.to_string());
            }
        }

        if diff.is_empty() {
            return reserved.choose(rng).unwrap().to_string();
        }

        let choice = diff.choose(rng).unwrap().to_string();
        USED.get_mut(input).unwrap().push(choice.clone());
        return choice;
    }
}
