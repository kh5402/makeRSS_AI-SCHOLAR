import requests
import re
import xml.etree.ElementTree as ET
from xml.dom import minidom
import os

def main():
    output_file = "makeRSS_AI-SCHOLAR.xml"
    base_url = "https://ai-scholar.tech/"

    # 既存のRSSフィードを読み込む
    existing_links = set()
    if os.path.exists(output_file):
        tree = ET.parse(output_file)
        root = tree.getroot()
        for item in root.findall(".//item/link"):
            existing_links.add(item.text)
    else:
        root = ET.Element("rss", version="2.0")
        channel = ET.SubElement(root, "channel")
        title = "AI-SCHOLARからの情報"
        description = "AI-SCHOLARからの情報を提供します。"
        ET.SubElement(channel, "title").text = title
        ET.SubElement(channel, "description").text = description
        ET.SubElement(channel, "link").text = "https://example.com"

    response = requests.get(base_url)
    html_content = response.text

    article_pattern = re.compile(r'<a class="list-item__link" href="([^"]+)">.*?<h3 class="list-item__title is__pc">([^<]+)<\/h3>.*?<time class="updated entry-time list-item__date list-item__date--time" datetime="([^"]+)">([^<]+)<\/time>')
    channel = root.find("channel")

    for match in article_pattern.findall(html_content):
        link, title, datetime, date = match

        # 既存のリンクならスキップ
        if link in existing_links:
            continue

        new_item = ET.SubElement(channel, "item")
        ET.SubElement(new_item, "title").text = title
        ET.SubElement(new_item, "link").text = link
        ET.SubElement(new_item, "pubDate").text = datetime

    xml_str = ET.tostring(root)
    xml_pretty_str = minidom.parseString(xml_str).toprettyxml(indent="  ")

    with open(output_file, "w") as f:
        f.write(xml_pretty_str)

if __name__ == "__main__":
    main()
