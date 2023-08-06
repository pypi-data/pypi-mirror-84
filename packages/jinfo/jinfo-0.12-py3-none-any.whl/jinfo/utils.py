class MuscleNotInstalledError(Exception):
    pass


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


def seq_list_to_fasta(
    seq_list: list, file_name: str = None, label_list: list = None
) -> str:
    """
    Covnert a list of Seq objects to a fasta format string
    Optionally add labels and save to file
    Returns: fasta string
    """
    fasta_str = ""
    for i, seq_obj in enumerate(seq_list):
        if label_list:
            label = label_list[i]
        elif seq_obj.label != "":
            label = seq_obj.label
        else:
            label = f"Sequence_{i}"
        fasta_str += f">{label}\n{seq_obj.seq}\n\n"

    if file_name:
        with open(file=file_name, mode="w") as text_file:
            text_file.write(fasta_str)
    return fasta_str


def seq_from_fasta(file_path: str, seq_type=None):
    """
    Parse a fasta file
    Returns specified type of Seq object
    """
    import re
    from jinfo.sequence import BaseSeq, DNASeq, RNASeq, AASeq

    with open(file_path, "r") as text_file:
        fasta_str = text_file.read()

    label = re.findall(r"^>(.*)", fasta_str)[0]
    fasta_lines = fasta_str.split("\n")
    label_index = fasta_lines.index(">" + label)
    seq_string = "".join(fasta_lines[label_index + 1 :])
    if seq_type is None:
        return BaseSeq(sequence=seq_string, label=label)
    else:
        return seq_type(sequence=seq_string, label=label)


def seq_list_from_fasta(file_path: str, seq_type=None) -> list:
    """
    Parse a multifasta file
    Returns list of BaseSeq objects
    """
    from jinfo.sequence import BaseSeq
    import re

    with open(file_path, "r") as text_file:
        fasta_str = text_file.read()

    label_list = re.findall(r"^>(.*)", fasta_str, re.MULTILINE)
    fasta_lines = fasta_str.split("\n")
    seq_list = []

    for i in range(len(label_list)):
        label_index = fasta_lines.index(">" + label_list[i])
        if i == len(label_list) - 1:
            seq_string = "".join(fasta_lines[label_index + 1 :])
        else:
            next_label_index = fasta_lines.index(">" + label_list[i + 1])
            seq_string = "".join(fasta_lines[label_index + 1 : next_label_index])

        if seq_type is None:
            seq_list.append(BaseSeq(sequence=seq_string, label=label_list[i]))
        else:
            seq_list.append(seq_type(sequence=seq_string, label=label_list[i]))
    return seq_list


def alignment_from_fasta(file_path: str):
    """
    Parse alignment from fasta file
    Returns Alignment object
    """
    from jinfo.alignment import BaseAlignment

    seq_list = seq_list_from_fasta(file_path=file_path)
    return BaseAlignment(aligned_sequences=seq_list)


def multialign(seq_list: list, maxiters: int = 16):
    """
    Perform multiple sequence alignment, optionally control the number of iterations
    ***Requires MUSCLE package***
    Returns Alignment object
    """
    import subprocess
    from jinfo.utils import seq_list_to_fasta, alignment_from_fasta

    try:
        test_cmd = "muscle -quiet".split(" ")
        subprocess.run(test_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except FileNotFoundError:
        raise MuscleNotInstalledError

    in_path = "_temp.fasta"
    out_path = "_temp2.fasta"
    seq_list_to_fasta(seq_list=seq_list, file_name=in_path)
    bash_cmd = f"muscle -in {in_path} -out {out_path} -quiet -maxiters {maxiters}".split(
        sep=" "
    )
    subprocess.run(bash_cmd)

    alignment_obj = alignment_from_fasta(out_path)
    cleanup_cmd = f"rm {in_path} {out_path}".split(sep=" ")
    subprocess.run(cleanup_cmd)
    return alignment_obj


if __name__ == "__main__":
    pass
