def enc_base(bits: str) -> str:
    if bits == "00":
        return "A"
    elif bits == "01":
        return "C"
    elif bits == "10":
        return "G"
    elif bits == "11":
        return "T"
    else:
        raise Exception(f"Error trying to encode {bits} to a base pair.")


def dec_base(base: str) -> str:
    if base == "A":
        return "00"
    elif base == "C":
        return "01"
    elif base == "G":
        return "10"
    elif base == "T":
        return "11"
    else:
        raise Exception(f"Error trying to decode {base} into bits.")


def bits_to_dna(seq: str) -> str:
    if len(seq) % 2 != 0:
        raise Exception("Sequence must be of even length to encode into nucleotides.")

    return "".join([enc_base(seq[i : i + 2]) for i in range(0, len(seq), 2)])


def dna_to_bits(seq: str) -> str:
    return "".join(map(dec_base, seq))
