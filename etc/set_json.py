
# -*- coding: utf-8 -*-

from flask import jsonify, json

# ????? ??? ???? ??? ??? ??
def set_json(send):
    if send:
        send = json.dumps(send, indent=4, ensure_ascii = False)

        for text in send:
            if ord(text) == 92:
                print(text)
                print(ord(text))
                send = send.replace(text, "")
                print("???")

        # send = send.replace("\\", "").replace("\n", "")

        return send
    else:
        return send
