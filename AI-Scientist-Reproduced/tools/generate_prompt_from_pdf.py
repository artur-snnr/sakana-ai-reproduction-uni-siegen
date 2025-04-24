"""
============================================================
Filename: generate_prompt_from_pdf.py
Author: Moritz Baumgart
Affiliation: University of Siegen, Intelligent Systems Group (ISG)
Date: December, 2024
============================================================

Description:
This script extracts text from given pdf and generates a prompt that asks AI-S to reproduce that paper.

In and output file and other options can be specified as CLI parameters, call the script with flag `-h` for more information.
============================================================
"""

from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from pathlib import Path

from pypdf import PdfReader


def main():

    argparse = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
    argparse.add_argument("in_file", help="Input pdf file to extract text from.")
    argparse.add_argument(
        "out_file",
        help="Output txt file to write text to.",
        nargs="?",
        default="text_extract.txt",
    )
    argparse.add_argument(
        "-f",
        "--force",
        action="store_true",
        help="Force overwrite if output file already exists.",
    )

    args = argparse.parse_args()

    in_pth = Path(args.in_file)
    if not in_pth.exists():
        print(f"Error: Input file {in_pth} does not exists.")
        return

    out_pth = Path(args.out_file)
    if out_pth.exists() and not args.f:
        print(
            f"Error: Output file {out_pth} does already exists. Use -f to force overwrite!"
        )
        return
    else:
        out_pth.parent.mkdir(exist_ok=True, parents=True)

    reader = PdfReader(in_pth)

    txt_out = ""
    for page in reader.pages:
        txt_out += page.extract_text()

    txt_out = txt_out.replace("\n", " ")

    prompt = "Below is the full text of the paper with given title. Your goal is to change the code so it reproduces the idea. There are three levels of reproducibility that you might be able to check for: 1) Replicate everything 1:1 and just check if the obtained results are the same as in the paper; 2) Do just a slight variation, e.g. a different random seed, different datasets, etc. to verify that the results are not cherry picked; 3) Do larger variation, e.g. changes in the algorithm itself. Here comes the original paper:\\n"

    final_out = prompt + txt_out

    with open(out_pth, "w") as out_f:
        out_f.write(final_out)


if __name__ == "__main__":
    main()
