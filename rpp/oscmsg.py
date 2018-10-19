"""Osc messages for the rust Osc server."""

import OSC


def new():
    msg = OSC.OSCMessage()
    msg.setAddress("/new")
    return msg

def set_render_id(rid):
    msg = OSC.OSCMessage()
    msg.setAddress("/render/render_id")
    msg.append(rid)
    return msg

def set_folder(folder):
    msg = OSC.OSCMessage()
    msg.setAddress("/render/folder")
    msg.append(folder)
    return msg

def set_filename(filename):
    msg = OSC.OSCMessage()
    msg.setAddress('/render/filename')
    msg.append(filename)
    return msg

def set_duration(duration):
    msg = OSC.OSCMessage()
    msg.setAddress("/render/duration")
    msg.append(duration)
    return msg
 
def set_wait(duration):
    msg = OSC.OSCMessage()
    msg.setAddress("/render/wait")
    msg.append(duration)
    return msg

def new_with_default_params():
    msg = OSC.OSCMessage()
    msg.setAddress("/topology/new_with_default_params")
    return msg

def new_with_current_params():
    msg = OSC.OSCMessage()
    msg.setAddress("/topology/new_with_current_params")
    return msg

def set_params(params, index=0):
    msg = OSC.OSCMessage()
    msg.setAddress("/topology/params")
    msg.append([index] + params)
    return msg

def render_static():
    msg = OSC.OSCMessage()
    msg.setAddress("/render/static")
    return msg

# def render_with_wait(c, s):
#     def foo(pat, tags, args, source): 
#         print "thanks rs!"
#         s.server.delMsgHandler('/{0}'.format(rid))
#
#     s.server.addMsgHandler("/{0}".format(rid), foo)
#     msg = OSC.OSCMessage()
#     msg.setAddress("/render/render")
#     c.send(msg)

# def set_id(c):
#     msg = OSC.OSCMessage()
#     msg.setAddress('/render/set_id')
#     msg.append(666)
#     c.send(msg)

if __name__ == "__main__":
    import time
    import pyserv
    import datetime

    a = datetime.datetime.now()
    rid = '{0}{1}{2}{3}{4}{5}{6}'.format(a.year, a.month, a.day, a.hour, a.minute, a.second, a.microsecond)
    s = pyserv.PyServer(('127.0.0.1', 57126), 666).start()
    c = OSC.OSCClient()
    c.connect(('127.0.0.1', 6667))

    test_new(c)
    time.sleep(0.1)

    test_set_render_id(c)
    test_set_foldername(c)
    test_set_filename(c)
    test_set_duration(c)
    test_set_wait(c)
    test_new_with_default_params(c)
    time.sleep(0.1)
    
    test_set_params(c, 0)
    test_set_params(c, 1)
    test_set_params(c, 2)
    test_set_params(c, 3)
    time.sleep(0.1)
    
    test_new_with_current_params(c)
    time.sleep(0.1)
    
    test_render(c)
    # # test_render_with_wait(c,s)
    time.sleep(2)
    s.stop()
    c.close()
