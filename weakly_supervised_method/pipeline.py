from weakly_supervised_method.data import NewsRoomDataset
from weakly_supervised_method.heuristics import lf_too_short, lf_is_a_date, lf_has_HTML
from weakly_supervised_method.heuristics import (
    lf_mostly_quotes,
    lf_strange_ending,
    lf_has_1st_or_2nd_person_pronoun,
    lf_has_question_exclamation_marks,
    lf_imperative_speech,
    lf_is_repeated,
)
from weakly_supervised_method.model import WeaklySupervisedMethod
from snorkel.labeling.model import MajorityLabelVoter, LabelModel

from pprint import pprint

import logging

logging.basicConfig(level=logging.INFO)


def get_positive_samples(dataset, prediction_model, lf_data):
    preds = prediction_model.predict(L=lf_data)
    summaries = []

    for sample, pred in zip(dataset.articles, list(preds)):
        if pred == 1:
            summaries.append(
                {"title": sample.data["title"], "summary": sample.data["summary"]}
            )
    return summaries


if __name__ == "__main__":
    dataset = NewsRoomDataset("investigation_notebooks/train_samples.jsonl")

    noise_model = WeaklySupervisedMethod(
        [lf_too_short, lf_is_a_date, lf_has_HTML, lf_strange_ending]
    )
    noise_train = noise_model.fit(dataset)
    logging.info(noise_model.generate_train_report())

    noise_majority_model = MajorityLabelVoter()
    noise_label_model = LabelModel(cardinality=2, verbose=True)
    noise_label_model.fit(
        L_train=noise_train,
        n_epochs=500,
        log_freq=100,
        seed=123,
        class_balance=[0.5, 0.5],
    )

    majority_sample = get_positive_samples(dataset, noise_majority_model, noise_train)
    logging.info(
        f"Number of noisy samples detected by the majority voting model: {len(majority_sample)}"
    )
    label_samples = get_positive_samples(dataset, noise_majority_model, noise_train)
    logging.info(
        f"Number of noisy samples detected by the label merging model: {len(label_samples)}"
    )

    cleaned_dataset = dataset.generate_a_cleaned_dataset(
        noise_majority_model.predict(noise_train)
    )

    heuristics_model = WeaklySupervisedMethod(
        [
            lf_mostly_quotes,
            lf_has_1st_or_2nd_person_pronoun,
            lf_has_question_exclamation_marks,
            lf_imperative_speech,
            lf_is_repeated,
        ]
    )
    heuristics_train = heuristics_model.fit(cleaned_dataset)
    logging.info(heuristics_model.generate_train_report())

    heuristics_majority_model = MajorityLabelVoter()
    heuristics_label_model = LabelModel(cardinality=2, verbose=True)
    heuristics_label_model.fit(
        L_train=heuristics_train,
        n_epochs=500,
        log_freq=100,
        seed=123,
        class_balance=[0.5, 0.5],
    )
    majority_sample = get_positive_samples(
        cleaned_dataset, heuristics_majority_model, heuristics_train
    )
    logging.info(
        f"Number of strapline samples detected by the majority voting model: {len(majority_sample)}"
    )
    label_samples = get_positive_samples(
        cleaned_dataset, heuristics_majority_model, heuristics_train
    )
    logging.info(
        f"Number of strapline samples detected by the label merging model: {len(label_samples)}"
    )
