from gensim.models import CoherenceModel, LdaModel
import json
from numpy.random import RandomState


def read_lda_input(filename, title=False):
    """
    Read LDA input text from a specified file.

    Args:
        filename (str): A *.jl filename from which to read the LDA input text
        title (bool): Whether or not title should be included in a Tuple

    Returns:
        Any:
            If title is True, then list[list[str]], which is a list of the bag-of-words (list[str]) of each show.
            Else list[(str,list[str])], which is the same, but each element is a Tuple including the show title (str).
    """
    with open(filename) as f:
        lda_input = []
        for line in f:
            # Extract scraped JSON data for single anime show
            json_line = json.loads(line)
            text = json_line['LDA text']
            toks = text.split()
            elt = (json_line['title'], toks) if title else toks
            lda_input.append(elt)
    return lda_input


def get_lda_model(corpus, id2word, k, r=None, eta=None):
    """
    Run LDA with some specified inputs.

    Args:
        corpus (list[list[(int,int)]]):
            Bag-of-words representation of texts
        id2word (gensim.corpora.dictionary.Dictionary):
            A gensim Dictionary
        k (int):
            Number of topics
        r (int):
            Optional integer to seed random starting state, for reproducibility
        eta ({float, np.array, str}):
            Optional hyperparameter for LDA

    Returns:
        gensim.models.LdaModel: LDA output model object
    """
    if r is not None:
        r = RandomState(r)

    lda_model = LdaModel(
        corpus=corpus,
        num_topics=k,
        id2word=id2word,
        chunksize=100,
        random_state=r,
        update_every=1,
        eta=eta
    )
    return lda_model


def compute_coherence(lda_model, texts, corpus, id2word):
    """
    Compute the Coherence score for a given LDA model.

    Args:
        lda_model (gensim.models.LdaModel): LDA model object from gensim
        texts (list[list[str]]): List of texts, where a text is a list of tokens (strs)
        corpus (list[list[(int,int)]]): Bag-of-words representation of texts
        id2word (gensim.corpora.dictionary.Dictionary): A gensim Dictionary

    Returns:
        float: Coherence score of the LDA model
    """
    coherence_model = CoherenceModel(
        model=lda_model,
        texts=texts,
        corpus=corpus,
        dictionary=id2word
    )
    return coherence_model.get_coherence()
