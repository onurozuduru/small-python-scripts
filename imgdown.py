#!/usr/bin/python

from lxml import html
from datetime import datetime
import sys, getopt
import os
import requests


def get_src_list(url, img_class=None):
    page = requests.get(url)
    tree = html.fromstring(page.text)
    xpath = "//img/@src"
    if img_class:
        xpath = "//img[@class='" + img_class + "']/@src"
    src_list = tree.xpath(xpath)
    src_list = ["https:" + src for src in src_list]
    return src_list


def save_files(src_list, filename=None):
    dir_name = "images/" + datetime.now().strftime("%Y-%m-%d-%H:%M:%S")
    os.makedirs(dir_name)
    for ind, src in enumerate(src_list):
        img = requests.get(src, stream=True)
        fn = str.split(src, "/")[-1]
        if filename:
            fn = filename + str(ind) + "." + fn.split(".")[-1]
        file = os.path.join(dir_name, fn)
        with open(file, 'wb') as f:
            for c in img.iter_content(512):
                f.write(c)


def usage():
    print "imgdown.py [-h] [-c class] [-f filename] <url>"


# if __name__ == '__main__':
#     url = "https://tr.wikipedia.org/wiki/Trigonometrik_d%C3%B6n%C3%BC%C5%9F%C3%BCm_form%C3%BClleri"
#     img_class = "mwe-math-fallback-image-inline tex"
#     save_files(get_src_list(url, img_class), "tri")


def main(argv):
    img_class = None
    filename = None
    url = argv[-1]
    try:
        opts, args = getopt.getopt(argv,"hc:f:",["class=","filename="])
    except getopt.GetoptError:
        usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            usage()
            sys.exit()
        elif opt in ("-c", "--class"):
            img_class = arg
        elif opt in ("-f", "--filename"):
            filename = arg
    save_files(get_src_list(url, img_class), filename)

if __name__ == "__main__":
	if len(sys.argv) == 1:
		usage()
		sys.exit(2)
	main(sys.argv[1:])
