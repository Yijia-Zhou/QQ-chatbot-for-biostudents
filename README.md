# README

此 QQ 聊天机器人基于 Python 第三方库 [qqbot](https://github.com/pandolia/qqbot) 开发，运行于 Python 3.5, 主要使用 requests & beautifulsoup 包进行对 pubmed 检索结果的获取和解析，使用 feedparser 模块解析 rss 源获取新闻（于 sciencenews.py 模块中）。为避免短时间大量发送消息被封号而经常调用 time.sleep

---

目前功能：
关键词 + @pubmed 可获得检索结果页面链接和前四条结果
数字1-3加 @keyanAI 可获得指定数量的生命科学相关新闻
论文标题 + @scihub 可获得 scihub 提供的下载链接
@keyanAI获得使用指南，想随便聊聊的话就用@chat结尾吧