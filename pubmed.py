import datetime
import os
import send_livemail
import freegoogletranslator
import requests
import lxml.html

def get_pmid(word):
    url = r"https://www.ncbi.nlm.nih.gov/pubmed/?term={}".format(word)
    req = requests.get(url)
    html = lxml.html.fromstring(req.content)
    title = html.xpath("//title/text()[normalize-space()]")
    if title.count("No items fond"):
        return None
    titleid = html.xpath("//dd/text()[normalize-space()]")
    return titleid

def get_abstract(id):
    try:
        url = r"https://www.ncbi.nlm.nih.gov/pubmed/{}".format(id)
        req = requests.get(url)
        html = lxml.html.fromstring(req.content)
        title = html.xpath("//div[@class='rprt abstract']/h1/text()[normalize-space()]")[0]
        jatitle = freegoogletranslator.googletranslate(title)
        print(jatitle)
        abstr = html.xpath("//div[@class='abstr']")[0]
        abstr_text = abstr.text_content()
        jaabstr_text = freegoogletranslator.googletranslate(abstr_text)
        contents = [jatitle,jaabstr_text,url]
        return contents
    except IndexError as e:
        print(e, ": {}は未完成の記事です".format(title))
        return "{}は未完成の記事です".format(title)

def initiate_body(fpath,word,titlenumbers):
    now = datetime.datetime.now()
    strnow = "{0:%Y年%m月%d日}".format(now)
    with open(fpath, "w") as f:
        f.writelines("{0}のPubmedから引用した『{1}』関連記事は{2}件ありました。\n\n".format(strnow,word,titlenumbers))

def write_body(fpath,word,contentslist,titlenumbers):
    try:
        with open(fpath, "a") as f:
            f.writelines("【本日の纏め】\n")
            for t in contentslist[0]:
                 f.writelines(t + "\n")
            f.writelines("\n================詳細=====================\n")
            for i in range(titlenumbers):
                f.writelines("\n" + contentslist[0][i] + "\n")
                f.writelines(contentslist[2][i] + "\n")
                f.writelines("\n" + contentslist[1][i] + "\n")
                f.writelines("\n=====================================\n")
    except TypeError as e:
        print(e, ": コンテンツが無い為入力をスキップします")
