from weakly_supervised_method.data import NewsRoomDataset
from snorkel.labeling import LFApplier, LFAnalysis
from heuristics import lf_too_short, lf_is_a_date, lf_has_HTML
from heuristics import (
    lf_mostly_quotes,
    lf_strange_ending,
    lf_has_1st_or_2nd_person_pronoun,
    lf_has_question_exclamation_marks,
    lf_imperative_speech,
)


class WeaklySupervisedMethod:
    def __init__(self, heuristics_list):
        self.heuristics_list = heuristics_list
        self.applier = LFApplier(heuristics_list)

    def fit(self, dataset):
        self.train_labels = self.applier.apply(dataset.articles)
        return self.train_labels

    def generate_train_report(self):
        # Check the overlaps/conflicts between labeling functions
        # Note: No conflicts for now since negative labels aren't used
        return LFAnalysis(L=self.train_labels, lfs=self.heuristics_list).lf_summary()


if __name__ == "__main__":
    dataset = NewsRoomDataset("investigation_notebooks/train_samples.jsonl")
    noise_model = WeaklySupervisedMethod([lf_too_short, lf_is_a_date, lf_has_HTML])
    noise_model.fit(dataset)
    print(noise_model.generate_train_report())
    heuristics_model = WeaklySupervisedMethod(
        [
            lf_mostly_quotes,
            lf_strange_ending,
            lf_has_1st_or_2nd_person_pronoun,
            lf_has_question_exclamation_marks,
            lf_imperative_speech,
        ]
    )
    heuristics_model.fit(dataset)
    print(heuristics_model.generate_train_report())
