import time
import viterbi
import encoding
from constraints import default_constraints
from utils import inject_base_errors, hamming_dist

symbol_size = 4
reserved_bits = 4
init_state = "0" * 8

eg = "01010101010000111101"

c = default_constraints()
constraints = (0.15, 0.85, c.max_run_length, c.reserved)
fsm = encoding.random_fsm(
    symbol_size, reserved_bits, init_state, constraints, 123456
)
print(eg)
start = time.time()
enc = viterbi.encode(fsm, eg)
duration = time.time() - start
print(f"Encoding took {duration} seconds.")
print(enc)
dna = encoding.bits_to_dna(enc)
print(dna)
err = inject_base_errors(dna, 0.05)
print(err)
print(f"Number of errors injected: {hamming_dist(dna, err)}")
rec = encoding.dna_to_bits(err)
print(rec)
(l, seq, obs) = viterbi.decode(fsm, rec)
print(seq)
print(f"Number of errors remaining: {hamming_dist(eg, seq)}")

