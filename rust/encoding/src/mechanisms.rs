use rand::rngs::StdRng;
use rand::seq::SliceRandom;
use rand::SeedableRng;

use crate::constraints::gc_content;

pub(crate) fn random_choice(reserved: Vec<String>, seed: u64) -> String {
    let mut rng: StdRng = SeedableRng::seed_from_u64(seed);
    return reserved.choose(&mut rng).unwrap().to_string();
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
    seed: u64,
) -> String {
    let mut rng: StdRng = SeedableRng::seed_from_u64(seed);
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

    return closest.choose(&mut rng).unwrap().to_string();
}
