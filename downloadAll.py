#!/usr/bin/python

from lxml import html
from lxml.html import builder
from datetime import datetime
import sys, getopt
import os
import requests


HTTP = "http://"
HTTPS = "https://"
CLASS_NAME = "formulas"
X_IMG = "//img"
X_SRC = "@src"
X_ALT = "@alt"
X_STR_TITLE = "string(//title)"


# Splits URL into parts,
# Returns list of strings that first element is the domain.
def split_url(url):
	# Delete protocol parts if there's any.
	url = url.replace(HTTP, "")
	url = url.replace(HTTPS, "")
	return url.split("/")


def gen_base_img_url(url_parts):
	if url_parts:
		base_url = ""
		for p in url_parts[:-1]:
			base_url = base_url + p + "/"
		return base_url
	return None


def gen_page_tree(url):
	page = requests.get(url)
	return html.fromstring(page.text)


def gen_dir_name(tree):
	if tree is not None and tree.xpath(X_STR_TITLE):
		name = tree.xpath(X_STR_TITLE).replace(".", "_")
		if os.path.isdir(name):
			return name + datetime.now().strftime("%Y-%m-%d-%H:%M:%S")
		return name
	return datetime.now().strftime("%Y-%m-%d-%H:%M:%S")

# Returns list of dict with keys "src" and "alt"
def get_src_and_alt_list(tree):
	all_images = tree.xpath(X_IMG)
	img_list = [{"src": i.xpath(X_SRC)[0], "alt": i.xpath(X_ALT)[0].replace("\n", "")} \
		for i in all_images if i.xpath(X_ALT)] # Take images which are only have "alt."
	return img_list


def download_images(img_list, base_url, tree):
	dir_name = gen_dir_name(tree)
	os.makedirs(dir_name)
	dwn_img_list = []
	for ind, d in enumerate(img_list):
		filename = str(ind) + "." + d["src"].split(".")[-1]
		src = HTTP + base_url + d["src"]
		alt = d["alt"]
		
		img = requests.get(src, stream=True)
		filepath = os.path.join(dir_name, filename)
		
		with open(filepath, 'wb') as f:
			for c in img.iter_content(512):
				f.write(c)
		dwn_img_list.append({"src": filename, "alt": alt})
	return dir_name, dwn_img_list


def gen_html_tree(img_list, title=""):
	body = builder.BODY()
	for d in img_list:
		body.append(builder.P(builder.IMG(builder.CLASS(CLASS_NAME), src=d["src"], alt=d["alt"])))
	return builder.HTML(builder.TITLE(title), body)
	
	
def save_html_file(dir_name, filename, html_tree):
	if not os.path.isdir(dir_name):
		os.makedirs(dir_name)
	filepath = os.path.join(dir_name, filename + ".html")
	
	with open(filepath, 'w') as f:
		f.write("<!DOCTYPE html>\n" + html.tostring(html_tree, pretty_print=True))


def download(url):
	if not url:
		return
	print "URL: %s\n-----------------------------" % url
	url_parts = split_url(url)
	base_url = gen_base_img_url(url_parts)
	print "Generating page tree..."
	tree = gen_page_tree(url)
	print "Page tree is generated."
	print "Downloading images..."
	dir_name, img_list = download_images(get_src_and_alt_list(tree), base_url, tree)
	print "Images are downloaded."
	print "Generating html..."
	html_tree = gen_html_tree(img_list, dir_name)
	print "Html is generated."
	print "Saving html file..."
	save_html_file(dir_name, dir_name, html_tree)
	print "Html file is saved as %s" % dir_name + ".html\n-----------------------------"


def read_source_list(fn):
	with open(fn, "r") as f:
		text = f.read()
	return text.split("\n")


if __name__ == "__main__":
	args = sys.argv
	if len(args) == 1:
		url = "http://www.sosmath.com/trig/Trig5/trig5/trig5.html"
		download(url)
	else:
		source_list = read_source_list(args[-1])
		for url in source_list:
			download(url)
	print "I worked a lot,\nGoodbye!"
