from snorkel.labeling import LFApplier, LFAnalysis
import logging

logging.basicConfig(level=logging.INFO)


def votes_to_predictions(votes, threshold):
    """Convert rows of votes into predictions"""

    n_voting = (votes == 1).sum(axis=1)
    predictions = n_voting >= threshold

    return predictions


class WeaklySupervisedMethod:
    def __init__(self, heuristics_list):
        """Construct a weakly supervised method using a list of snorkel heuristics"""
        self.heuristics_list = heuristics_list
        self.applier = LFApplier(heuristics_list)

    def fit(self, dataset, threshold=1):
        """Fit the labelling functions using a dataset object"""
        train_votes = self.applier.apply(dataset.articles)
        logging.info(self.generate_lfs_report(train_votes))

        return train_votes, votes_to_predictions(train_votes, threshold)

    def predict(self, dataset, threshold=1):
        """Generate predictions"""
        votes = self.applier.apply(dataset.articles)
        return votes, votes_to_predictions(votes, threshold)

    def generate_lfs_report(self, votes):
        # Check the overlaps/conflicts between labeling functions
        # Note: No conflicts for now since negative labels aren't used
        return LFAnalysis(L=votes, lfs=self.heuristics_list).lf_summary()

    # TODO: Store/load the dataset to avoid repetitive computations
    def pickle(self):
        pass

    def unpickle(self):
        pass
