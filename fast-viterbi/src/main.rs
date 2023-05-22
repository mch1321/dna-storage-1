use std::collections::HashMap;
mod fsm;

fn one_half() -> fsm::FSM {
    return fsm::FSM {
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

fn test_conv() {
    let fsm: fsm::FSM = one_half();
    let msg: &'static str = "0001101101101100010111010111010101011110110000101001111100100010";
    let enc = fsm::conv(&fsm, msg);
    let dec = fsm::viterbi(&fsm, enc.as_str());
    println!("Original: {}", msg);
    println!("Encoded : {}", enc);
    println!("Received: {}", dec.observations);
    println!("Decoded : {}", dec.sequence);
    println!("{}", dec.sequence == msg);
}

fn main() {
    test_conv();
}
