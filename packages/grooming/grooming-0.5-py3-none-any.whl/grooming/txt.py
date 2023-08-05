"""
This package is combination of text clean up process to reduce lot of extra lines in the code. Package is purely built on top
nltk and re libraries.

Usage:
cleaner: Use this function to clean all kind of junk from the text.
clean_email: Use this function to remove the emails from the text.
clean_html: Use this function to remove the html Tags from the text.
word2num: Use this function to convert word representation of number to actual number in the text.
clean_stopword: Use this function to remove stopwords from the text. This uses default stopword library from NLTK.

"""

from nltk.tokenize import   word_tokenize
from nltk.corpus import stopwords
import re
from word2number import w2n

def clean_email(email):
    """
    Description: Use this function to remove the emails from the text.
    """
    try:
        email = str(email)
        e_cleanr = re.compile("(\S+@\S+)")
        cleantext = re.sub(e_cleanr, '', email)
    #     cleantext = re.findall(e_cleanr, email)
    except Exception as e:
        print(e)
    return cleantext

#to clean the HTML tags
def clean_html(raw_html):
    """
    Description: Use this function to remove the html Tags from the text.
    """
    try:
        raw_html = str(raw_html)
        cleanr = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
        cleantext = re.sub(cleanr, '', raw_html)
    except Exception as e:
        print(e)
    return cleantext

def word2num(txt):
    """
    Description: Use this function to convert word representation of number to actual number in the text.
    """
    try:
        txt = str(txt)
        token = txt.split(" ")
        token = [tok for tok in token if tok not in ' ' or tok not in '']
        w2n_txt=''
        for t in token:
            try:
                num = w2n.word_to_num(t)
                w2n_txt+=str(num)+' '
            except:
                w2n_txt+=t+' '
        w2n_txt = w2n_txt.strip()
    except Exception as e:
        print(e)
    return w2n_txt

def clean_stopword(stp_txt,ext_stp=[]):
    """
    Description: Use this function to remove stopwords from the text. This uses default stopword library from NLTK.
    """
    try:
        stp_txt=str(stp_txt)
        stopset = set(stopwords.words('english')) #list of stopwords from nltk library
        if ext_stp:
            stopset = stopwords.words('english')
            stopset.extend(ext_stp)
            stopset = set(stopset)
        token = stp_txt.split(' ')
        token = [tok for tok in token if tok not in ' ' or tok not in ''] #remove blank split
        stp_txt = " ".join([w for w in token if w not in stopset]) #adding the text back to string
    except Exception as e:
        print(e)
    return stp_txt


def cleaner(text,rem_email = True,rem_html = True,rem_stopwords=True,extend_stpwords=[],word2number=True,cus_reg=None,rem_space=True,need_token = False):

    """
    Description: Function will clean up different kind of junk in the text. Appropiate argument should be selected to customize.
    ---------

    Arguments:
    ---------
        rem_email: Default to True. Enabling it will remove the email Ids from the text.
        rem_html: Default to True. Enabling it will remove the html tags from the text.
        rem_stopwords: Default to True. Enabling it will remove the stopwords from the text. Stopwords are used from NLTK library.
        wrod2number: Default to True. Enabling it will convert word representation of numbers into actual numbers from the text.
        cus_reg: By default it will remove all the speacial characters and just keep the numbers and the words. However, custom regex expression can be provided here
        rem_space: Default to True. Enabling it will remove additional spaces from the text.
        need_token: Default to false. Enabling it will return the text in tokens.

    """
    try:
        clean_text=str(text)
        if rem_email:
            clean_text = clean_email(clean_text) #remove emails from text

        if rem_html:
            clean_text = clean_html(clean_text) #remove html tag from clean_text

        if rem_stopwords:
            clean_text = clean_stopword(clean_text,extend_stpwords)

        if cus_reg:
            clean_text = re.sub(cus_reg,' ',clean_text)
        else:
            clean_text = re.sub('[^A-Za-z0-9+]',' ',clean_text)

        if word2number:
            clean_text = word2num(clean_text)

        if rem_space:
            token = clean_text.split(" ")
            token = [tok for tok in token if tok not in ' ' or tok not in '']
            clean_text = " ".join(token)

        if need_token:
            clean_text = tokenizer.tokenize(clean_text)

        return clean_text
    except Exception as e:
        print('Error occured:',e)
