import spacy
from weakly_supervised_method.heuristics import lf_mostly_quotes
from weakly_supervised_method.data import NewsRoomArticle


spacy_model = spacy.load("en_core_web_sm")
ABSTAIN = -1
NOT_STRAPLINE = 0
STRAPLINE = 1


def test_high_quotes_coverage():
    article = NewsRoomArticle(
        {
            "summary": 'This summary "contains words between two double quotes"',
            "coverage": -1,
            "density": -1,
        }
    )
    article.compute_additional_fields(spacy_model)
    assert lf_mostly_quotes(article) == STRAPLINE


def test_low_quotes_coverage():
    article = NewsRoomArticle(
        {
            "summary": "This summary's single quote is a referential one",
            "coverage": -1,
            "density": -1,
        }
    )
    article.compute_additional_fields(spacy_model)
    assert lf_mostly_quotes(article) == ABSTAIN
