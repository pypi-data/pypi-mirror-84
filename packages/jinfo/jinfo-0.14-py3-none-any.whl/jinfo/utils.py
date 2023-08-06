class MuscleNotInstalledError(Exception):
    pass


class FastTree2NotInstalledError(Exception):
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

    Returns jinfo.DNASeq object
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


def percentage_identity(seq1, seq2, dp: int = 2) -> float:
    """
    Calculate pairwise sequence similarity from aligned sequences

    Optionally control precision using dp argument
    Returns: float
    """
    i = 0
    for b1, b2 in zip(seq1.seq, seq2.seq):
        if b1 == b2:
            i += 1
    pid = i * 100 / ((seq1.len + seq2.len) / 2)
    return pid


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
    bash_cmd = (
        f"muscle -in {in_path} -out {out_path} -quiet -maxiters {maxiters}".split(
            sep=" "
        )
    )
    subprocess.run(bash_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    alignment_obj = alignment_from_fasta(out_path)
    cleanup_cmd = f"rm {in_path} {out_path}".split(sep=" ")
    subprocess.run(cleanup_cmd)
    return alignment_obj


def calc_phylo_tree(alignment_obj):
    """
    Calculate a Newick format phylogenetic tree from an alignment object

    ***Requires FastTree2 package***
    Returns: Tree object
    """

    import subprocess
    from jinfo.utils import seq_list_to_fasta
    from jinfo.phylogenetics import PhyloTree

    try:
        test_cmd = "FastTreeMP".split(" ")
        subprocess.run(test_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except FileNotFoundError:
        raise FastTree2NotInstalledError

    in_path = "temp.fasta"
    out_path = "temp.tree"
    seq_list_to_fasta(seq_list=alignment_obj.seqs, file_name=in_path)

    bash_cmd = f"FastTreeMP {in_path}".split(sep=" ")
    with open(out_path, "w") as text_file:
        subprocess.run(bash_cmd, stdout=text_file)

    with open(out_path, "r") as text_file:
        tree_obj = PhyloTree(text_file.read())

    cleanup_cmd = f"rm {in_path} {out_path}".split(sep=" ")
    subprocess.run(cleanup_cmd)
    return tree_obj


def remove_degenerate_seqs(alignment_obj, identity_limit: int):
    """
    Filter high similarity sequences from a list of Seq objects

    Returns: BaseAlignment
    """
    import multiprocessing as mp
    from functools import partial
    from jinfo.alignment import BaseAlignment

    seq_list = alignment_obj.seqs
    identity_array = []
    filtered_seqs = []
    pool = mp.Pool(mp.cpu_count())  # Set up cpu pool for parallel calculation

    for seq_obj in seq_list:
        id_partial = partial(percentage_identity, seq2=seq_obj)
        identity_array_row = pool.map(id_partial, seq_list)
        identity_array.append(identity_array_row)

    for i, row in enumerate(identity_array):
        row.remove(100)  # remove seq 100% match with itself
        if max(row) < float(identity_limit):
            filtered_seqs.append(seq_list[i])

    return BaseAlignment(filtered_seqs)


if __name__ == "__main__":
    pass
