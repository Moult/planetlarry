import requests
import xml.etree.ElementTree as ET
from datetime import datetime

blogs = {
    "https://thinkmoult.com/feed.atom",
    "https://fitzcarraldoblog.wordpress.com/feed/atom",
}

feed = ET.Element("feed", xmlns="http://www.w3.org/2005/Atom")
ET.SubElement(feed, "title").text = "Planet Larry"
ET.SubElement(feed, "link", href="https://planetlarry.org")
ET.SubElement(feed, "updated").text = datetime.now().isoformat(timespec="seconds".replace(" ", "T", 1))
author = ET.SubElement(feed, "author")
ET.SubElement(author, "name").text = "Larry the Cow"
ET.SubElement(feed, "id").text = "https://planetlarry.org/"

entries = []
updated_timestamps = []

for blog in blogs:
    response = requests.get(blog["url"])

    root = ET.fromstring(response.text)
    ns = {"ns": root.tag.split("{")[1].split("}")[0]}
    for entry in root.findall("ns:entry", ns):
        entries.append(entry)
        updated_timestamps.append(entry.find("ns:updated", ns).text)

# Sort entries by date
# https://stackoverflow.com/questions/6618515/sorting-list-according-to-corresponding-values-from-a-parallel-list
entries = [x for _, x in sorted(zip(updated_timestamps, entries), key=lambda pair: pair[0], reverse=True)]

for entry in entries[0:50]:
    feed.append(entry)

tree = ET.ElementTree(feed)
for elem in tree.iter():
    if elem.tag.startswith("{"):
        elem.tag = elem.tag.split("}", 1)[1]

print(ET.tostring(feed, encoding="utf-8").decode("utf-8"))
with open("feed.atom", "wb") as f:
    tree.write(f)
