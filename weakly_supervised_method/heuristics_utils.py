def compute_quotes_coverage(article):
    """
    Compute the quotes coverage for a summary

    article: A NewsRoomArticle object

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

    summary_tokens = [t.text for t in article.data["summary_tokens"]]
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


def has_strange_ending(article):
    """
    Check if the summary ends abruptly

    article: A NewsRoomArticle object

    returns:
    A boolean value
    """
    summary_tokens = article.data["summary_tokens"]

    last_token_text = summary_tokens[-1].text.lower().strip()
    # List of pos tags can be found through: https://universaldependencies.org/u/pos/
    last_token_pos = summary_tokens[-1].pos_

    if last_token_text in ".":
        return False

    if last_token_text in ",":
        return True

    if (
        last_token_pos in ["DET", "INTJ", "CCONJ", "SCONJ", "X"]
        and last_token_text != "all"
    ):
        return True

    if last_token_pos == "PRON" and last_token_text in ["what", "who", "which", "that"]:
        return True

    return False
