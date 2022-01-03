import re
import dateutil
from snorkel.labeling import labeling_function
from weakly_supervised_method.heuristics_utils import (
    compute_quotes_coverage,
    has_strange_ending,
)
from langdetect import detect

# for clickbait detection
import torch
from transformers import DistilBertTokenizerFast
from torch.utils.data import DataLoader
from transformers import DistilBertForSequenceClassification, AdamW, get_scheduler, logging

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
    non_punct_tokens = [
        token for token in article.data["summary_tokens"] if not token.is_punct
    ]
    summary_n_tokens = len(non_punct_tokens)
    return NOISY if summary_n_tokens <= 3 else ABSTAIN


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
    # Look for tags in the form <...> or <.../>
    if re.findall(r"<[a-zA-Z0-9_]+[/]?>", article.data["summary"]):
        return NOISY
    # Look for formatting in the form ...="
    if re.findall(r"[a-z]+=\"", article.data["summary"]):
        return NOISY
    return ABSTAIN


@labeling_function()
def lf_strange_ending(article):
    strange_ending = has_strange_ending(article)
    return STRAPLINE if strange_ending else ABSTAIN


@labeling_function()
def lf_is_non_english(article):
    try:
        lang = detect(str(article.data["text"]))
    except:
        # Fallback to English
        lang = "en"
    return NOISY if lang != "en" else ABSTAIN


# Heuristics for strapline summaries
@labeling_function()
def lf_mostly_quotes(article):
    quotes_coverage = compute_quotes_coverage(article)
    return STRAPLINE if quotes_coverage > 0.36 else ABSTAIN


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


@labeling_function()
def lf_is_repeated(article):
    if (
        article.data["summary_repetition_count"] > 1
        or article.data["title_repetition_count"] > 1
    ):
        return STRAPLINE
    return ABSTAIN


@labeling_function()
def lf_is_clickbait(article):
    device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')

    tokenizer = DistilBertTokenizerFast.from_pretrained('./clickbait_models/DistilBert4ClickBait.tokenizer/')
    model = DistilBertForSequenceClassification.from_pretrained('./clickbait_models/DistilBert4ClickBait.model/').to(device)

    input_encodings = tokenizer(article.data["summary"], truncation=True, padding=True)
    input_ids = torch.tensor(input_encodings['input_ids']).unsqueeze(0).to(device)
    attention_mask = torch.tensor(input_encodings['attention_mask']).to(device)

    model.eval()
    with torch.no_grad():
        outputs = model(input_ids, attention_mask)
        predictions = torch.argmax(outputs.logits, dim=-1)
        if(predictions.item()):
            return STRAPLINE
        return ABSTAIN