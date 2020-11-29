import unicodedata
import json
import nltk
from nltk.corpus import stopwords
from nltk.corpus import wordnet
from nltk.tokenize import word_tokenize

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
    ord('—'): ' '    # Long hyphen which is often used in the MAL descriptions
}

# Frequently-appearing words which aren't useful for LDA
# TODO: Add unwanted words
unwanted_words = {}


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


def clean_text(text, unwanted):
    """
    Prepares text to be fed into the LDA algorithm.

    Args:
        text     (str):      Input text of a single document
        unwanted (set[str]): Words to be filtered out of text

    Returns:
        list[str]: Tokenized/cleaned list of strings for LDA
    """
    text_ascii = text.translate(char_table)  # Hepburn vowels, etc
    text_ascii = unicodedata.normalize('NFKD', text_ascii).encode('ascii', 'ignore').decode('utf-8')  # Other odd chars

    toks = word_tokenize(text_ascii)  # Initial split
    toks = [tok.lower() for tok in toks if len(tok) > 3]  # Get rid of particles/punctuation, and lowercase
    toks = [tok for tok in toks if tok not in unwanted]  # Remove stop-words, and other unwanted words
    toks = [get_lemma(tok) for tok in toks]  # Lemmatize (not Stem) to get reduced versions of words
    return toks


################################################################################
#                                     MAIN                                     #
################################################################################

def main():
    print('Cleaning scraped data...')
    with open(input_filename, 'r') as in_f, open(output_filename, 'w') as out_f:
        # Words to exclude for LDA
        unwanted = set(stopwords.words('English'))
        unwanted.union(unwanted_words)
        for in_line in in_f:
            # Read scraped input JSON for this anime
            in_json = json.loads(in_line)
            title = in_json['title']
            print('    {:60}'.format('{}...'.format(title)), end='')
            desc = in_json['description']

            # Clean description
            toks = clean_text(desc, unwanted=unwanted)

            # Write output JSON as newline
            out_json = {
                'title':    title,
                'LDA text': ' '.join(toks)
            }
            out_line = json.dumps(out_json)
            out_f.write('{}\n'.format(out_line))
            print('Done!')
    print('Done!\n')
    return None


if __name__ == '__main__':
    main()
