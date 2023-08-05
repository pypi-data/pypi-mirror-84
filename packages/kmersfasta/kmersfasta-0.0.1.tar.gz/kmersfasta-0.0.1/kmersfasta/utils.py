from collections import Counter
from itertools import product
from Bio import Entrez
def kmers_from_file(file):
    b = True
    while b:
        try:
            with open(file) as f:
                f.readline()
                ly = []
                for i in f.readlines():
                    ly.append(i)
            b = False
        except:
            print('Enter the correct filename: ')
    fasta_string = ''.join([i.strip() for i in ly])
    k = int(input('Enter the value of k: '))
    counts = Counter(fasta_string[i:i+k] for i in range(0,len(fasta_string)) if len(fasta_string[i:i+k])==k)
    for k_mer in (''.join(t) for t in product('ACGT', repeat=k)):
        print(f"count of {k_mer} is {counts[k_mer]}")

def kmers_from_ncbi(email):
    Entrez.email = email
    file = input('Enter the ncbi accession number: ')
    k = int(input('Enter the value of k: '))
    handle = Entrez.efetch(db = 'nucleotide', id = file,rettype="fasta", retmode="text")
    record = handle.read()
    fasta_string = ''.join(record.split('\n')[1:])
    counts = Counter(''.join(t) for t in zip(*[iter(fasta_string)]*k))
    for k_mer in (''.join(t) for t in product('ACGT', repeat=k)):
        print(f"count of {k_mer} is {counts[k_mer]}")
