"""
============================================================
Filename: code_metrics.py
Author: Moritz Baumgart
Affiliation: University of Siegen, Intelligent Systems Group (ISG)
Date: February, 2025
============================================================

Description:
This script calculates multiple metrics to compare how many changes the ai scientist did to the original experiment.py files.

You can specify the location of the results and the templates below.
============================================================
"""

from pathlib import Path
import subprocess
from typing import Any

import pandas as pd


# Put results dir and template dir here
RESULTS_DIR = Path("../data/AI-Scientist/results")
TEMPLATES_DIR = Path("../data/AI-Scientist/templates")

RUN_NUM = 5


def main():

    metrics = (
        "LOC",
        "LOC vs. run_0",
        "#Code chars",
        "#Code chars vs. run_0",
        "insertions to run_0",
        "deletions from run_0",
    )
    data_columns = ("template", "idea", "run")
    data_columns += metrics
    data = {col: [] for col in data_columns}

    def push_data(values: list[Any]):
        assert len(data_columns) == len(
            values
        ), f"Value length mismatch on data push: {len(data_columns)=}, {len(values)=}"

        for col, val in zip(data_columns, values):
            data[col].append(val)

    for template_dir in RESULTS_DIR.iterdir():
        for idea_dir in template_dir.iterdir():

            run_0_file = TEMPLATES_DIR / template_dir.stem / "experiment.py"
            assert (
                run_0_file.exists()
            ), f"Could not find template file at {run_0_file}. Make sure the template folder is set right."

            run_0_loc, run_0_chars = count_loc_and_chars(run_0_file)
            push_data(
                [
                    template_dir.stem,
                    idea_dir.stem,
                    0,
                    run_0_loc,
                    0,
                    run_0_chars,
                    0,
                    0,
                    0,
                ]
            )

            for run_nr in range(1, RUN_NUM + 1):
                run_file = idea_dir / f"run_{run_nr}.py"
                if run_file.exists():
                    loc, chars = count_loc_and_chars(run_file)

                    insertions, deletions = git_diff_stat(run_0_file, run_file)

                    push_data(
                        [
                            template_dir.stem,
                            idea_dir.stem,
                            run_nr,
                            loc,
                            loc - run_0_loc,
                            chars,
                            chars - run_0_chars,
                            insertions,
                            deletions,
                        ]
                    )

    df = pd.DataFrame(data)
    df = df.pivot(index=["template", "idea"], columns=["run"], values=list(metrics))
    df.to_excel("metrics.xlsx")


def git_diff_stat(file1: Path, file2: Path):
    proc = subprocess.run(
        ["git", "diff", "--no-index", "--numstat", file1, file2],
        capture_output=True,
        text=True,
    )

    s = proc.stdout.split("\t")
    insertions = int(s[0])
    deletions = int(s[1])
    return insertions, deletions


def count_loc_and_chars(experiment_file: Path):
    with open(experiment_file, "r") as f:
        lines = f.readlines()

    loc = 0
    chars = 0
    in_block_comment = False

    for line in lines:
        stripped = line.strip()

        # Ignore empty lines
        if not stripped:
            continue

        # Ignore block comments
        if stripped.startswith('"""') or stripped.startswith("'''"):
            in_block_comment = not in_block_comment
            continue

        if in_block_comment:
            continue

        # Ignore single line comments
        if stripped.startswith("#"):
            continue

        loc += 1
        chars += len(stripped)

    return loc, chars


if __name__ == "__main__":
    main()
