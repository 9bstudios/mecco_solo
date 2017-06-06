# python

import lx, lxifc, lxu, solo

class MySceneListener(lxifc.SceneItemListener):
    def __init__(self):
        self.COM_object = lx.object.Unknown(self)
        self.lis_svc = lx.service.Listener()
        self.lis_svc.AddListener(self.COM_object)

    def __del__(self):
        self.lis_svc.RemoveListener(self.COM_object)

    def notify(self):
        solo.queue_idle_visitor(solo.solo_set_status)

    ''' Listener Method Overrides '''
    def sil_SceneCreate(self, scene):
        self.notify()

    def sil_SceneDestroy(self, scene):
        self.notify()

    def sil_SceneClear(self, scene):
        self.notify()

MySceneListener()
