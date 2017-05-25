# encoding=utf-8

import itchat
from itchat.content import *

# from telegram import send_msg

# CHAT_ID = "252227225"
chat_id = None
tele = None

@itchat.msg_register([TEXT, MAP, CARD, NOTE, SHARING])
def text_reply(msg):
    # for key, value in msg.items():
    #     print key, value
    # itchat.send("Sender:"+msg.user+"\nrecieved:" + msg.text, toUserName="fsd_vip")
    text = "sender: %s\nmsg: %s" % (msg.user.nickName, msg.text)
    tele.send_msg(chat_id, text)
    """用户为自己"""
    if msg['FromUserName'] == itchat.originInstance.storageClass.userName:
        return

    itchat.send("sender: %s\n" % msg.user.nickName +
                "msg: %s" % msg.text,
                toUserName="fsd_vip")

    # itchat.send("@img@170430-014847.png")


@itchat.msg_register([PICTURE, RECORDING, ATTACHMENT, VIDEO])
def download_files(msg):
    # if msg['FromUserName'] == itchat.originInstance.storageClass.userName:
    #     return
    # msg.download(msg.fileName)
    itchat.send("sender: %s\n" % msg.user.nickName +
                "type: %s" % msg.type,
                toUserName="fsd_vip")
    itchat.send('@%s@%s' % ('img' if msg['Type'] == 'Picture' else 'fil', msg['FileName']),
                toUserName="fsd_vip")
    text = "sender: %s\n" % msg.user.nickName
    tele.send_msg(chat_id, text)
    tele.send_photo(chat_id, msg['Text']())
    # return '%s received' % msg['Type']


@itchat.msg_register([TEXT, MAP, CARD, NOTE, SHARING], isGroupChat=True)
def text_reply(msg):
    # if msg.isAt:
    if True:
        # msg.user.send(u'@%s\u2005I received: %s' % (
        #     msg.actualNickName, msg.text))
        """
        msg.user.nickName: 群名
        msg.actualNickName: 人名
        """
        itchat.send("sender: %s[%s]\n" % (msg.user.nickName, msg.actualNickName) +
                    "msg: %s" % msg.text,
                    toUserName="fsd_vip")

        text = "sender: %s[%s]\nmsg: %s" % (msg.user.nickName, msg.actualNickName, msg.text)
        tele.send_msg(chat_id, text)


@itchat.msg_register([PICTURE, RECORDING, ATTACHMENT, VIDEO], isGroupChat=True)
def download_files(msg):
    # msg.download(msg.fileName)
    itchat.send("sender: %s[%s]\n" % (msg.user.nickName, msg.actualNickName) +
                "type: %s" % msg.type,
                toUserName="fsd_vip")
    itchat.send('@%s@%s' % ('img' if msg['Type'] == 'Picture' else 'fil', msg['FileName']),
                toUserName="fsd_vip")

    text = "sender: %s[%s]" % (msg.user.nickName, msg.actualNickName)
    tele.send_msg(chat_id, text)
    tele.send_photo(chat_id, msg['Text']())


def set_tele_instance(instance):
    global tele
    tele = instance

# itchat.auto_login()
# itchat.send("hello", toUserName='filehelper')
# itchat.send("hello", toUserName='fsd_vip')
# itchat.run()


def run(cid):
    global tele
    global chat_id
    chat_id = cid

    def send_QR(uuid, status, qrcode):
        tele.send_photo(chat_id, qrcode)

    if tele:
        itchat.auto_login(qrCallback=send_QR)
        itchat.run()
