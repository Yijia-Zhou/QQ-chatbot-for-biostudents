'''
目前功能：
关键词 + @pubmed 可获得检索结果页面链接和前四条结果
数字1-3加 @keyanAI 可获得指定数量的生命科学相关新闻
论文标题 + @scihub 可获得 scihub 提供的下载链接
@keyanAI获得使用指南，想随便聊聊的话就用@chat结尾吧
'''
import random
import time
import urllib.parse
import requests
from bs4 import BeautifulSoup

from qqbot import QQBotSlot as qqbotslot, RunBot

import sciencenews

@qqbotslot
def onQQMessage(bot, contact, member, content):
    '''
    对 QQ 消息进行响应的主函数，各种聊天消息统一进行处理。
    '''
    content = content.strip()
    if content == '-stop':
        bot.SendTo(contact, 'QQ机器人已关闭')
        bot.Stop()

    elif content.endswith('@pubmed'):
        keyword = strQ2B(content[:-7])
        url = 'https://www.ncbi.nlm.nih.gov/pubmed/?term=' + keyword.strip().replace(' ', '+')
        bot.SendTo(contact, url)
        time.sleep(random.choice(range(3, 6)))

        pubmedresult = getPubmed(url)
        tosend = ''
        for result_index in range(4):
            try:
                tosend += next(pubmedresult)+'\n'
            except StopIteration:
                tosend += "That's all."
                break
        bot.SendTo(contact, tosend)

    elif content.endswith('@scihub'):
        keyword = strQ2B(content[:-7])
        bot.SendTo(contact, getScihub(keyword))

    elif content.endswith('@chat'):
        senten = urllib.parse.quote(strQ2B(content[:-5]))
        time.sleep(random.choice(range(3, 7)))
        try:
            response = requests.get('http://api.qingyunke.com/api.php?key=free&appid=0&msg=' + senten)
            bot.SendTo(contact, response.json()['content'])
        except Exception as e:
            bot.SendTo(contact, str(e))


    elif '@ME' in content or '@keyanAI' in content:
        try:
            firstDigit = content.strip('[@ME]').strip()[0]
        except IndexError:
            firstDigit = 'Nothing'
        if firstDigit in '123':
            news = sciencenews.db.get_science_news(int(firstDigit))
            for new in news:
                bot.SendTo(contact, new + '\n')
                time.sleep(random.choice(range(4, 11)))
        else:
            bot.SendTo(contact, '''你好，我是科研小 AI, 我目前的功能有：
关键词 + @pubmed 可获得检索结果页面链接和前四条结果
数字1-3开头并 @我 可获得指定数量的生命科学相关新闻
论文标题 + @scihub 可获得 scihub 提供的下载链接
@我获得使用指南，想随便聊聊的话就用@chat结尾吧O(∩_∩)O''')


# @qqbotslot
# def onNewContact(bot, contact, owner):
#     '''
#     # 当新增 好友/群/讨论组/群成员/讨论组成员 时被调用
#     # bot     : QQBot 对象
#     # contact : QContact 对象，代表新增的联系人
#     # owner   : QContact 对象，仅在新增 群成员/讨论组成员 时有效，代表新增成员所在的 群/讨论组
#     '''
#     print('New Contact: ' + str(owner))
#     bot.SendTo(contact, '''你好，我是科研小 AI, 我目前的功能有：
# 关键词 + @pubmed 可获得检索结果页面链接和前四条结果
# 数字1-3加 @keyanAI 可获得指定数量的生命科学相关新闻
# 论文标题 + @scihub 可获得 scihub 提供的下载链接
# @我获得使用指南，想随便聊聊的话就用@chat结尾吧O(∩_∩)O''')

def getPubmed(url):
    '''
    获取并解析 pubmed 检索结果，输入关键词，返回生成器。
    '''
    html = requests.get(url).text

    soup = BeautifulSoup(html, 'lxml')

    for c in soup.findAll('div'):
        if c.get('class') == ['rprt']:
            for p in c.findAll('p'):
                if p.get('class') == ['title']:
                    yield '%s\nhttps://www.ncbi.nlm.nih.gov%s\n' %(p.a.text, p.a.get('href'))

def getScihub(keyword):
    '''
    通过 keyword 查 PMID, 返回 scihub 提供的 'www.ncbi.nlm.nih.gov.sci-hub.cc/pubmed/' 下载链接，
    并读取 doi 号方便手动在 scihub 输入。
    '''
    # pubhuburl = 'http://www.ncbi.nlm.nih.gov.secure.sci-hub.cc/pubmed/' + PMID
    # respon = requests.get(pubhuburl)
    # if respon.url.startswith('http://www.ncbi.nlm.nih.gov.secure.sci-hub.cc/pubmed/'):
    #     try:
    #         return furtherScihub(respon)
    #     except:
    #         return furtherScihub(respon)
    # return pubhuburl
    url = 'https://www.ncbi.nlm.nih.gov/pubmed/?term=' + keyword.strip().replace(' ', '+')
    try:
        pub = next(getPubmed(url))
        PMID = pub.strip()[-8:]
    except StopIteration:
        h = requests.get(url)
        soup = BeautifulSoup(h.text, 'lxml')
        PMID = soup.findAll('dd')[-2].span.text
    
    pubhuburl = 'http://www.ncbi.nlm.nih.gov.sci-hub.cc/pubmed/' + PMID
    respon = requests.get('http://www.ncbi.nlm.nih.gov/pubmed/' + PMID)
    soup = BeautifulSoup(respon.text, 'lxml')
    doi = soup.findAll('dd')[-1].a.text
    return '{pubhuburl}\n如果点击此链接未成功下载 PDF, 请在 sci-hub.cc 中输入 {doi} 并点击右侧钥匙按钮。'.format(pubhuburl=pubhuburl, doi=doi)

# def furtherScihub(respon):
#     '''
#     Parse the pubmed@scihub html, get artical url with doi, return the scihub downloading url.
#     '''
    # soup = BeautifulSoup(respon.text, 'lxml')
    # doi = soup.findAll('dd')[-1].a.text
    # handle = requests.get('http://doi.org/api/handles/' + doi, timeout=15)
    # puburl = handle.json()['values'][0]['data']['value']
    # puburl = puburl[puburl.index('://')+3:]
    # scihuburl = puburl[:puburl.index('/')] + '.secure.sci-hub.cc' + puburl[puburl.index('/'):]
#     return scihuburl

def strQ2B(ustring):
    """全角转半角"""
    rstring = ""
    for uchar in ustring:
        inside_code = ord(uchar)
        if inside_code == 12288: #全角空格直接转换
            inside_code = 32
        elif inside_code >= 65281 and inside_code <= 65374: #全角字符（除空格）根据关系转化
            inside_code -= 65248

        rstring += chr(inside_code)
    return rstring


if __name__ == '__main__':
    RunBot()
