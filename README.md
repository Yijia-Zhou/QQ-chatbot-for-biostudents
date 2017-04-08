# README

此 QQ 聊天机器人基于 Python 第三方库 [qqbot](https://github.com/pandolia/qqbot) 开发，运行于 Python 3.5, 主要使用 requests & beautifulsoup 包进行对 pubmed 检索结果的获取和解析，使用 feedparser 模块解析 rss 源获取新闻（于 sciencenews.py 模块中）。为避免短时间大量发送消息被封号而经常调用 time.sleep