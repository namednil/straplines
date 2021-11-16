import dateutil
from snorkel.labeling import labeling_function

# from weakly_supervised_method.data import NewsRoomArticle

# NOTE: I am afraid of returning a NOT_STRAPLINE label
# based on any of the heuristics so I am just ABSTAINing

ABSTAIN = -1
NOT_STRAPLINE = 0
STRAPLINE = 1


def compute_quotes_coverage(article):
    """
    Compute the quotes coverage for a summary

    article: A NewsRoomArticleObject

    returns:
    A value in range [0, 1] representing the percentage of tokens
    that are enclosed in quotes
    """
    n_tokens_inside = 0
    # Keep track of nested quotes
    quotes_stack = []
    # Count the number of tokens inside the current quotes range
    tokens_in_quotes = []

    # TODO: Is single quotation ' needed as well?
    quotes = '”“‘’"'

    summary_tokens = article.data["summary_tokens"]
    for token in summary_tokens:
        #  This token is inside a candidate quotes range
        if quotes_stack and token not in quotes:
            tokens_in_quotes[-1] += 1

        # The current token is a quotation
        if token in quotes:
            # This is the end of a quotes range
            if quotes_stack and abs(ord(token) - ord(quotes_stack[-1])) <= 1:
                quotes_stack.pop(-1)
                # Increment the number of tokens inside quotes range
                # only when the range ends
                n_tokens_inside += tokens_in_quotes[-1]
                tokens_in_quotes.pop(-1)

            # This is the start of a new range
            else:
                quotes_stack.append(token)
                tokens_in_quotes.append(0)

    n_non_quotes_tokens = len(
        [token for token in summary_tokens if token not in quotes]
    )
    return n_tokens_inside / n_non_quotes_tokens


@labeling_function()
def lf_mostly_quotes(article):
    quotes_coverage = compute_quotes_coverage(article)
    return STRAPLINE if quotes_coverage > 0.6 else ABSTAIN
