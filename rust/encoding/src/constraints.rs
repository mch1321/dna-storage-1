pub(crate) struct Constraints {
    pub(crate) gc_min: f32,
    pub(crate) gc_max: f32,
    pub(crate) max_run_length: usize,
    pub(crate) reserved: Vec<String>,
}

impl Constraints {
    pub(crate) fn satisfied(&self, seq: String) -> bool {
        let gc_content: f32 = gc_content(&seq);

        return self.gc_min <= gc_content
            && gc_content <= self.gc_max
            && longest_homopolymer(&seq) <= self.max_run_length
            && !contains_subsequence(&self.reserved, &seq);
    }
}

pub(crate) fn gc_content(seq: &str) -> f32 {
    return seq.chars().filter(|c| c == &'G' || c == &'C').count() as f32 / seq.len() as f32;
}

fn longest_homopolymer(seq: &str) -> usize {
    let mut longest: usize = 0;
    let mut count: usize = 0;
    let mut curr = seq.chars().nth(0).unwrap();

    for base in seq.chars() {
        if base == curr {
            count += 1;
            if count > longest {
                longest = count;
            }
        } else {
            count = 1;
        }

        curr = base;
    }

    return longest;
}

fn contains_subsequence(reserved: &Vec<String>, seq: &str) -> bool {
    return reserved.into_iter().any(|r| seq.contains(r));
}
