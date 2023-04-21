import os
import tweetnlp
import argparse
import pandas as pd


from tqdm import tqdm


def preprocess(text):
    """
    Preprocess the given text by replacing mentions and URLs with placeholders.

    Args:
        text (str): The text to be preprocessed.

    Returns:
        str: The preprocessed text.

    """
    new_text = []
    for t in text.split(" "):
        t = '@user' if t.startswith('@') and len(t) > 1 else t
        t = 'http' if t.startswith('http') else t
        new_text.append(t)
    return " ".join(new_text)


def analyze(language):
    """
    Analyze the sentiment of the tweets in a given language using a pre-trained multilingual sentiment analysis model.

    Args:
        language (str): The language of the tweets to be analyzed.

    Returns:
        None

    Raises:
        FileNotFoundError: If the data file for the given language is not found.

    """
    file_path = f"data/{language}.csv"
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"Missing data file: {file_path}")
    if not os.path.exists("results/"):
        os.mkdir("results")
        
    data = pd.read_csv(file_path)

    model_name = "cardiffnlp/twitter-xlm-roberta-base-sentiment-multilingual"
    model = tweetnlp.Classifier(model_name, max_length=128)

    predictions = []
    # We analyze in chunks of 1000 tweets
    for start in tqdm(range(0, len(data), 1000)):
        if start + 1000 > len(data):
            tweets = data[start:].tweet
        else:
            tweets = data[start:start+1000].tweet
        tweets = [preprocess(tweet) for tweet in tweets]
        preds = model.predict(tweets)
        predictions += [pred["label"] for pred in preds]
    
    data["sentiment"] = predictions
    data.to_csv(f"results/{language}_sentiment.csv")


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
    analyze(args.language)
