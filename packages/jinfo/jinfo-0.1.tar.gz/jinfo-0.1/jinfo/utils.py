def one_hot_dna(input_seq_str: str, max_seq_len: int):
    """
    One hot encode a string format dna sequence.
    Add zero padding up to the maximum length.
    Returns: 1D numpy array of length 4*max_seq_len
    """
    import numpy as np

    encode_dict = {
        "A": [1, 0, 0, 0],
        "T": [0, 1, 0, 0],
        "C": [0, 0, 1, 0],
        "G": [0, 0, 0, 1],
        "X": [0, 0, 0, 0],
    }
    input_seq_upper = input_seq_str.upper()
    padding = "".join(["X" for i in range(max_seq_len - len(input_seq_str))])
    encoded_dna = [encode_dict[base] for base in input_seq_upper + padding]
    np_encoded = np.array(encoded_dna, dtype=int)
    return np_encoded.flatten()


def random_dna(seq_length: int) -> str:
    """
    Generate a random DNA sequence for primer design
    Returns: String of length seq_length
    """
    import random

    dna_base_list = ["A", "T", "C", "G"]
    seq_list = [random.choice(dna_base_list) for i in range(seq_length)]
    return "".join(seq_list)


def DNASeq_from_NCBI():
    """
    Fetch a DNA sequence using the NCBI Entrez api
    Returns ji.DNASeq object
    """
    from jinfo.sequence import DNASeq

    return


if __name__ == "__main__":
    pass
