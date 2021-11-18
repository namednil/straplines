import re
import json
import spacy

from tqdm import tqdm
import logging

logging.basicConfig(level=logging.INFO)


class NewsRoomArticle:
    def __init__(self, data):
        self.data = data

    def compute_additional_fields(self, spacy_model):
        self.data["summary_tokens"] = spacy_model(self.data["summary"])

        self.data["normalized_density"] = self.data["density"] / len(
            self.data["summary_tokens"]
        )

        # Generate preprocessed fields
        # TODO: Make this more generic
        self.data["preprocessed_summary"] = re.sub(
            r" - USATODAY.com$", "", self.data["summary"]
        )

        # TODO: Optimize those thersholds
        th1, th2 = (0.07958477508823529, 0.2988165680461538)
        cov_th = 0.85

        # Don't also consider high coverage summaries as abstractive ones
        self.data["normalized_density_bin"] = (
            "abstractive"
            if self.data["normalized_density"] <= th1
            and self.data["coverage"] <= cov_th
            else "mixed"
            if self.data["normalized_density"] <= th2
            else "extractive"
        )


class NewsRoomDataset:
    def __init__(self, data_file=None, articles=None, summaries_dict=None):
        self.spacy_model = spacy.load("en_core_web_sm")

        if data_file:
            with open(data_file, "r") as f:
                article_jsons = [json.loads(l.strip()) for l in f]

            self.articles = [
                NewsRoomArticle(article_json) for article_json in article_jsons
                if article_json["density_bin"] != "extractive"
            ]

            logging.info("Compute additional fields for each article")
            for article in tqdm(self.articles):
                article.compute_additional_fields(self.spacy_model)

        elif articles:
            self.articles = articles

        else:
            raise ValueError(
                "Please specify either a 'data_file' or a list of 'articles'"
            )

        if not summaries_dict:
            self.summaries_dict = {}
        else:
            self.summaries_dict = summaries_dict

        logging.info("Search for duplicated summaries")
        for article in tqdm(self.articles):
            summary = article.data["summary"]
            if summary not in self.summaries_dict:
                self.summaries_dict[summary] = 1
            else:
                self.summaries_dict[summary] += 1

        for article in tqdm(self.articles):
            article.data["summary_repetition_count"] = self.summaries_dict[
                article.data["summary"]
            ]

    def generate_a_cleaned_dataset(self, predictions):
        articles = [
            article for article, pred in zip(self.articles, predictions) if pred != 1
        ]
        return NewsRoomDataset(articles=articles)
