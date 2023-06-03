use rand::rngs::StdRng;
use rand::seq::SliceRandom;

use crate::constraints::gc_content;

pub(crate) fn random_choice(reserved: Vec<String>, rng: &mut StdRng) -> String {
    return reserved.choose(rng).unwrap().to_string();
}

pub(crate) fn gc_tracking(state: &str, input: &str, reserved: Vec<String>) -> String {
    let mut closest: String = reserved[0].clone();
    let mut min_diff: f32 = 1.0;
    let gc_target: f32 = 0.5;

    for candidate in reserved {
        let concat = state.to_string() + input + &candidate;
        let gc_content = gc_content(&concat);
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
        let concat = state.to_string() + input + &candidate;
        let gc_content = gc_content(&concat);
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
    return one.chars().zip(two.chars()).filter(|(a, b)| a != b).count();
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
