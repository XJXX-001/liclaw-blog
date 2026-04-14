#!/usr/bin/env python3
"""
热门资讯爬虫
每天获取 Hacker News + Indie Hackers 热门内容，翻译后推送到飞书
"""

import requests
import json
from datetime import datetime
from deep_translator import GoogleTranslator
from bs4 import BeautifulSoup

# 飞书 Webhook（用户需要替换为真实 URL）
FEISHU_WEBHOOK = "https://open.feishu.cn/open-apis/bot/v2/hook/e50ccac9-89c9-41d8-bb93-b76088a7fd7f"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}


def get_hackernews_top(limit=10):
    """
    获取 Hacker News 热门帖子
    
    Returns:
        list: [{title, url, score}]
    """
    try:
        resp = requests.get("https://news.ycombinator.com/", headers=HEADERS, timeout=15)
        soup = BeautifulSoup(resp.text, "html.parser")
        items = soup.find_all("tr", class_="athing")
        
        posts = []
        for item in items[:limit]:
            title_elem = item.find("a", class_="storylink")
            if not title_elem:
                title_elem = item.find("span", class_="titleline")
            
            title = title_elem.text.strip() if title_elem else ""
            url = title_elem.get("href", "") if title_elem else ""
            
            # Score in next tr
            score_elem = item.find_next_sibling("tr")
            if score_elem:
                score_tag = score_elem.find("span", class_="score")
                score_text = score_tag.text.strip() if score_tag else "0"
                score = int(score_text.replace(" points", "").replace(",", "")) if score_text else 0
            else:
                score = 0
            
            if title:
                posts.append({"title": title, "url": url, "score": score})
        
        return posts
        
    except Exception as e:
        print(f"Hacker News 获取失败: {e}")
        return []


def get_indiehackers_top(limit=10):
    """
    获取 Indie Hackers 热门帖子
    
    Returns:
        list: [{title, url, score}]
    """
    try:
        resp = requests.get("https://www.indiehackers.com/", headers=HEADERS, timeout=15)
        soup = BeautifulSoup(resp.text, "html.parser")
        
        posts = []
        
        # 按 class 找 story 链接
        stories = soup.find_all("a", class_="story__text-link")
        
        for story in stories[:limit]:
            title = story.text.strip()
            if not title or len(title) < 10:
                continue
            
            href = story.get("href", "")
            if not href:
                continue
            
            # 完整 URL
            url = "https://www.indiehackers.com" + href if href.startswith("/") else href
            
            # 找评论数/票数
            parent = story.parent
            score = 0
            if parent:
                stats = parent.find_all(["span", "p"])
                for s in stats:
                    try:
                        num = int("".join(filter(str.isdigit, s.text)))
                        score = max(score, num)
                    except:
                        pass
            
            posts.append({"title": title, "url": url, "score": score})
        
        return posts
        
    except Exception as e:
        print(f"Indie Hackers 获取失败: {e}")
        return []


def translate_to_chinese(text, max_length=500):
    """
    将英文翻译成中文
    """
    if not text:
        return ""
    
    text = text[:max_length]
    
    try:
        translator = GoogleTranslator(source="en", target="zh-CN")
        result = translator.translate(text)
        return result if result else text
    except Exception as e:
        print(f"翻译失败: {e}")
        return text


def send_to_feishu(posts_by_source):
    """
    发送消息到飞书
    
    Args:
        posts_by_source: {"HN": [{title, url, score}], "IH": [{title, url, score}]}
    """
    today = datetime.now().strftime("%Y-%m-%d")
    
    lines = [f"📮 每日热门资讯（{today}）\n"]
    
    # Hacker News
    hn_posts = posts_by_source.get("HN", [])
    if hn_posts:
        lines.append("\n🔷 Hacker News TOP 10")
        for i, post in enumerate(hn_posts, 1):
            title = post.get("translated_title", post.get("title", ""))
            url = post.get("url", "")
            score = post.get("score", 0)
            lines.append(f"\n{i}. 【{title}】")
            lines.append(f"   🔗 {url}")
            lines.append(f"   ⬆️ {score} 票")
    
    # Indie Hackers
    ih_posts = posts_by_source.get("IH", [])
    if ih_posts:
        lines.append("\n\n🔶 Indie Hackers TOP 10")
        for i, post in enumerate(ih_posts, 1):
            title = post.get("translated_title", post.get("title", ""))
            url = post.get("url", "")
            score = post.get("score", 0)
            lines.append(f"\n{i}. 【{title}】")
            lines.append(f"   🔗 {url}")
            lines.append(f"   ⬆️ {score}")
    
    content = "\n".join(lines)
    
    payload = {
        "msg_type": "text",
        "content": {
            "text": content
        }
    }
    
    try:
        response = requests.post(FEISHU_WEBHOOK, json=payload, timeout=10)
        return {"success": True, "result": response.json()}
    except Exception as e:
        return {"success": False, "error": str(e)}


def main():
    print(f"[{datetime.now()}] 开始获取热门资讯...")
    
    posts_by_source = {}
    
    # Hacker News
    print("\n📰 获取 Hacker News...")
    hn_posts = get_hackernews_top(10)
    print(f"获取到 {len(hn_posts)} 条")
    posts_by_source["HN"] = hn_posts
    
    # Indie Hackers
    print("\n📰 获取 Indie Hackers...")
    ih_posts = get_indiehackers_top(10)
    print(f"获取到 {len(ih_posts)} 条")
    posts_by_source["IH"] = ih_posts
    
    # 翻译
    print("\n🌐 翻译标题...")
    all_posts = list(posts_by_source.items())
    for source, posts in all_posts:
        for post in posts:
            print(f"  翻译 [{source}]: {post['title'][:40]}...")
            translated = translate_to_chinese(post["title"])
            post["translated_title"] = translated
    
    # 推送
    print("\n📱 推送到飞书...")
    result = send_to_feishu(posts_by_source)
    
    if result.get("success"):
        print("✅ 推送成功！")
    else:
        print(f"❌ 推送失败: {result.get('error')}")


if __name__ == "__main__":
    main()
