# JYI

This repository holds python script to scrape research articles from jyi.org and find which articles are most similar to each other. <br/>
Cosine similarity has been used to measure the similarity between articles. TF-IDF model has been used. 

# About JYI

JYI is a student-led initiative to broaden the undergraduate scientific experience, allowing students to participate in the scientific review and publication processes of its peer-reviewed undergraduate journal. Incorporated as a non-profit, student-run corporation, JYI represents over 50 different academic institutions from over half a dozen countries.

# Requirements:
You need to install following python packages because this project depends on those. 

 1. Pandas
```python
pip install pandas
```
 2. NLTK 
```python
pip install nltk
```
After installing nltk you have to download all the necessary text data it provides like stopwords etc.
You can do that in 3 simple steps:

1.Open CMD <br/>
2.Write 'python' in the prompt so a python environement will start. <br/>
3.Write these two lines of code into the prompt. 

```python
import nltk
nltk.download('all')
```
Wait till download is finished.

 3. BeautifulSoup
```python
pip install beautifulsoup4
```
 4. Scikit-Learn
```python
pip install scikit-learn
```
 5. Selenium
```python
pip install selenium
```
After installing selenium you need to download its Chrome WebDriver which can be downloaded from:
http://chromedriver.chromium.org/downloads
Choose appropriate version of Chrome Driver according to the version of your google chrome browser. 
You need to add the downloaded ChromeDriver EXE to your PATH variable. 

Thats all for dependencies.

# Usage

usage: similarityscript.py [-h] [-i INPUTFILE] [-s SHEET] [-o OUTPUTFILE]

optional arguments: <br/> -h, --help show this help message and exit <br/> -i INPUTFILE, --inputfile INPUTFILE <br/> Specify the input xlsx file path. E.g. C:\user\downloads\Excel.xlsx <br/> -s SHEET, --sheet SHEET <br/> Specify the sheet name in xlsx file. E.g. Dataset1  <br/> -o OUTPUTFILE, --outputfile OUTPUTFILE <br/> Specify the directory you want to save output xlsx file. E.g. C:\user\downloads\

![](img/Example%20Usage.jpg)

<br/>
If no input file is specified then this script tries to find a file named "input.xlsx" in script's directory- The current directory. <br/>
If no sheet name is specified then "Dataset1" is considered as default sheet name of the input xlsx file. <br/>
If no output path is specified then the output file is placed in the same folder as the script. <br/>
<br/>

###### Example input and output XLSX files have been added along with python script. <br/> This Script has been been tested on Windows 10 with Python 3.6.2 


