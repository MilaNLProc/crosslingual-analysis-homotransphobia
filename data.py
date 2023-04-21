import os
import json
import argparse
import pandas as pd


def parse(language):
    """
    Parse the data from a JSONL file for a given language and convert it into a CSV file.

    Args:
        language (str): Language for which the data needs to be parsed.

    Returns:
        None

    Raises:
        FileNotFoundError: If the data file for the given language is not found.

    """
    file_path = f"data/{language}.jsonl"
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"Missing data file: {file_path}")
    
    dataset = dict(
        id=list(),
        tweet=list()
    )
    raw_tweets_file = open(file_path, "r")
    json_data = [json.loads(line) for line in raw_tweets_file]
    for data in json_data:
        data = data["data"]
        for datapoint in data:
            dataset["id"] += [datapoint["id"]]
            dataset["tweet"] += [datapoint["text"]]
    csv_file = f"data/{language}.csv"
    pd.DataFrame.from_dict(dataset).to_csv(csv_file, index=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-l", "--language",
        type=str,
        default="IT",
        choices=["IT", "EN", "DE", "FR", "ES", "PT", "NO"],
        help="The language of the experiment"
    )
    args = parser.parse_args()
    parse(args.language)
