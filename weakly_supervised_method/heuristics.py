import re
import dateutil
from snorkel.labeling import labeling_function
from weakly_supervised_method.heuristics_utils import (
    compute_quotes_coverage,
    has_strange_ending,
)

# NOTE: I am afraid of returning a NOT_STRAPLINE, NOT_NOISY label
# based on any of the heuristics so I am just ABSTAINing
NOT_STRAPLINE = 0
NOT_NOISY = 0

ABSTAIN = -1
STRAPLINE = 1
NOISY = 1

# Heuristics for noisy summaries
@labeling_function()
def lf_too_short(article):
    summary_n_tokens = len(article.data["summary_tokens"])
    return NOISY if summary_n_tokens <= 4 else ABSTAIN


@labeling_function()
def lf_is_a_date(article):
    try:
        # Attempt to parse the text as a date
        dateutil.parser.parse(article.data["summary"])
        return NOISY
    except:
        return ABSTAIN


@labeling_function()
def lf_has_HTML(article):
    # Attempt to parse the text as a date
    if re.findall(r"<[a-zA-Z0-9_]+[/]?>", article.data["summary"]):
        return NOISY
    return ABSTAIN


# Heuristics for strapline summaries
@labeling_function()
def lf_mostly_quotes(article):
    quotes_coverage = compute_quotes_coverage(article)
    return STRAPLINE if quotes_coverage > 0.6 else ABSTAIN


@labeling_function()
def lf_strange_ending(article):
    strange_ending = has_strange_ending(article)
    return STRAPLINE if strange_ending else ABSTAIN


@labeling_function()
def lf_has_1st_or_2nd_person_pronoun(article):
    set_of_person_pronouns = {
        "i",
        "me",
        "mine",
        "myself",
        "we",
        "our",
        "ours",
        "ourself",
        "ourselves",
        "you",
        "your",
        "yours",
        "yourself",
        "yourselves",
    }
    tokens = [t.text.lower() for t in article.data["summary_tokens"]]
    if any([t in set_of_person_pronouns for t in tokens]):
        return STRAPLINE
    return ABSTAIN


@labeling_function()
def lf_has_question_exclamation_marks(article):
    if any([c in article.data["summary"] for c in "?!"]):
        return STRAPLINE
    return ABSTAIN


@labeling_function()
def lf_imperative_speech(article):
    summary_tokens = article.data["summary_tokens"]
    if summary_tokens[0].tag_ == "VB":
        return STRAPLINE
    return ABSTAIN
