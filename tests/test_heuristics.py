import pytest
import spacy
from weakly_supervised_method.heuristics import lf_mostly_quotes
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
