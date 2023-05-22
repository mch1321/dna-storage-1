from choice_mechanism import gc_tracking, gc_tracked_random, random_choice
from constraints import default_constraints, wider_gc_limits
from experiments import Parameters


# EXP 1 - DEFAULT (5 RESERVED BITS, 35% < GC < 85%)
exp1 = Parameters(sequence_length=300, repetitions=20, random_seed=42)

# EXP 2 - 3 RESERVED BITS, 15% < GC < 85%
exp2 = Parameters(
    reserved_bits=3,
    constraints=wider_gc_limits(),
    sequence_length=300,
    repetitions=20,
    random_seed=42,
)

# EXP 3 - 4 RESERVED BITS, 25% < GC < 75%
exp3 = Parameters(
    reserved_bits=4,
    constraints=default_constraints(gc_min=0.25, gc_max=0.75),
    sequence_length=300,
    repetitions=20,
    random_seed=42,
)

# EXP 4 - SYMBOL LENGTH 5, 5 RESERVED BITS, 30% < GC 70%
exp4 = Parameters(
    symbol_size=5,
    constraints=default_constraints(
        symbol_size=5,
        gc_min=0.3,
        gc_max=0.7,
        restriction_sites=[],
    ),
    sequence_length=200,
    repetitions=20,
    random_seed=42,
)

# EXP 5 - DEFAULT LONGER SEQUENCE
exp5 = Parameters(
    sequence_length=600,
    repetitions=5,
)

# EXP 6 - GC TRACKING
exp6 = Parameters(
    sequence_length=600,
    choice_mechanism=gc_tracking,
    repetitions=5,
)

# EXP 7 - GC TRACKING + RANDOM
exp7 = Parameters(
    sequence_length=600,
    choice_mechanism=gc_tracked_random,
    repetitions=5,
)

# EXP 8 - 4 RESERVED BITS, 25% < GC < 75% (LONGER SEQUENCE)
exp8 = Parameters(
    reserved_bits=4,
    constraints=default_constraints(gc_min=0.25, gc_max=0.75),
    sequence_length=600,
    choice_mechanism=random_choice,
    repetitions=3,
)

# EXP 9 - 3 RESERVED BITS, 15% < GC < 85% (LONGER SEQUENCE)
exp9 = Parameters(
    reserved_bits=3,
    constraints=default_constraints(gc_min=0.15, gc_max=0.85),
    sequence_length=600,
    choice_mechanism=random_choice,
    repetitions=3,
)

# EXP 10 - GC TRACKING, SYMBOL SIZE 5, 5 RESERVED BITS, 25% < GC < 75% (SEQ 600)
exp10 = Parameters(
    symbol_size=5,
    reserved_bits=5,
    constraints=default_constraints(gc_min=0.25, gc_max=0.75, restriction_sites=[]),
    sequence_length=600,
    choice_mechanism=gc_tracking,
    repetitions=3,
)

# EXP 11 - RANDOM, SYMBOL SIZE 5, 5 RESERVED BITS, 25% < GC < 75% (SEQ 300)
# Shorter sequence for shorter run time
exp11 = Parameters(
    symbol_size=5,
    reserved_bits=5,
    constraints=default_constraints(gc_min=0.25, gc_max=0.75, restriction_sites=[]),
    sequence_length=300,
    choice_mechanism=random_choice,
    repetitions=3,
)

# EXP 11 - GC TRACKED RANDOM, SYMBOL SIZE 5, 5 RESERVED BITS, 25% < GC < 75%
config = Parameters(
    symbol_size=5,
    reserved_bits=5,
    constraints=default_constraints(gc_min=0.25, gc_max=0.75, restriction_sites=[]),
    sequence_length=600,
    choice_mechanism=gc_tracked_random,
    repetitions=3,
)

# CONF 1 - DEFAULT
conf1 = Parameters(
    sequence_length=300,
    error_rate=0.01,
    repetitions=10,
    random_seed=1704182,
)

# CONF 2 - GC TRACKING
conf2 = Parameters(
    sequence_length=300,
    choice_mechanism=gc_tracking,
    error_rate=0.01,
    repetitions=10,
    random_seed=1704182,
)

# CONF 3 - GC TRACKING + RANDOM
conf3 = Parameters(
    sequence_length=300,
    choice_mechanism=gc_tracked_random,
    error_rate=0.01,
    repetitions=10,
    random_seed=1704182,
)

# CONF 4 - 4 RESERVED BITS
conf4 = Parameters(
    reserved_bits=4,
    sequence_length=300,
    choice_mechanism=random_choice,
    error_rate=0.01,
    repetitions=10,
    random_seed=1704182,
)
