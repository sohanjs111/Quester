"""
Created on Sat Jul  9 13:32:16 2022

@author: sohanjs, Mahdjoubi Bilal
"""

import openai
import wget
import pathlib
import glob
import re

from PyPDF2 import PdfFileReader

files = glob.glob("*.pdf")
CHARACTER_LIMIT = 3000
openai.api_key = "YOUR_API_KEY"


def getPaper(paper_url, filename="espelage2016 (1).pdf"):
    """
    Downloads a paper from it's arxiv page and returns
    the local path to that file.
    """
    downloadedPaper = wget.download(paper_url, filename)
    downloadedPaperFilePath = pathlib.Path(downloadedPaper)

    return downloadedPaperFilePath


paperFilePath = "espelage2016 (1).pdf"
paperContent = PdfFileReader(paperFilePath)


def displayPaperContent(paperContent, page_start=0, page_end=5):
    for page in paperContent[page_start:page_end]:
        print(page.extract_text())


# displayPaperContent(paperContent)


def showPaperSummary(paperContent):
    tldr_tag = "\n Tl;dr"
    text = ""

    numberPages = paperContent.pages
    ##Loop through all the pages of the paper and concatenate the text
    for page in numberPages:
        text += page.extract_text()

    print("The full text of the paper is : ", text)
    try:
        textBegin = re.search("[\s\S]*?(?=INTRODUCTION|INTRODUCTIONS)", text).group()
    except AttributeError:
        textBegin = re.search("[\s\S]*?(?=INTRODUCTION|INTRODUCTIONS)", text)
    print("The text before Introduction is : ", textBegin)
    #select the text after the conclusion
    try:
        textEnd = re.search("(?=CONCLUSION\n|CONCLUSIONS\n)[\s\S]*", text).group()
    except AttributeError:
        textEnd = re.search("(?=CONCLUSION\n|CONCLUSIONS\n)[\s\S]*", text)
    print("The text after Conclusion is : ", textEnd)
    if textBegin is not None and textEnd is not None:
        text = textBegin + textEnd
    if text is not None:        
        text = cut(text)
        text += tldr_tag
    print("The AI will summarize the text below:", text)
    response = openai.Completion.create(model="text-davinci-002",
                                        prompt=text,
                                        temperature=0,
                                        max_tokens=300,
                                        top_p=1,
                                        frequency_penalty=0,
                                        presence_penalty=0
                                        )
    print("The response is:")
    print(response["choices"][0]["text"])


def cut(text):
    ##Make sure the numbers of characters in text is under or equals 5727
    ###If it is, then we return the text
    ###If it is not, then we cut the text and return the text
    if len(text) <= CHARACTER_LIMIT:
        print("Length text : , good", len(text))
        return text
    else:
        print("Length text : , bad", len(text))
        return text[:CHARACTER_LIMIT]


paperContent = PdfFileReader(paperFilePath)
showPaperSummary(paperContent)
