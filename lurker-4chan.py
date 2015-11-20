#!/usr/bin/python

import sys
import os
import requests
import urllib.request

def main(url):
    """Downloads all images from a thread on 4chan.

    Keyword arguments:
    args -- valid URL to thread

    Returns: None
    """
    elems = url.split("/")
    if elems[0].lower().startswith("http"):
        # case http://boards.4chan.org/BOARD/thread/THREAD/TITLE
        board = elems[3].lower()
        thread = elems[5]
    else:
        # case boards.4chan.org/BOARD/thread/THREAD/TITLE
        board = elems[1].lower()
        thread = elems[3]

    jsonurl = "http://api.4chan.org/{}/res/{}.json".format(board, thread)
    dst = os.path.join("4chan", board, thread)

    try:
        r = requests.get(jsonurl)
        res = r.json()
    except Exception as e:
        print(e)

    total = sum(1 for post in res["posts"] if "filename" in post and not "filedeleted" in post)
    if total > 0:
        if not os.path.exists(dst):
            os.makedirs(dst)

    print("Found {} images!".format(total))
    print("Downloading...")
    current = 1
    for post in res["posts"]:
        if "filename" in post and not "filedeleted" in post:
            file_name = "{}{}".format(post["tim"], post["ext"])
            file_url = "http://i.4cdn.org/{}/{}".format(board, file_name)
            file_path = os.path.join(dst, file_name)
            if not os.path.exists(file_path):
                u = urllib.request.urlopen(file_url)
                f = open(dst + "\\" + file_name, "wb")
                file_size = int(u.getheader('Content-Length'))
                file_size_dl = 0
                block_sz = 8192
                while True:
                    buffer = u.read(block_sz)
                    if not buffer:
                        break
                    file_size_dl += len(buffer)
                    f.write(buffer)
                    progress = int(file_size_dl * 100 / file_size)
                    print("\r\t [{}/{}]: \t {} \t => \t Downloading: {}%".format((str(current)).zfill(2), (str(total)).zfill(2), file_name, (str(progress)).zfill(3)), end = "")
                f.close()
                print('')
            else:
                print("\t [{}/{}]: \t {} \t => \t Duplicate".format((str(current)).zfill(2), (str(total)).zfill(2), file_name))
            current += 1
    print("...Done.")

if __name__ == "__main__":
    args = sys.argv
    if len(args) > 2:
        print("Usage: python {} (url to thread)".format(sys.argv[0]))
        sys.exit()
    elif len(args) == 2:
        main(args[1])
    else:
        print("Enter the url to the thread:")
        inp = input()
        main(inp)