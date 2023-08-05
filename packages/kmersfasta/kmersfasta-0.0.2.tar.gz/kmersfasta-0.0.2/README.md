### Counting K-mers from the sequence in fasta format  
<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/8/8a/K-mer_diagram.svg/640px-K-mer_diagram.svg.png?1603804064236" alt="alt text" width="200">


Usage: 
```
import kmers
kmers.kmers_from_file('filename.fasta')
```

where, *filename.fasta* is the name of the file in fasta format  

### Counting K-mers from the sequence obtained from NCBI using accession number
Usage:  

```
import kmers
kmers.kmers_from_ncbi('email')
```

where, *email* is your email address and you also need to provide the NCBI ACCESSION number during the prompt
