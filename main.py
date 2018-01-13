import pubmed
import sys
import freegoogletranslator
import send_livemail

titlelist = []
abstractlist = []
contentslist = []
urllist = []

print("Pubmedで検索したいキーワードを入力してください")
word = input(">>")
word = word.strip()

fpath = "body.txt"

titleids = pubmed.get_pmid(word)
titlenumbers = len(titleids)
pubmed.initiate_body(fpath,word,titlenumbers)

if len(titleids) == 0:
    print("対象のキーワードに関連する記事が見つかりませんでした")
    sys.exit()
else:
    for titleid in titleids:
        contents = pubmed.get_abstract(titleid)
        titlelist.append(contents[0])
        abstractlist.append(contents[1])
        urllist.append(contents[2])

contentslist = [titlelist,abstractlist,urllist]
pubmed.write_body(fpath,word,contentslist,titlenumbers)

# send_livemail.sendmail(word)

print("プロセスが完了しました")
