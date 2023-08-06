from jinfo.tables import DNA_VOCAB, AA_VOCAB


class BaseAlignment:
    """
    Iterator which holds sequence alignments and the respective sequence labels
    """

    def __init__(self, aligned_sequences: list, labels: list = None, vocab: set = None):
        self.seqs = aligned_sequences
        self.seqs_str = [seq_obj.seq for seq_obj in self.seqs]
        self.vocab = vocab

        if labels:
            self.labels = labels
        else:
            self.labels = [seq.label for seq in aligned_sequences]
        return

    def __iter__(self):
        self.index = 0
        return self

    def __next__(self):
        if self.index < len(self.seqs):
            next_seq = self.seqs[self.index]
            self.index += 1
            return next_seq
        else:
            raise StopIteration

    def __str__(self):
        import textwrap

        seq_str_rows = [
            textwrap.fill(seq_obj.seq, width=80).split("\n") for seq_obj in self.seqs
        ]
        str_out = ""
        for i in range(len(seq_str_rows)):
            str_out += f"{self.labels[i]}:\n"
            for j in range(len(seq_str_rows[i])):
                str_out += f"{seq_str_rows[i][j]}\n"

            str_out += "\n"

        return str_out

    def calc_tree(self):
        """
        Calculate a phylogenetic tree from the alignment
        ***Requires FastTree2 package***
        Returns: Tree object
        """
        from jinfo.utils import calc_phylo_tree

        return calc_phylo_tree(self)

    pass
