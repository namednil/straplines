import dateutil
from snorkel.labeling import labeling_function
from weakly_supervised_method.heuristics_utils import (
    compute_quotes_coverage,
    has_strange_ending,
)

# from weakly_supervised_method.data import NewsRoomArticle

# NOTE: I am afraid of returning a NOT_STRAPLINE label
# based on any of the heuristics so I am just ABSTAINing

ABSTAIN = -1
NOT_STRAPLINE = 0
STRAPLINE = 1


@labeling_function()
def lf_mostly_quotes(article):
    quotes_coverage = compute_quotes_coverage(article)
    return STRAPLINE if quotes_coverage > 0.6 else ABSTAIN


@labeling_function()
def lf_strange_ending(article):
    strange_ending = has_strange_ending(article)
    return STRAPLINE if strange_ending else ABSTAIN
