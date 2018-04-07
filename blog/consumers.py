from cahnnel import group
def ws_message(message):
    Group('users').add(message.reply_channel)
def ws_disconnect(message):
    Group('users').discard(message.reply_channel)
