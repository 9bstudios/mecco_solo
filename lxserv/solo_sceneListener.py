# python

import lx, lxifc, lxu, solo

class MySceneListener(lxifc.SceneItemListener):
    def __init__(self):
        self.COM_object = lx.object.Unknown(self)
        self.lis_svc = lx.service.Listener()
        self.lis_svc.AddListener(self.COM_object)

    def __del__(self):
        self.lis_svc.RemoveListener(self.COM_object)

    ''' Listener Method Overrides '''
    def sil_SceneCreate(self, scene):
        sceneStatuses = solo.SceneStatuses()
        sceneStatuses.handle_scene_create(scene)
        notifier = solo.Notifier()
        notifier.Notify(lx.symbol.fCMDNOTIFY_DATATYPE)

    def sil_SceneDestroy(self, scene):
        sceneStatuses = solo.SceneStatuses()
        sceneStatuses.handle_scene_delete(scene)
        notifier = solo.Notifier()
        notifier.Notify(lx.symbol.fCMDNOTIFY_DATATYPE)

    def sil_SceneClear(self, scene):
        pass

MySceneListener()
