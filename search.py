from datetime import date
from logging import error, fatal
from nltk.util import pr
import wikipedia
from textblob import TextBlob
from typing import List

searchOptions = []
isSecondRequest = False
lang = ""

def Request(name: str) -> str:
    global searchOptions
    global isSecondRequest

    if isSecondRequest == False:
        return find_options_in_wikipedia(name)
    else:
        return find_info_in_wikipedia(name)

def find_options_in_wikipedia(name: str) -> str:
    global searchOptions
    global isSecondRequest
    global lang

    b = TextBlob(name)
    lang = b.detect_language()

    wikipedia.set_lang(lang)
    data = wikipedia.search(name)
    searchOptions = data
    if len(data) == 0:
        return "По данному запросу ничего не найдено."
    else:
        isSecondRequest = True

    return str(gat_string_with_search_find_options(data))

def gat_string_with_search_find_options(arr: List[str]) -> str:
    i = 1
    outpout = "Что именно вас интересует?\n\n"
    for s in arr:
        outpout += str(i) + " " + s + '\n\n'
        i += 1

    return outpout

def find_info_in_wikipedia(name: str) -> str:
    global searchOptions
    global isSecondRequest
    global lang

    isSecondRequest = False

    option = searchOptions[int(name) - 1]
    wikipedia.set_lang(lang)

    try: 
        data = wikipedia.page(option)
    except Exception as e:
        searchOptions = []
        i = 1
        out = "Что именно вас интересует?\n\n"
        for s in e.options:
            out += str(i) + " " + s + '\n\n'
            searchOptions.append(s)
            i += 1
        isSecondRequest = True
        return out
    
    outpout = "Вот, что мне удалось найти\n\n"
    outpout += data.content
    return outpout