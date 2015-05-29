#!/usr/bin/python

import sys
import os
import requests
import urllib.request

def main(args):
    """Downloads all images from a thread on 4chan.

    Keyword arguments:
    args -- valid URL to thread

    Returns: None
    """
    elems = args.split("/")
    # http://boards.4chan.org/_BOARD/thread/_THREAD/_TITLE
    if elems[0][0:4] == "http":
        board = elems[3]
        thread = elems[5]
    # boards.4chan.org/_BOARD/thread/_THREAD/_TITLE
    else:
        board = elems[1]
        thread = elems[2]

    jsonurl = "http://api.4chan.org/%s/res/%s.json" % (board, thread)
    path = "4chan"

    try:
        req = requests.get(jsonurl)
        res = req.json()
        dst = os.path.join(path, board, thread)
        total = 0
        for post in res["posts"]:
            if "filename" in post:
                total += 1
        current = 1
        for post in res['posts']:
            if "filename" in post:
                if "filedeleted" in post:
                    continue
                file_name = "%s%s" % (post["tim"], post["ext"])
                file_url = "http://i.4cdn.org/%s/%s" % (board, file_name)
                file_path = os.path.join(dst, file_name)
                if not os.path.exists(file_path):
                    if not os.path.exists(os.path.join(path, board, thread)):
                        os.makedirs(os.path.join(path, board, thread))
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
                        print("\rFile [%s/%s]: \t %s \t => \t Downloading: %s%%" % ((str(current)).zfill(2), (str(total)).zfill(2), file_name, (str(progress)).zfill(3)), end = "")
                    f.close()
                    print("")
                else:
                    print("File [%s/%s]: \t %s \t => \t Duplicate" % ((str(current)).zfill(2), (str(total)).zfill(2), file_name))
                current += 1
    except Exception as e:
        print(e)

if __name__ == "__main__":
    args = sys.argv
    if len(args) > 2:
        print("Usage: python %s (url to thread)" % (sys.argv[0]))
        sys.exit()
    elif len(args) == 2:
        main(args[1])
    else:
        print("Enter the url to the thread:")
        inp = input()
        main(inp)