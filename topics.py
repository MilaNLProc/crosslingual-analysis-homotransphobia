import os
import re
import argparse
import pandas as pd

from contextualized_topic_models.evaluation.measures import *
from contextualized_topic_models.models.ctm import CombinedTM
from contextualized_topic_models.utils.data_preparation import TopicModelDataPreparation


def clean(data, language):
    """
    Preprocesses the given data by removing stopwords and other unwanted characters
    from the tweets.

    Args:
    - data (pandas.DataFrame): A dataframe containing the tweets to be preprocessed.
    - language (str): The language of the tweets in the data.

    Returns:
    - pandas.DataFrame: A dataframe containing the preprocessed tweets.
    """
    stopwords = [
        stopword.strip() 
        for stopword in open(f"data/stopwords/{language}.txt").readlines()
    ]
    data["preprocessed_text"] = data.tweet.str.lower().str.strip().progress_apply(
        lambda x: re.sub("@[A-Za-z0-9_]+", "", x)  # removing mentions
    ).apply(
        lambda x: re.sub("#[A-Za-z0-9_]+", "", x)  # removing hashtags
    ).apply(
        lambda x: re.sub(r"http\S+", "", x)  # removing http urls
    ).apply(
        lambda x: re.sub(r"www.\S+", "", x)  # removing www urls
    ).apply(
        lambda x: re.sub("[^a-z]", " ", x)  # removing non-letter characters
    ).str.strip().str.split().apply(
        lambda x: " ".join([word for word in x if word not in stopwords])
    )
    ids = data.loc[data["preprocessed_text"].astype(str).str.strip().ne(""), "id"]
    return data.loc[data["id"].isin(ids)]


def analyze(language):
    """
    Perform topic modeling on a CSV file of preprocessed text.

    Args:
        language (str): The language of the text data.

    Raises:
        FileNotFoundError: If the specified data file doesn't exist.

    Returns:
        None
    """
    file_path = f"data/{language}.csv"
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"Missing data file: {file_path}")
    if not os.path.exists("results/"):
        os.mkdir("results")

    data = pd.read_csv(file_path)
    data = clean(data, language)

    if args.language == "NO":
        model_version = "-v2"
    else:
        model_version = "-v1"
    ct_model = "distiluse-base-multilingual-cased" + model_version

    tp = TopicModelDataPreparation(ct_model)
    tweets = data.tweet.tolist()
    preprocessed_tweets = data.preprocessed_text.tolist()
    training_dataset = tp.fit(
        text_for_contextual=tweets, 
        text_for_bow=preprocessed_tweets
    )

    npmi = list()
    for no_topics in [5, 10, 15, 20]:
        no_epochs = 10
        ctm = CombinedTM(
            bow_size=len(tp.vocab), 
            contextual_size=512, 
            n_components=no_topics, 
            num_epochs=no_epochs
        )
        ctm.fit(training_dataset)

        topics = ctm.get_topic_lists(10)
        descriptors = []
        for i in range(len(topics)):
            if no_topics == 10:
                output_file = f"results/{language}_topics.txt"
                output_file.write(f"{i} {topics[i]}")
            descriptors.append(", ".join(topics[i][:3]))

        npmi_score = CoherenceNPMI(
            texts=[t.split() for t in preprocessed_tweets], topics=topics)
        npmi.append(npmi_score.score(topk=10))

        if no_topics == 10:
            topic_predictions = ctm.get_thetas(training_dataset)
            topic_scores = [
                descriptors[np.argmax(prediction)] 
                for prediction in topic_predictions
            ]
            topic_distros = pd.DataFrame.from_dict(
                {"id": data["id"], "tweet": data["tweet"], "topic": topic_scores})
            scores_filename = f"results/{language}_topics.csv"
            topic_distros.to_csv(scores_filename, index=False)


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
