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
        return "\n".join([f"{seq_obj.label}\t{seq_obj.seq}" for seq_obj in self.seqs])

    pass
