import json
import string

import unicodedata as ud
import sentencepiece as spm


lang_map = {
    'el': 'GREEK',
    'en': 'LATIN',
    'de': 'LATIN',
    'ru': 'CYRILLIC',
    'he': 'HEBREW',
    'ar': 'ARABIC'
}


def token_cleanup(token):
    token = token.strip()
    # For Marian vocab non-subwords start with ▁
    if token.startswith('▁'):
        token = token[1:]
    # Facebook FSMT models, non-subwords end with </w>
    if token.endswith('</w>'):
        token = token[:-4]
    return token


def is_valid_token(lang, token):
    assert ' ' not in token, '"%s"' % token
    token = token_cleanup(token)
    valid = False
    try:
        c_langs = [ud.name(c).split(' ', 1)[0] for c in token]
        # if lang == 'en':
        #     is_lang = all(c.lower() in string.ascii_lowercase for c in token)
        # else:
        is_lang = all(l == lang_map[lang] for l in c_langs)
        # is_digits = all(l == 'DIGIT' for l in c_langs)
        # is_punct = all(c in string.punctuation for c in token)
        # valid = is_lang or is_digits
        valid = is_lang
    except Exception as e:
        print(token, e)
        valid = False
    return valid


def load_vocab(filename):
    vocab = None
    if filename.endswith('.spm'):
        sp = spm.SentencePieceProcessor(model_file=filename)
        vocab = {sp.id_to_piece(i): i for i in range(sp.get_piece_size())}
    elif filename.endswith('.json'):
        with open(filename, 'r') as f:
            vocab = json.load(f)
    elif filename.endswith('.txt'):
        tokens = []
        with open(filename, 'r') as f:
            for i, line in enumerate(f):
                line = line.rstrip()
                token, _ = line.split(' ', 1)
                tokens.append((token, i))
        vocab = dict(tokens)
    else:
        raise ValueError('Do not know how to parse %s format' % filename)
    return vocab
