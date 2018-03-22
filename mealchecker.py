import requests
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET

tree = ET.parse("config.xml")
root = tree.getroot()
username = root.find("username").text
password = root.find("password").text
key = root.find("key").text

with requests.Session() as s:
	main = s.get("https://ecas.millersville.edu/cas/login?service=https%3A%2F%2Fcbordweb.millersville.edu%2Flogin%2Fcas.php")
	soup = BeautifulSoup(main.text, "lxml")
	d = {e["name"]: e.get("value", "") for e in soup.find_all("input", {"name": True})}
	d["username"] = username
	d["password"] = password
	p = s.post("https://ecas.millersville.edu/cas/login?service=https%3A%2F%2Fcbordweb.millersville.edu%2Flogin%2Fcas.php", data = d, verify = False)
	soup = BeautifulSoup(s.get("https://cbordweb.millersville.edu/student/welcome.php").text, "lxml")
	tds = soup.find_all("td", attrs = {"colspan": "2"})
	tdrs = soup.find_all("td", attrs = {"align": "right"})
	print("Notifying.")
	requests.post(key, data = {"value1" : tds[1].text, "value2" : tdrs[0].text})