import fbchat
from fbchat import Client
from fbchat.models import *
import re

def login(fb_id, fb_pw):
    fbchat._util.USER_AGENTS = ["Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36"]
    fbchat._state.FB_DTSG_REGEX = re.compile(r'"name":"fb_dtsg","value":"(.*?)"')

    return Client(fb_id, fb_pw)

def send(fb_msg, cl):
    cl.send(Message(text=fb_msg), thread_id=cl.uid, thread_type=ThreadType.USER)