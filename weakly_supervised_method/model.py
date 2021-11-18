from snorkel.labeling import LFApplier, LFAnalysis
from snorkel.labeling.model import MajorityLabelVoter, LabelModel
from weakly_supervised_method.heuristics import lf_too_short, lf_is_a_date, lf_has_HTML
from weakly_supervised_method.heuristics import (
    lf_mostly_quotes,
    lf_strange_ending,
    lf_has_1st_or_2nd_person_pronoun,
    lf_has_question_exclamation_marks,
    lf_imperative_speech,
    lf_is_repeated,
)


class WeaklySupervisedMethod:
    def __init__(self, heuristics_list):
        self.heuristics_list = heuristics_list
        self.applier = LFApplier(heuristics_list)
        self.label_model = MajorityLabelVoter(cardinality=2)

    def fit(self, dataset):
        self.train_labels = self.applier.apply(dataset.articles)
        return self.train_labels, self.label_model.predict(self.train_labels)

    def predict(self, dataset):
        labels = self.applier.apply(dataset.articles)
        return labels, self.label_model.predict(labels)

    def generate_train_report(self):
        # Check the overlaps/conflicts between labeling functions
        # Note: No conflicts for now since negative labels aren't used
        return LFAnalysis(L=self.train_labels, lfs=self.heuristics_list).lf_summary()
