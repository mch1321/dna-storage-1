import encoding
import viterbi
from constraints import standard_constraints
from dna_mapping import bits_to_dna, dna_to_bits
from utils import rand_bases, rand_bit_string

homopolymers = "A" * 10 + "C" * 10 + "G" * 15 + "T" * 10
strs = "ACGT" * 5 + "TGA" * 5 + "GCTAG" * 4
low_gc = rand_bases(exclude=["C", "G"], length=40)
high_gc = rand_bases(exclude=["A", "T"], length=40)

pathalogical = homopolymers + strs + low_gc + high_gc

if __name__ == "__main__":
    print(len(pathalogical))
    print(pathalogical)
    bits = dna_to_bits(pathalogical)

    symbol_size = 4
    reserved_bits = 4
    output_size = symbol_size * 2
    input_size = output_size - reserved_bits
    init_state = "0" * output_size
    seed = 42

    c = standard_constraints(symbol_size=symbol_size, reserved_bits=reserved_bits)
    constraints = (
        c.gc_min,
        c.gc_max,
        c.str_lower,
        c.str_upper,
        c.max_run_length,
        c.reserved,
    )

    fsm = encoding.random_fsm(symbol_size, reserved_bits, init_state, constraints, 42)
    enc = bits_to_dna(viterbi.encode(fsm, bits))
    print(enc)
