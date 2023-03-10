"""
Converts annotated corpus files with the format:
TOKEN	TAG
(tab-separated).
Sentence boundaries are indicated by empty lines.
"""

from argparse import ArgumentParser
from glob import glob


occitan_contractions = {"al": ("a", "lo"), "als": ("a", "los"),
                        "au": ("a", "lo"), "aus": ("a", "los"),
                        "ai": ("a", "lei"), "ais": ("a", "lei"),
                        "ath": ("a", "eth"), "ara": ("a", "era"),
                        "del": ("de", "lo"), "dels": ("de", "los"),
                        "dei": ("de", "lei"), "des": ("de", "les"),
                        "dau": ("de", "lo"), "daus": ("de", "los"),
                        "deu": ("de", "lo"), "deus": ("de", "los"),
                        "deth": ("de", "eth"),
                        "dera": ("de", "era"), "deras": ("de", "eras"),
                        "pel": ("per", "lo"), "pels": ("per", "los"),
                        "peu": ("per", "lo"), "peus": ("per", "los"),
                        "peth": ("per", "eth"), "pera": ("per", "era"),
                        "sul": ("sus", "lo"), "suls": ("sus", "los"),
                        "suu": ("sus", "lo"), "suus": ("sus", "los"),
                        "tau": ("tà", "lo"), "taus": ("tà", "los"),
                        "tath": ("tà", "eth"),
                        "entau": ("entà", "lo"), "entaus": ("entà", "los"),
                        }


def ud(input_files, out_file, verbose=True):
    pos_idx = 3
    sents_added = 0
    sents_skipped = 0
    with open(out_file, 'w+', encoding="utf8") as f_out:
        for in_file in input_files:
            if verbose:
                print("Reading " + in_file)
            with open(in_file, encoding="utf8") as f_in:
                filename = None
                first_sent = True
                sent = []
                skip_sent = False
                for line in f_in:
                    line = line.strip()
                    if not line:
                        if sent:
                            if not skip_sent:
                                sents_added += 1
                                for form, pos, filename in sent:
                                    if filename:
                                        f_out.write(
                                            f"{form}\t{pos}\t{filename}\n")
                                    else:
                                        f_out.write(f"{form}\t{pos}\n")
                            else:
                                sents_skipped += 1
                                print("Missing POS tag (skipping sent.)")
                                print(" ".join((x[0] for x in sent)))
                            sent = []
                        if not first_sent:
                            f_out.write("\n")
                        continue
                    if line[0] == "#":
                        continue
                    first_sent = False
                    cells = line.split("\t")
                    try:
                        form = cells[1].strip()
                        pos = cells[pos_idx]
                        if "+" in pos:
                            print("Splitting " + pos + " and " + form)
                            try:
                                lemmas = occitan_contractions[form.lower()]
                                for i, (subpos, lemma) in enumerate(
                                        zip(pos.split("+"), lemmas)):
                                    if i == 0 and form[0] == form[0].upper():
                                        lemma = lemma[0].upper() + lemma[1:]
                                    sent.append((lemma, subpos, filename))
                            except IndexError:
                                print("Unknown lemma: " + form)
                                print("Skipping sentence!")
                                skip_sent = True
                        else:
                            if not pos:
                                print("POS tag missing for " + form)
                                print("Skipping sentence!")
                                skip_sent = True
                            if pos == "_":
                                continue
                            if not form:
                                print("Form missing:")
                                print(line)
                                continue
                            sent.append((form, pos, filename))
                    except IndexError:
                        print("!!! malformed line:")
                        print(line)
                        print(in_file)
                        print("(exiting)")
                        return
    print(f"Added {sents_added} sentences.")
    print(f"Skipped {sents_skipped} sentences.")


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--dir", default="",
                        help="data directory root")
    parser.add_argument("--files", default="",
                        help="input file(s) within the data directory, "
                        "comma-separated")
    parser.add_argument("--glob", default="",
                        help="glob pattern (ignores --dir and --files)")
    parser.add_argument("--out", help="output file")
    args = parser.parse_args()
    if args.glob:
        input_files = glob(args.glob)
    else:
        input_files = [args.dir + "/" + f.strip()
                       for f in args.files.split(",")]
    ud(input_files, args.out)
