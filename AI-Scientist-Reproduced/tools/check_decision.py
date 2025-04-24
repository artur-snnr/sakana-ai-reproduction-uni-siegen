"""
============================================================
Filename: check_decision.py
Author: Moritz Baumgart
Affiliation: University of Siegen, Intelligent Systems Group (ISG)
Date: December, 2024
============================================================

Description:
This script checks if the decision the ai reviewer made matches the actual decision from openreview and prints an overview for that.

You can specify the location of the reviews and the papers.csv below.
============================================================
"""

import json
import logging
from pathlib import Path

import pandas as pd
from colorama import Fore, Back, just_fix_windows_console


PAPERS_DIR = Path("../data/AI-Scientist/ai_reviewer")


def main():

    just_fix_windows_console()
    logger = logging.getLogger()
    logging.basicConfig(level=logging.INFO)

    paper_df = pd.read_csv(PAPERS_DIR / "papers.csv")

    actual_reject_count = 0
    ai_s_reject_count = 0
    total_papers = 0
    max_line_len = 0

    for _, current_paper in paper_df.iterrows():
        current_paper_id = current_paper["openreview_id"]
        review_pth = PAPERS_DIR / f"{current_paper_id}/review.txt"

        if not review_pth.exists():
            logger.warning(f"No review.txt found for {current_paper_id}")
            continue

        actual_decision = current_paper["status"]

        if actual_decision == "reject":
            actual_reject_count += 1
            actual_color = Fore.RED
        else:
            actual_color = Fore.GREEN

        with open(review_pth, "r") as f:
            review = json.load(f)
            ai_s_decision = str(review["Decision"]).lower()

            if ai_s_decision == "reject":
                ai_s_reject_count += 1
                ai_s_color = Fore.RED
            else:
                ai_s_color = Fore.GREEN

            decision_match = ai_s_decision == actual_decision
            if decision_match:
                match_color = Back.GREEN
            else:
                match_color = Back.RED

            line = f"{Fore.YELLOW}{current_paper_id}{Fore.RESET}: AI-S: {ai_s_color}{ai_s_decision}{Fore.RESET}, Actual: {actual_color}{actual_decision}{Fore.RESET}, Match? {match_color}{decision_match}{Back.RESET}"
            if len(line) > max_line_len:
                max_line_len = len(line)
            print(line)

        total_papers += 1

    print("═" * max_line_len)

    print(
        f"Total: AI-S: {ai_s_reject_count}/{total_papers} rejected, Actual: {actual_reject_count}/{total_papers}."
    )


if __name__ == "__main__":
    main()
