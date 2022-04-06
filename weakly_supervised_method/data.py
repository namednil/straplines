import re
import json
import spacy

from tqdm import tqdm
import logging

logging.basicConfig(level=logging.INFO)

from copy import deepcopy


class NewsRoomArticle:
    def __init__(self, data):
        self.data = data

    def compute_additional_fields(self, spacy_model):
        self.data["summary_tokens"] = spacy_model(self.data["summary"])

        self.data["normalized_density"] = self.data["density"] / len(
            self.data["summary_tokens"]
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

    def dump(self):
        summary_tokens = self.data["summary_tokens"]
        self.data.pop("summary_tokens", None)
        json_str = json.dumps(self.data)
        self.data["summary_tokens"] = summary_tokens
        return json_str


class NewsRoomDataset:
    def __init__(self, data_file=None, summaries_dict=None, titles_dict=None):
        self.spacy_model = spacy.load("en_core_web_sm")

        if data_file:
            with open(data_file, "r") as f:
                article_jsons = [json.loads(l.strip()) for l in f]

            # Filter out articles having extractive summaries.
            self.articles = [
                NewsRoomArticle(article_json)
                for article_json in article_jsons
                if article_json["density_bin"] != "extractive"
            ]

            logging.info("Compute additional fields for each article")
            for article in tqdm(self.articles):
                article.compute_additional_fields(self.spacy_model)

        else:
            raise ValueError(
                "Please specify either a 'data_file' for a subset of NewsRoom."
            )

        if not summaries_dict:
            self.summaries_dict = {}
        else:
            # Load the summaries dict from another dict
            self.summaries_dict = summaries_dict

        if not titles_dict:
            self.titles_dict = {}
        else:
            # Load the titles dict from another dict
            self.titles_dict = titles_dict

        logging.info("Search for duplicated titles/summaries")
        for article in tqdm(self.articles):
            summary = article.data["summary"]
            title = article.data["title"]
            if summary not in self.summaries_dict:
                self.summaries_dict[summary] = 1
            else:
                self.summaries_dict[summary] += 1
            if title not in self.titles_dict:
                self.titles_dict[title] = 1
            else:
                self.titles_dict[title] += 1

        for article in tqdm(self.articles):
            article.data["summary_repetition_count"] = self.summaries_dict[
                article.data["summary"]
            ]
            article.data["title_repetition_count"] = self.titles_dict[
                article.data["title"]
            ]

    def filter_articles(self, drop_mask):
        """Filter out articles having drop_mask that isn't equal to one."""
        dataset = deepcopy(self)
        filtered_articles = [
            article for article, drop in zip(dataset.articles, drop_mask) if drop != 1
        ]
        dataset.articles = filtered_articles
        return dataset

    # TODO: Store/load the dataset to avoid repetitive computations
    def dump(self, filename):
        json_str = "\n".join([article.dump() for article in tqdm(self.articles)])
        with open(filename, "w") as f:
            f.write(json_str)

    def unpickle(self):
        pass
