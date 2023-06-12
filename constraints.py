from dataclasses import dataclass
from utils import gc_content, longest_homopolymer, contains_reserved


@dataclass
class Constraints:
    gc_min: float
    gc_max: float
    max_run_length: int
    reserved: list[str]

    def satisfied(self, sequence: str) -> bool:
        gc = gc_content(sequence)
        return (
            self.gc_min <= gc
            and gc <= self.gc_max
            and longest_homopolymer(sequence) <= self.max_run_length
            and not contains_reserved(sequence, self.reserved)
        )

    def __str__(self):
        return (
            f"GC Min: {self.gc_min}\n"
            + f"GC Max: {self.gc_max}\n"
            + f"Max Run Length: {self.max_run_length}\n"
            + f"Reserved: {self.reserved}"
        )

    def short_str(self):
        return f"{self.gc_min} <= GC <= {self.gc_max}, Max Run Length: {self.max_run_length}"


def standard_constraints(symbol_size: int, reserved_bits: int):
    if symbol_size == 3:
        if reserved_bits == 2:
            return default_constraints(gc_min=0.16, gc_max=0.84)
        if reserved_bits == 3:
            return default_constraints(gc_min=0.33, gc_max=0.67)
        if reserved_bits == 4:
            return default_constraints(gc_min=0.33, gc_max=0.67)
        else:
            raise Exception(
                "No standard constraints for reserved bits other than 2, 3 and 4."
            )
    if symbol_size == 4:
        if reserved_bits == 3:
            return default_constraints(gc_min=0.15, gc_max=0.85)
        elif reserved_bits == 4:
            return default_constraints(gc_min=0.25, gc_max=0.75)
        elif reserved_bits == 5:
            return default_constraints()
        else:
            raise Exception(
                "No standard constraints for reserved bits other than 3, 4 and 5."
            )
    elif symbol_size == 5:
        if reserved_bits == 3:
            return default_constraints(gc_min=0.15, gc_max=0.85, restriction_sites=[])
        elif reserved_bits == 4:
            return default_constraints(gc_min=0.2, gc_max=0.8, restriction_sites=[])
        elif reserved_bits == 5:
            return default_constraints(gc_min=0.25, gc_max=0.75, restriction_sites=[])
        else:
            raise Exception(
                "No standard constraints for reserved bits other than 3, 4 and 5."
            )
    else:
        raise Exception("No standard constraints for symbol sizes other than 4 and 5.")


def default_constraints(
    symbol_size: int = 4,
    max_run_length: int = 8,
    gc_min: float = 0.35,
    gc_max: float = 0.65,
    restriction_sites: list[str] = ["GAGTC"],
    primers: list[str] = [
        "GAACCGTGCCGAGTCTGAGC",  # start primer
        "CTCAGGACTCGCAACGCTGG",  # end primer
        "GCGACTGGATGACCTGACGC",  # partssup table id primer
        "GCAGACCGGAGACCTGTCGG",  # parts table id primer
    ],
) -> Constraints:
    concat_size = 2 * symbol_size

    regexes = []
    regexes.extend(restriction_sites)

    for primer in primers:
        for i in range(len(primer) - concat_size + 1):
            regexes.append(primer[i : i + concat_size])

    return Constraints(gc_min, gc_max, max_run_length, regexes)


def wider_gc_limits() -> Constraints:
    return default_constraints(gc_min=0.15, gc_max=0.85)


if __name__ == "__main__":
    print(default_constraints())
