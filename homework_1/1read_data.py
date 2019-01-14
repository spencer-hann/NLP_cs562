import sys
import gzip
from lxml import etree

def create_tree_list(data):
    parser = etree.XMLParser(remove_blank_text=True)
    tree_list = [etree.XML(doc, parser) for doc in data]

    # trim tree
    for tree in tree_list:
        for item in tree.iter("*"):
            if item.text is None: continue
            item.text = item.text.strip()
            if not item.text: # is empty
                item.text = None

    return tree_list

if __name__ == "__main__":
    if len(sys.argv) > 1:
        data = list(map(gzip.open, sys.argv[1:]))
        data = [f.read() for f in data]
        tree_list = create_tree_list(data)

        for tree in tree_list:
            for p in tree.iter("P"):
                if p.text:
                    print(p.text)
    else:
        print("ERROR: must include list of .xml.gz files as arg")
