import pytest
import spacy
from weakly_supervised_method.heuristics import lf_is_a_date, lf_too_short
from weakly_supervised_method.data import NewsRoomArticle
from weakly_supervised_method.heuristics import ABSTAIN, NOT_NOISY, NOISY

# Create this model only once for this testing module
@pytest.fixture
def spacy_model(scope="module"):
    return spacy.load("en_core_web_sm")


def test_date_summary(spacy_model):
    article = NewsRoomArticle(
        {
            "summary": "16 Nov, 2021",
            "coverage": -1,
            "density": -1,
        }
    )
    article.compute_additional_fields(spacy_model)
    assert lf_is_a_date(article) == NOISY


def test_not_a_date_summary(spacy_model):
    article = NewsRoomArticle(
        {
            "summary": "This summary was written in 16 Nov, 2021",
            "coverage": -1,
            "density": -1,
        }
    )
    article.compute_additional_fields(spacy_model)
    assert lf_is_a_date(article) == ABSTAIN


def test_too_short(spacy_model):
    article = NewsRoomArticle(
        {
            "summary": "I am short",
            "coverage": -1,
            "density": -1,
        }
    )
    article.compute_additional_fields(spacy_model)
    assert lf_too_short(article) == NOISY
