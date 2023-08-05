"""
This package will clean the text and lemmatize it. This will return output as text

"""
from grooming import txt
from nltk.stem import WordNetLemmatizer
from nltk import pos_tag
from nltk.corpus import wordnet
lemmatizer = WordNetLemmatizer()

def get_wordnet_pos(word):
    """Map POS tag to first character lemmatize() accepts"""
    tag = pos_tag([word])[0][1][0].upper()
    tag_dict = {"J": wordnet.ADJ,
                "N": wordnet.NOUN,
                "V": wordnet.VERB,
                "R": wordnet.ADV}
    return tag_dict.get(tag, wordnet.NOUN)

def lemm(text,txt_clean=True,word_len = 3,ignore_lem=[],rem_stopwords=True,extend_stpwords=[],cus_reg=None):
    """
    Description: Use this function to lemmatize the text.
    ---------

    Arguments:
    ---------
        txt: takes string as an input
        txt_clean: Default to True. Enabling it will clean the text.
        word_len: Default to 3. Length greater than this number will only be lemmatized
        ignore_lem: Default to blank. List of words which needs to be ignored in lemmatization process
        rem_stopwords: Default to True. Enabling it will remove the stopwords from the text. Stopwords are used from NLTK library.
        cus_reg: By default it will remove all the speacial characters and just keep the numbers and the words. However, custom regex expression can be provided here

    """
    try:
        clean_txt = str(text)
        if txt_clean:
            clean_txt = txt.cleaner(clean_txt,rem_stopwords=rem_stopwords,extend_stpwords=extend_stpwords,cus_reg=cus_reg)

        token = clean_txt.split(' ')
        token = [tok for tok in token if (tok not in ' ' or tok not in '')]
        lem = ''
        for t in token:
            if t.lower() not in ignore_lem and len(t)>word_len:
                lem += lemmatizer.lemmatize(t.lower(), get_wordnet_pos(t.capitalize()))+' '
            else:
                lem+=t.lower()+' '
        clean_txt = str.rstrip(lem)
    except LookupError:
        print(LookupError)
    except Exception as e:
        print(e)
    return clean_txt

    # lemm("I'm going to the market##",rem_stopwords=False,cus_reg='[^A-Za-z0-9+#]',word_len=3)
