# 获取任然的词云
# 这里使用webdriver和switch_to_frame来获得html
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import jieba
from bs4 import BeautifulSoup
from selenium import webdriver
artist_id = "9255"  # 歌手id
artist_url = "https://music.163.com/#/artist?id=" + artist_id
browser = webdriver.Chrome()


def get_hotsong_id(artist_url):
    """
    获取artist_url下的前50首歌曲的歌词链接后缀，返回列表
    :param artist_id:
    :param headers:
    :return:
    """
    try:
        back_hrefs = []  # 存储每首歌的歌词链接后缀
        browser.get(artist_url)
        browser.implicitly_wait(10)
        iframe = browser.find_element_by_name("contentFrame")  # 定位iframe
        browser.switch_to.frame(iframe)  # 切换进iframe
        html = browser.page_source  # 得到iframe下的html界面
        soup = BeautifulSoup(html, "lxml")  # 解析
        spans = soup.find_all("span", attrs={"class": "txt"})
        for span in spans:
            a = span.find("a")
            back_hrefs.append(a["href"])
        return back_hrefs
    except Exception as e:
        print(e)


def get_lyrics(back_hrefs):
    """
    获取每首歌的歌词，连接成一个长字符串后返回
    :param back_hrefs:
    :param headers:
    :return:
    """
    url = "https://music.163.com/#"
    lyrics = ""
    for href in back_hrefs:
        lyric_url = url + href
        try:
            browser.get(lyric_url)
            browser.implicitly_wait(2)
            iframe = browser.find_element_by_name("contentFrame")
            browser.switch_to.frame(iframe)  # 切换进iframe
            html = browser.page_source
            soup = BeautifulSoup(html, "lxml")
            div = soup.find("div", attrs={"id": "lyric-content"})
            lyric = div.get_text()
            lyrics += lyric
            div = soup.find("div", attrs={"id": "flag_more"})
            lyric = div.get_text()
            lyrics += lyric
        except Exception as e:
            print("出错！", lyric_url, e)
    replace_words = ["作曲", "作词", "编曲", "缩混", "监制", "制作人", "吉他", "配唱制作人", "和声编写",
                   "和声", "录音室", "混音室", "任然", "Hot Music Studio"]
    for old in replace_words:
        lyrics = lyrics.replace(old, "")
    return lyrics


def get_cuttext(lyrics):
    """
    对歌词进行分词，返回分词后以空格连接的文本
    :param lyrics:
    :return:
    """
    cut_list = jieba.cut(lyrics)
    cuttext = " ".join(cut_list)
    return cuttext


def get_wordcloud(cuttext):
    """
    对分词后连接而成的长文本生成词云
    :param cuttext:
    :return:
    """
    wc = WordCloud(
        font_path="C:/Windows/Fonts/simhei.ttf",
        width=800,
        height=400
    )
    wordcloud = wc.generate(cuttext)
    return wordcloud


def show_wordcloud(wordcloud):
    """
    利用matplotlib.pyplot显示词云
    :param wordcloud:
    :return:
    """
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.show()


back_hrefs = get_hotsong_id(artist_url)
print(back_hrefs)
lyrics = get_lyrics(back_hrefs=back_hrefs)
print(lyrics)
text = get_cuttext(lyrics)
wordcloud = get_wordcloud(text)
wordcloud.to_file("renran.jpg")
show_wordcloud(wordcloud)
browser.close()
