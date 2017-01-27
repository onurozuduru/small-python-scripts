#!/usr/bin/python

from lxml import html
import requests
import argparse

PREFIX = """<!-- Codes From Github -->
<link rel="stylesheet" href="https://assets-cdn.github.com/assets/gist/embed-3313cb70789df61d3bb75cd878325a1266ccab50b6aac9b80f1691ae0694a216.css">
<div class="gist">
    <div class="gist-file">
"""
SUFFIX = """
    </div>
</div>
<!-- END OF CODE -->
"""
DTAB = "        "

def get_tree(url):
    page = requests.get(url)
    tree = html.fromstring(page.text)
    return tree.xpath("//div[@class='file']/div")[1]
    
def get_footer(url):
    raw_url = url.replace("blob", "raw")
    file_name = url.split("/")[-1]
    return """<div class="gist-meta">
            <a href="%s" style="float:right" target="_new">view raw</a>
            <a href="%s" target="_new">%s</a>
        hosted with &#10084; by <a href="https://github.com" target="_new">GitHub</a>
        </div>"""%(raw_url, url, file_name)

def convert_to_list(s):
    unique_vals = set()
    for val in s.split(","):
        if "-" in val:
            unique_vals |= set(map(str, range(*map(int, val.split("-")))))
        else:
            unique_vals.add(val)
    sorted_list = list(unique_vals)
    sorted_list.sort(key=int)
    return ["L"+v for v in sorted_list]

def select_lines(table_node, str_line_nums):
    new_table_node = html.fromstring("<table>\n</table>\n")
    parent = table_node.getparent()
    for el_id in convert_to_list(str_line_nums):
        try:
            new_table_node.append(table_node.get_element_by_id(el_id).getparent())
            if new_table_node.get_element_by_id(el_id.replace("L", "LC")).text == "\n":
                new_table_node.get_element_by_id(el_id.replace("L", "LC")).text = "";
        except:
            break
    parent.remove(table_node)
    parent.append(new_table_node)
    return parent

def create_code_embed(url, str_line_nums=None):
    tree = get_tree(url)
    if str_line_nums:
        select_lines(tree.xpath("//table")[0], str_line_nums)
    code = DTAB + html.tostring(tree).replace("\n","\n"+DTAB)
    footer = get_footer(url)
    return PREFIX + code + footer + SUFFIX

def save(code):
    with open("embed", "w") as f:
        f.write(code)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.epilog="Example usage: %s -l 3,7-10 'https://github.com/USER/REPO/FILE.cpp'"%parser.prog
    parser.add_argument("url", metavar="URL",
        help="Address of a github page where the code is placed. Example: 'https://github.com/USER/REPO/FILE.cpp'")
    parser.add_argument("-l", "--line-numbers",
        help="Specific line numbers that are divided by comma(,) and/or interval of numbers that are divided by dash(-) " +
        "last number is not included for intervals. Example: 1,2,6 (Only for lines 1, 2 and 3) OR 3-7 (For lines 3, 4, 5 and 6) " +
        "OR 3,7,10-12 (For lines 3, 7, 10 and 11)")
    args = parser.parse_args()
    print "Code embed is generating from %s..."%args.url
    save(create_code_embed(args.url, args.line_numbers))
    print "Code embed is generated and saved."
