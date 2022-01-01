from weakly_supervised_method.data import NewsRoomDataset
from weakly_supervised_method.heuristics import (
    lf_too_short,
    lf_is_a_date,
    lf_has_HTML,
    lf_is_non_english,
)
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

import argparse
from weakly_supervised_method.eval import compute_metrics, generate_confusion_matrix
from sklearn.metrics import ConfusionMatrixDisplay
import matplotlib.pyplot as plt

plt.rcParams.update({"font.size": 18})

import glob
from pathlib import Path

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
    parser = argparse.ArgumentParser()
    parser.add_argument("--train", required=True, help="Path of the training data file")
    parser.add_argument("--test", required=True, help="Path of the training data file")
    parser.add_argument(
        "--plots_dir",
        default="../plots",
        help="Path of the directory to store the confusion matrices",
    )
    args = parser.parse_args()
    training_datafile = args.train
    test_data_path = args.test
    plots_dir = args.plots_dir

    dataset = NewsRoomDataset(training_datafile)

    noise_model = WeaklySupervisedMethod(
        [lf_too_short, lf_is_a_date, lf_has_HTML, lf_strange_ending, lf_is_non_english]
    )
    noise_train, _ = noise_model.fit(dataset)
    noise_majority_model = MajorityLabelVoter()

    label_samples = get_positive_samples(dataset, noise_majority_model, noise_train)
    logging.info(
        f"""Number of noisy samples detected by the majority voting model: {len(label_samples)} out of {len(dataset.articles)}"""
        f"""\nwith percentage: {len(label_samples)/len(dataset.articles)*100}"""
    )

    cleaned_dataset = dataset.filter_articles(
        drop_mask=noise_majority_model.predict(noise_train)
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
    heuristics_train, _ = heuristics_model.fit(cleaned_dataset)
    heuristics_majority_model = MajorityLabelVoter()
    majority_sample = get_positive_samples(
        cleaned_dataset, heuristics_majority_model, heuristics_train
    )
    logging.info(
        f"Number of strapline samples detected by the majority voting model: {len(majority_sample)}  out of {len(cleaned_dataset.articles)}"
        f"""\nwith percentage: {len(majority_sample)/len(dataset.articles)*100}"""
    )

    # Run evaluation
    # TODO: Refactor this part of the pipeline
    for test_data_path in glob.glob(test_data_path):
        evaluation_dataset = NewsRoomDataset(
            test_data_path,
            summaries_dict=cleaned_dataset.summaries_dict,
        )

        # Unify the labels and predictions
        label_map = {
            "summary": 0,
            "strapline": 1,
            "no_summary_no_strapline": 0,
            "summary_and_strapline": 1,
        }
        pred_map = {-1: 0, 1: 1, 0: 0}

        for threshold in range(1, len(heuristics_model.heuristics_list) + 1):
            predictions = []
            labels = []
            for article, noise_pred, pred in zip(
                evaluation_dataset.articles,
                noise_model.predict(evaluation_dataset)[-1],
                heuristics_model.predict(evaluation_dataset, threshold=threshold)[-1],
            ):
                pred = pred_map[pred]
                noise_pred = pred_map[noise_pred]
                label = label_map.get(article.data["annotation"], -1)
                if label == -1:
                    continue
                predictions.append(pred)
                labels.append(label)
            print("".join(compute_metrics(predictions, labels)))
            confusion_matrix = generate_confusion_matrix(predictions, labels)
            fig, ax = plt.subplots()

            display_labels = ["Not\nstrapline", "A strapline"]
            disp = ConfusionMatrixDisplay(
                confusion_matrix, display_labels=display_labels
            ).plot(cmap="Greens", colorbar=False, ax=ax)

            # ax.set_yticklabels(display_labels, rotation = 45)
            fig.savefig(
                f"{Path(plots_dir, Path(test_data_path).stem)}_threshold_{threshold}.pdf",
                bbox_inches="tight",
            )
