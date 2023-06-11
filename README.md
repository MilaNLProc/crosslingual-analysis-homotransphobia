# A Cross-Lingual Study of Homotransphobia on Twitter

[Davide Locatelli](http://davidelct.com) · [Greta Damo](https://milanlproc.github.io/authors/greta_damo/) · [Debora Nozza](https://deboranozza.com/)

This repository contains data and code used in the paper [A Crosslingual Analysis of Homotransphobia on Twitter](https://aclanthology.org/2023.c3nlp-1.3/).

## Data

In accordance with Twitter's policy, we have provided the tweet IDs for analysis. There are seven files, each containing tweet IDs for tweets in one of the seven languages: English, Italian, German, French, Spanish, Portuguese, and Norwegian.

## Code 

The code consists of three files:
- `data.py` - to process the data
- `topics.py` - to run the contextualized topic modeling analysis
- `sentiment.py` - to run the sentiment analysis

## Instructions

To reproduce our study:
1. Retrieve the tweets. To do this, you will need Twitter API keys. Once you have those, you can use the [twarc library](https://twarc-project.readthedocs.io/en/latest/) as follows:
```
twarc hydrate data/LANG.txt > LANG.jsonl
```
2. Preprocess the data:
```
python data.py -l LANG
```
3. Run topic modeling analysis:
```
python topics.py -l LANG
```
4. Run sentiment analysis:
```
python sentiment.py -l LANG
```
Where LANG is an [ISO 639-1 language code](https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes). For example, for Norwegian it's `NO`.

## Pre-trained models

The following pre-trained models are used for the analysis:
- CTM: [distiluse-base-multilingual-cased-v1](https://huggingface.co/sentence-transformers/distiluse-base-multilingual-cased-v1), [distiluse-base-multilingual-cased-v2](https://huggingface.co/sentence-transformers/distiluse-base-multilingual-cased-v2)
- Sentiment analysis: [twitter-xlm-roberta-base-sentiment](https://huggingface.co/cardiffnlp/twitter-xlm-roberta-base-sentiment)

## Results

The results of the analysis will be stored in the `results` folder. There will be three files per language: 
- `LANG_topics.txt` - contains the results of the topic modeling analysis with the top words for 5, 10, 15, 20 topics
- `LANG_topics.csv` - contains the results of the topic modeling analysis with each tweet assigned to a topic
- `LANG_sentiment.csv` - contains the results of the sentiment analysis with each tweet assigned to a sentiment class


## Reference

If you use the data or code please cite the following paper:

    @inproceedings{locatelli-etal-2023-cross,
    title = "A Cross-Lingual Study of Homotransphobia on {T}witter",
    author = "Locatelli, Davide  and
      Damo, Greta  and
      Nozza, Debora",
    booktitle = "Proceedings of the First Workshop on Cross-Cultural Considerations in NLP (C3NLP)",
    month = may,
    year = "2023",
    address = "Dubrovnik, Croatia",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2023.c3nlp-1.3",
    pages = "16--24",
    abstract = "We present a cross-lingual study of homotransphobia on Twitter, examining the prevalence and forms of homotransphobic content in tweets related to LGBT issues in seven languages. Our findings reveal that homotransphobia is a global problem that takes on distinct cultural expressions, influenced by factors such as misinformation, cultural prejudices, and religious beliefs. To aid the detection of hate speech, we also devise a taxonomy that classifies public discourse around LGBT issues. By contributing to the growing body of research on online hate speech, our study provides valuable insights for creating effective strategies to combat homotransphobia on social media.",

