import spacy

# You will need to download the model:
# python -m spacy download en_core_web_sm
# This is the same model used in the NewsRoom paper for tokenization
spacy_model = spacy.load("en_core_web_sm")


def get_normalized_density(summary, old_density):
    """
    Normalize the density value to be in range [0, 1]

    summary: The string representation of the summary
    old_density: The density value associated to this summary in NewsRoom
    """
    return old_density / len(spacy_model(summary))


def get_normalized_density_bin_classification(summary, old_density):
    """
    Normalize the density value to be in range [0, 1]

    summary: The string representation of the summary
    old_density: The density value associated to this summary in NewsRoom
    """
    normalized_density = get_normalized_density(summary, old_density)

    # Those thesholds are computed on a random sample of 10,000 articles
    th1, th2 = (0.07958477508823529, 0.2988165680461538)

    if normalized_density >= th2:
        return "extractive"

    if normalized_density >= th1:
        return "mixed"

    return "abstractive"
