pub(crate) struct Constraints {
    pub(crate) gc_min: f32,
    pub(crate) gc_max: f32,
    pub(crate) str_lower: usize,
    pub(crate) str_upper: usize,
    pub(crate) max_run_length: usize,
    pub(crate) reserved: Vec<String>,
}

impl Constraints {
    pub(crate) fn satisfied(&self, seq: String) -> bool {
        assert!(self.str_upper * 2 <= seq.len());
        assert!(self.str_lower <= self.str_upper);

        let gc_content: f32 = gc_content(&seq);

        return self.gc_min <= gc_content
            && gc_content <= self.gc_max
            && longest_homopolymer(&seq) <= self.max_run_length
            && !str_present(&seq, self.str_lower, self.str_upper)
            && !contains_subsequence(&self.reserved, &seq);
    }
}

pub(crate) fn gc_content(seq: &str) -> f32 {
    return seq.chars().filter(|c| *c == 'G' || *c == 'C').count() as f32 / seq.len() as f32;
}

fn str_present(seq: &str, lower: usize, upper: usize) -> bool {
    for size in lower..=upper {
        for i in 0..=seq.len() - (size * 2) {
            if seq[i..i + size] == seq[i + size..i + (size * 2)] {
                return true;
            }
        }
    }
    return false;
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
