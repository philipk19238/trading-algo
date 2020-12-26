import json
import pandas as pd
from collections import defaultdict
import os


class LabelService:
    
    @staticmethod
    def get_starting():
        start_idx = input("Enter starting index or blank for auto: ")
        if not start_idx:
            return len(pd.read_csv("daily_data_labeled.csv"))
        return int(start_idx)

    @staticmethod
    def load_json_index(generator, start_idx, curr_idx=0):
        while generator and curr_idx < start_idx:
            generator.readline()
            curr_idx += 1
        return generator


if __name__ == "__main__":
    start_idx = LabelService.get_starting()
    labeled = defaultdict(list)
    label_dict = {"y": "Bull", "n": "Bear"}
    with open("temp.json", "r") as f:
        f = LabelService.load_json_index(f, start_idx)
        curr = json.loads(f.readline())
        cont = True
        while curr and cont:
            body = curr.get("body")
            label = input(
                f"Enter 'y' for Bull, 'n' for Bear, and blank for Neutral\n\n{'*'* 20}\n{body}\n{'*'* 20}\n\n"
            )
            if label and label.lower() not in ["y", "n"]:
                print("Invalid Label")
                label = input(
                    f"Enter 'y' for Bull, 'n' for Bear, and blank for Neutral\n\n{'*'* 20}\n{body}\n{'*'* 20}\n\n"
                )
            label = "Neutral" if not label else label_dict.get(label)
            labeled["body"].append(body)
            labeled["label"].append(label)
            curr = json.loads(f.readline())
            cont = input("Continue? Press any character or blank to end.\n")
    df = pd.DataFrame(labeled)
    if "daily_data_labeled.csv" in os.listdir(os.getcwd()):
        prev = pd.read_csv("daily_data_labeled.csv")
        prev.drop(["Unnamed: 0"], axis=1, inplace=True)
        df = pd.concat([prev, df], ignore_index=True, sort=False)
    df.to_csv("daily_data_labeled.csv")
