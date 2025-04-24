"""
============================================================
Filename: extract_cost.py
Author: Moritz Baumgart
Affiliation: University of Siegen, Intelligent Systems Group (ISG)
Date: December, 2024
============================================================

Description:
This script extracts API usage cost from the aider logs and saves it as cost.csv and cost.xlsx in CWD.

CAREFUL: Output files WILL be overwritten if they already exist.

You can specify the path to the results of the experiment to extract the costs from below. 
============================================================
"""

from datetime import datetime
from glob import glob
from pathlib import Path
import re

import pandas as pd

# Put results dir here
RESULTS_DIR = Path("../data/AI-Scientist/results/knn")


def main():

    COST_REGEX = re.compile(
        r"> Tokens: (.+) sent, (.+) received\. Cost: \$(.+) message, \$(.+) session\."
    )

    df_dict = {
        "date": [],
        "time": [],
        "idea_name": [],
        "sent": [],
        "recv": [],
        "cost": [],
        "session_cost": [],
    }

    for res_dir in RESULTS_DIR.iterdir():
        for aider_file_name in glob("*aider.txt", root_dir=res_dir):
            print(f"\nWorking on file: {aider_file_name}")

            s = aider_file_name.split("_")
            date = datetime.strptime(s[0], "%Y%m%d")
            time = datetime.strptime(s[1], "%H%M%S")
            idea_name = "_".join(s[2:]).replace("_aider.txt", "")

            print(date, idea_name)

            sent_tokens_cum = 0
            recv_tokens_cum = 0
            cost_cum = 0
            session_cost = 0
            with open(res_dir / aider_file_name, "r", encoding="utf8") as aider_file:
                for line in aider_file.read().splitlines():
                    m = COST_REGEX.match(line)
                    if m:
                        sent_tokens_cum += int(m.group(1).replace(",", ""))
                        recv_tokens_cum += int(m.group(2).replace(",", ""))
                        cost_cum += float(m.group(3))
                        session_cost = round(float(m.group(4)), 2)

                cost_cum = round(cost_cum, 2)

                print(
                    f"Sent total: {sent_tokens_cum}, Recv total: {recv_tokens_cum}, Cost total: {cost_cum}, Session cost: {session_cost}"
                )

                df_dict["date"].append(date)
                df_dict["time"].append(time)
                df_dict["idea_name"].append(idea_name)
                df_dict["sent"].append(sent_tokens_cum)
                df_dict["recv"].append(recv_tokens_cum)
                df_dict["cost"].append(cost_cum)
                df_dict["session_cost"].append(session_cost)

    df = pd.DataFrame(df_dict)
    df.to_excel("cost.xlsx", index=False)
    df.to_csv("cost.csv", index=False)


if __name__ == "__main__":
    main()
