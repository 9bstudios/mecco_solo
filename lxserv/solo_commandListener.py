# # python
#
# import lxifc, modo, lx
# svc_listen = lx.service.Listener()
#
# class CmdListener(lxifc.CmdSysListener):
#     def __init__(self):
#         svc_listen.AddListener(self)
#         self.armed = True
#
#     def cmdsysevent_ExecutePre(self,cmd,type,isSandboxed,isPostCmd):
#         if self.armed:
#             cmd = lx.object.Command(cmd)
#             # lx.out("'%s' will fire shortly" % cmd.Name())
#             if cmd.Name() in ("layer.setReference", "layer.referenceSelected"):
#                 if lx.eval('layer.setReference ?') == "":
#                     lx.eval('solo.toggle 0')
#                 else:
#                     lx.eval('solo.toggle 1')
#
#     def cmdsysevent_RefireBegin(self):
#         # we don't want a bunch of events when the user is
#         # dragging a minislider or something like that,
#         # so we disarm the listener on RefireBegin...
#         self.armed = False
#
#     def cmdsysevent_RefireEnd(self):
#         # ... and rearm on RefireEnd
#         self.armed = True
#
# cmdListener1 = CmdListener()
