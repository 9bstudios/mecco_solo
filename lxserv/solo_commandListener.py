# python

import lxifc, modo, lx
import solo
svc_listen = lx.service.Listener()

class CmdListener(lxifc.CmdSysListener):
    def __init__(self):
        svc_listen.AddListener(self)
        self.armed = True

    def cmdsysevent_ExecutePre(self,cmd,type,isSandboxed,isPostCmd):
        if self.armed:
            cmd = lx.object.Command(cmd)

            if cmd.Name() in ("scene.set", "item.refSystem", "layer.setReference", "layer.referenceSelected"):
                solo.queue_idle_visitor(solo.solo_set_status)

    def cmdsysevent_RefireBegin(self):
        self.armed = False

    def cmdsysevent_RefireEnd(self):
        self.armed = True

CmdListener()
