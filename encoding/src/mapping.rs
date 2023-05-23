fn enc_base(bits: &str) -> char {
    match bits {
        "00" => 'A',
        "01" => 'C',
        "10" => 'G',
        "11" => 'T',
        _ => panic!("No base mapping for {}.", bits),
    }
}

fn dec_base(base: char) -> String {
    String::from(match base {
        'A' => "00",
        'C' => "01",
        'G' => "10",
        'T' => "11",
        _ => panic!("Invalid base {}.", base),
    })
}

pub(crate) fn bits_to_dna(seq: &str) -> String {
    assert!(seq.len() % 2 == 0);

    return (0..seq.len())
        .step_by(2)
        .map(|i| enc_base(&seq[i..i + 2]))
        .collect::<String>();
}

pub(crate) fn dna_to_bits(seq: &str) -> String {
    return seq.chars().map(dec_base).collect::<String>();
}
