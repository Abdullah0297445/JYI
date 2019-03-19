#imports
import pandas as pd
import re
from bs4 import BeautifulSoup as bs
import requests
import nltk, string
from nltk.stem import PorterStemmer
from nltk.stem.wordnet import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
from nltk.tokenize import wordpunct_tokenize
import argparse
import os
import sys
from selenium import webdriver
from selenium.webdriver import ChromeOptions


def excelPreProcess(file, sheet):
    """
    This function takes a Excel file and convert it into a pandas data frame so that we can 
    extract information more easily.
    """

    #Reading the excel file into pandas dataframe.
    try:
        print("Reading input file..")
        frame = pd.read_excel(file, sheet_name = sheet)
        frame['Path'] = frame['Page path level 1'] + frame['Page path level 2'] + frame['Page path level 3'] + frame['Page path level 4']
        print('Done!')
        return frame
    except:
        print("Can't open input file.")
        sys.exit()

def makeAddress(data_frame):
    """
    This function takes in a pandas data frame and extracts JYI website addresses from it. 
    """
    pathList = data_frame['Path'].tolist()
    for i in range(len(pathList)) :
        pathList[i] = re.sub('//', '/', pathList[i])

    return pathList


def stemmerandlemmer(tokens):
    """
    This method takes in tokens then lemmatize them and then stem them. Its purpose is to make data
    consistent.
    """
    
    return [PorterStemmer().stem(WordNetLemmatizer().lemmatize(token)) for token in tokens]


def Normalize(text):
    """
    This is a helper function. It removes punctuation and tokenize the string data given to it. 
    """
    
    #Removing punctuation
    remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)
    #Lowering all the words and tokenizing them. 
    return stemmerandlemmer(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))


def cosine_sim(corpus):
    """
    Finds Cosine similarity score between all the documents given to it. It returns a matrix.
    It follows TF-IDF approach. 
    """
    
    vectorizer = TfidfVectorizer(tokenizer=Normalize, analyzer='word', stop_words='english')
    
    print("Calculating Similarity..")
    tfidf = vectorizer.fit_transform(corpus)
    print("Done!")
    return (tfidf * tfidf.T).A


def crawler(address_list):
    """
    A list of addresses is provided to this method and it goes and downloads those articles. E.g an Element of the given list can be this:
    https://www.jyi.org/2019-march/2019/3/1/the-implication-of-the-corticotropin-releasing-factor-in-nicotine-dependence-and-significance-for-pharmacotherapy-in-smoking-cessation
    """

    print("Downloading Articles.. Please wait.")
    #Whole Corpus which will contain every article from the input excel file.
    corpus = []

    #Setting browser options which will be running in the background.
    options = ChromeOptions()
    options.add_argument('headless')
    options.add_argument('--log-level=3')
    #options.add_argument('--disable-extensions')
    browser = webdriver.Chrome('chromedriver', chrome_options=options)

    #Visiting website and Downloading the text article data. 
    for address in address_list:
        try:
            #Download the whole webpage.
            site = 'https://www.jyi.org' + address
            browser.get(site)
            

        except:
            print("Can't connect to URL. Check your internet connection.")
            sys.exit()

        #Parse the webpage as HTML. 
        soup = bs(browser.page_source, 'html.parser')
        #soup.prettify()
        
        
        #This list will contain whole the article. 
        document = []

        try:
            #Finding the components which contain textual research data from the soup.
            parents = soup.find('div', 'entry-content e-content')
            parents = parents.find_all('div', 'sqs-block html-block sqs-block-html')
        except:
            print("Website structure is changed. OR Internet connection isn't smooth.")
            sys.exit()
        
        
        for parent in parents:
            #Since there are many components in a single webpage which contain textual research data. 
            #We go through them one by one extracting that text.
            parent = parent.find('div', 'sqs-block-content')
            
            #Deleting some unwanted components from the soup.
            disposable = parent.find_all('ol')
            if disposable != None:
                for all in disposable:
                    all.decompose()
            
            #Each paragraph will be an element in our document list. 
            Children = parent.find_all('p')
            for each in Children:
                document.append(each.text)
        
        #we join all the paragraphs into one single passage. 
        doc_str = " ".join(document)
        #Removing unwanted unicode characters.
        doc_str = doc_str.replace(u'\xa0', u' ')
        #A single document is appended to whole corpus. 1 element of corpus list
        #is a complete downloaded document.
        corpus.append(doc_str)
    
    print("All articles downloaded successfully.")
    #Finding cosine similarity between all documents.
    array = cosine_sim(corpus)
    
    browser.quit()
    return array, corpus

def writeback(inputFrame, array, path):
    """
    Writes an Excel .xlsx file with columns structure:
    Article 1    Views   Article 2    Views   Similarity 

    This file shows highest similarity of Article 1 with another article which will be specified under
    Article 2 column. They both have Views column which shows how many visits these pages have. 
    """

    print('Writing output file..')
    #Creating a dictionary skeleton which will be coverted to a data frame. 
    d = {'Article 1':[], 'Views 1':[], 'Article 2':[], 'Views 2':[], 'Similarity':[]}

    #Populating data
    for i in range(len(inputFrame.index) - 1) :
        
        d['Article 1'].append(inputFrame['Page Title'][i])
        d['Views 1'].append(inputFrame['Users'][i])
        array[i][array[i].tolist().index(max(array[i].tolist()))] = 0.0 
        d['Article 2'].append(inputFrame['Page Title'][array[i].tolist().index(max(array[i].tolist()))])
        d['Views 2'].append(inputFrame['Users'][array[i].tolist().index(max(array[i].tolist()))])
        d['Similarity'].append(max(array[i].tolist()) * 100)
    
    #Converting dictionary to pandas dataframe
    a = pd.DataFrame(data = d)
    #Writing dataframe to excel file
    
    a.to_excel(path+'output.xlsx', sheet_name='Dataset1', index=False)
    print("Done!")

if __name__ == "__main__":

    #Adding command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-i","--inputfile", help="Specify the input xlsx file path. \n E.g. C:\\user\\downloads\\Excel.xlsx")
    parser.add_argument("-s","--sheet", help="Specify the sheet name in xlsx file. \n E.g. Dataset1")
    parser.add_argument("-o","--outputfile", help="Specify the directory you want to save output xlsx file. \n E.g. C:\\user\\downloads\\")
    args = parser.parse_args()
    ##

    #Giving functionality to args
    if args.inputfile:
        input_file = args.inputfile
    else:
        input_file = 'input.xlsx'
    if args.sheet:
        sheet = args.sheet
    else:
        sheet = 'Dataset1'
    if args.outputfile:
        args.outputfile = re.sub('/', '//', args.outputfile)
        output_file = args.outputfile
    else:
        output_file = os.getcwd() + '\\'
    ##

    #Excel to pandas dataframe
    frame = excelPreProcess(input_file,sheet)
    ##

    #Extract JYI articles links from dataframe
    address_list = makeAddress(frame)
    ##

    #Crawler
    sim_array, corpus = crawler(address_list)
    #print(sim_array)
    ##

    #Write Output file
    writeback(frame, sim_array, output_file)
    #print(type(sim_array))
    ##

    print("Exporting downloaded articles..")
    #Export downloaded articles as txt file
    with open('Downloaded Articles.txt', mode='wt', encoding='utf-8') as f:
        f.write('\n\n|############|\n\n'.join(corpus))
    ##

    print('All Done!')
