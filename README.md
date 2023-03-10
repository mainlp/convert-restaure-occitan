# Converting RESTAURE Occitan to UPOS

This script converts the [Annotated Corpus for Occitan](https://zenodo.org/record/1182949) (Bras ea 2018; [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/legalcode)) to UPOS by splitting contractions.
It was used for the paper *TBD*.


## Usage

```
# Get the data
wget https://zenodo.org/record/1182949/files/CorpusRestaureOccitan.zip
unzip CorpusRestaureOccitan.zip
rm CorpusRestaureOccitan.zip
rm -r __MACOSX

python3 convert.py --glob "CorpusRestaureOccitan/*" --out "test_ROci_UPOS.tsv"
```

## Details

The original corpus is available in a slightly modified version of UPOS as well as a custom tagset ([Bernhard ea 2018](https://hal.science/hal-01704806v1/document)).
We're only concerned with the former.
While the corpus annotation also mentions the non-UPOS tags `EPE` and `MOD`, these are not actually in the RESTAURE Occitan corpus.
Thus, the only tag we're concerned with is `ADP+DET`.
Analogously to the other Romance UD treebanks, we split the relevant word forms into one `ADP` token and one `DET` token (e.g. `dau ADP+DET` -> `de ADP` + `lo DET`).
The `convert.py` file contains the full mapping of contractions to split lemmas.
