import pytest
import spacy
from weakly_supervised_method.heuristics import (
    lf_mostly_quotes,
    lf_strange_ending,
    lf_has_1st_or_2nd_person_pronoun,
    lf_has_question_exclamation_marks,
    lf_imperative_speech,
    lf_is_repeated,
)
from weakly_supervised_method.data import NewsRoomArticle
from weakly_supervised_method.heuristics import ABSTAIN, NOT_STRAPLINE, STRAPLINE

# Create this model only once for this testing module
@pytest.fixture
def spacy_model(scope="module"):
    return spacy.load("en_core_web_sm")


def test_high_quotes_coverage(spacy_model):
    article = NewsRoomArticle(
        {
            "summary": 'This summary "contains words between two double quotes"',
            "coverage": -1,
            "density": -1,
        }
    )
    article.compute_additional_fields(spacy_model)
    assert lf_mostly_quotes(article) == STRAPLINE


def test_low_quotes_coverage(spacy_model):
    article = NewsRoomArticle(
        {
            "summary": "This summary's single quote is a referential one",
            "coverage": -1,
            "density": -1,
        }
    )
    article.compute_additional_fields(spacy_model)
    assert lf_mostly_quotes(article) == ABSTAIN


def test_ending_with_a_determiner(spacy_model):
    article = NewsRoomArticle(
        {
            "summary": "This summary ends with a determiner an",
            "coverage": -1,
            "density": -1,
        }
    )
    article.compute_additional_fields(spacy_model)
    assert lf_strange_ending(article) == STRAPLINE


def test_ending_with_a_dot(spacy_model):
    article = NewsRoomArticle(
        {
            "summary": "This summary ends with a dot.",
            "coverage": -1,
            "density": -1,
        }
    )
    article.compute_additional_fields(spacy_model)
    assert lf_strange_ending(article) == ABSTAIN


def test_ending_with_a_comma(spacy_model):
    article = NewsRoomArticle(
        {
            "summary": "This summary ends with a comma,",
            "coverage": -1,
            "density": -1,
        }
    )
    article.compute_additional_fields(spacy_model)
    assert lf_strange_ending(article) == STRAPLINE


def test_1st_pronoun(spacy_model):
    article = NewsRoomArticle(
        {
            "summary": "I might be a strapline.",
            "coverage": -1,
            "density": -1,
        }
    )
    article.compute_additional_fields(spacy_model)
    assert lf_has_1st_or_2nd_person_pronoun(article) == STRAPLINE


def test_using_question_mark(spacy_model):
    article = NewsRoomArticle(
        {
            "summary": "I might be a strapline?",
            "coverage": -1,
            "density": -1,
        }
    )
    article.compute_additional_fields(spacy_model)
    assert lf_has_question_exclamation_marks(article) == STRAPLINE


def test_imperative_speech(spacy_model):
    article = NewsRoomArticle(
        {
            "summary": "Check me now.",
            "coverage": -1,
            "density": -1,
        }
    )
    article.compute_additional_fields(spacy_model)
    assert lf_imperative_speech(article) == STRAPLINE


def test_is_repeated(spacy_model):
    article = NewsRoomArticle(
        {
            "summary": "Check me now.",
            "coverage": -1,
            "density": -1,
            "summary_repetition_count": 10,
        }
    )
    article.compute_additional_fields(spacy_model)
    assert lf_is_repeated(article) == STRAPLINE
