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
    symbol_size, reserved_bits, init_state, constraints, 123456)

output1 = [] #empty list
output2 = []
output3 = []
output4 = []
output5 = []

for x in range(100):

    start_1 = time.time()
    enc = viterbi.encode(fsm, eg)
    section1_time = time.time() - start_1

    start_2 = time.time()
    dna = encoding.bits_to_dna(enc)
    section2_time = time.time() - start_2

    start_3 = time.time()
    err = inject_base_errors(dna, 0.05)
    section3_time = time.time() - start_3

    start_4 = time.time()
    rec = encoding.dna_to_bits(err)
    section4_time = time.time() - start_4

    start_5 = time.time()
    (l, seq, obs) = viterbi.decode(fsm, rec)
    section5_time = time.time() - start_5


    output1.append(section1_time)
    output2.append(section2_time)
    output3.append(section3_time)
    output4.append(section4_time)
    output5.append(section5_time)
    
    
print('Section 1: ', output1)



