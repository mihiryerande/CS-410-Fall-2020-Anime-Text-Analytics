import gensim
import json
import nltk
from nltk.corpus import stopwords
from nltk.corpus import wordnet
from nltk.tokenize import word_tokenize
import unicodedata

# Make sure some stuff is downloaded
nltk.download('averaged_perceptron_tagger')
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

################################################################################
#                                 GLOBAL VARS                                  #
################################################################################

# Relevant filenames
input_filename = 'scraped.jl'
output_filename = 'lda_input.jl'

# Char table to convert Hepburn vowels to ASCII
char_table = {
    ord('ā'): 'aa',
    ord('Ā'): 'Aa',
    ord('ē'): 'ee',
    ord('Ē'): 'Ee',
    ord('ī'): 'ii',
    ord('Ī'): 'Ii',
    ord('ō'): 'ou',  # Not necessarily correct! Might be 'oo'
    ord('Ō'): 'Oo',  # More typical to see starting double-O, like in Ōsaka
    ord('ô'): 'ou',  # Circumflex version sometimes used in Tôkyô
    ord('ū'): 'uu',
    ord('Ū'): 'Uu',
    ord('~'): ' ',  # Stylistic punctuation
    ord('+'): ' ',  # Stylistic punctuation
    ord('－'): ' ',  # Japanese hyphen-like char for vowel lengthening
    ord('—'): ' ',   # Long hyphen which is often used in the MAL descriptions
    ord('-'): ' ',   # Split any words joined with hyphens
    ord('/'): ' '    # Split any words joined with slashes
}

# Frequently-appearing words which aren't useful for LDA
# TODO: Add unwanted words
unwanted_words = set()
# {
#     'anime',
#     'manga',
#     'season',
#     'series'
# }


################################################################################
#                               HELPER FUNCTIONS                               #
################################################################################

def get_wordnet_pos(treebank_tag):
    """
    Helper function to get the WordNet POS tag from a treebank tag

    Args:
        treebank_tag (str): A treebank tag as given by nltk.pos_tag()

    Returns:
        str: POS-tag usable in WordNet functions
    """
    if treebank_tag.startswith('J'):
        return wordnet.ADJ
    elif treebank_tag.startswith('V'):
        return wordnet.VERB
    elif treebank_tag.startswith('R'):
        return wordnet.ADV
    else:
        # Assume everything else is Noun by default
        return wordnet.NOUN


def get_lemma(tok):
    """
    Helper function to get the lemmatized form of a given token.

    Args:
        tok (str): A token to lemmatize

    Returns:
        str: Lemmatized form of the token
    """
    # Get the POS tag
    pos_tb = nltk.pos_tag([tok])[0][1]
    pos_wn = get_wordnet_pos(pos_tb)

    # Return the lemma, if possible
    wn_lemma = wordnet.morphy(tok, pos=pos_wn)
    return wn_lemma or tok


def clean_tok(tok, unwanted):
    """
    Helper function to apply additional token-level cleaning, mostly related to punctuation.

    Args:
        tok      (str):      A token to clean
        unwanted (set[str]): Words to be filtered out of text

    Returns:
        str: Cleaned token, which may now include spaces
    """
    # Apostrophes
    tok_clean = tok.strip("'")  # Maintains internal apostrophes such as in "jun'ichi"

    # Commas --> Fine since they only appear in numbers (1,000)

    # Periods
    if any(c.isdigit() for c in tok_clean):
        tok_clean = tok_clean  # Leave decimal-looking toks alone
    else:
        tok_clean.lstrip(".")  # Kill ellipses and odd cases
        tok_split = tok_clean.split(".")
        if any(len(sub_tok) == 1 for sub_tok in tok_split):
            tok_clean = tok_clean  # Leave splits with any single-letter alone --> probably acronym
        else:
            # Keep sub-tokens separate by rejoining with spaces
            tok_split = [sub_tok for sub_tok in tok_split if sub_tok not in unwanted]  # Re-filter any stopwords away
            tok_clean = ' '.join(tok_split)  # Rejoin without periods, to split accidentally joined words
    return tok_clean


def clean_text(text, unwanted):
    """
    Prepares text to be fed into the LDA algorithm.

    Args:
        text     (str):      Input text of a single document
        unwanted (set[str]): Words to be filtered out of text

    Returns:
        str: Tokenized/cleaned text to feed into LDA
    """
    text_clean = text.translate(char_table)  # Hepburn vowels, etc
    text_clean = unicodedata.normalize('NFKD', text_clean).encode('ascii', 'ignore').decode('utf-8')  # Other odd chars
    # if any((c in punctuation) for c in text_clean):
    #     text_clean = text_clean.translate(str.maketrans('', '', punctuation))

    toks = word_tokenize(text_clean)  # Initial split
    toks = [tok.lower() for tok in toks if len(tok) > 3]  # Get rid of particles/punctuation, and lowercase
    toks = [tok for tok in toks if tok not in unwanted]  # Remove stop-words, and other unwanted words
    toks = [get_lemma(tok) for tok in toks]  # Lemmatize (not Stem) to get reduced versions of words
    toks = [clean_tok(tok, unwanted) for tok in toks]  # Additional specific token cleaning for LDA
    toks = [tok for tok in toks if len(tok) > 0]  # Some cleaned tok may have become empty

    text_clean = ' '.join(toks)  # Final join to clean up
    return text_clean


################################################################################
#                                     MAIN                                     #
################################################################################

def main():
    print('Cleaning scraped data...')
    with open(input_filename, 'r') as in_f, open(output_filename, 'w') as out_f:
        # Words to exclude for LDA
        unwanted = unwanted_words  # Specified words to ignore
        unwanted.update(set(stopwords.words('English')))  # NLTK stopwords
        unwanted.update(gensim.parsing.preprocessing.STOPWORDS)  # Gensim stopwords
        for in_line in in_f:
            # Read scraped input JSON for this anime
            in_json = json.loads(in_line)
            title = in_json['title']
            print('    {:60}'.format('{}...'.format(title)), end='')
            desc = in_json['description']

            # Clean description
            desc_clean = clean_text(desc, unwanted)
            if not desc_clean:
                desc_clean = clean_text(title, unwanted)  # Use title as LDA text, if necessary

            # Write output JSON as newline
            out_json = {
                'title':    title,
                'LDA text': desc_clean
            }
            out_line = json.dumps(out_json)
            out_f.write('{}\n'.format(out_line))
            print('Done!')
    print('Done!\n')
    return None


if __name__ == '__main__':
    main()
