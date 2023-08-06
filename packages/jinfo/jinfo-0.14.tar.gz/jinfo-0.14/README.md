# jinfo v0.13
Extensible bio/informatics library for hackers
https://pypi.org/project/jinfo/

### Objects:
- Sequences: BaseSeq, DNASeq, RNASeq, AASeq
- Alignments: BaseAlign
- Phylogenetic Trees: PhyloTree
- Small molecules: Metabolite

### Functions:
- one_hot_dna
- random_dna
- DNASeq_from_NCBI
- seq_list_to_fasta
- seq_from_fasta
- seq_list_from_fasta
- alignment_from_fasta
- multialign
- calc_phylo_tree
- percentage_identity
- remove_degenerate_seqs

### Admin TODO:
- Pypi description
- documentation

### Features TODO:
- DNASeq.find_CDS()
- DNASeq_from_NCBI()
- bring one_hot_dna and random_dna in line with rest of package
- metabolite methods
- Tests coverage
- NCBI, ChEBI, BiGG databast interfaces
- AASeq methods
- hmmer bindings
- tree methods
