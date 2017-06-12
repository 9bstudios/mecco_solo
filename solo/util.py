# python

import lx, lxu
from Notifier import Notifier
from MyOnIdleVisitor import MyOnIdleVisitor

HIDDEN_GROUP_NAME = "solo_hidden"

def queue_idle_visitor(todo_function, *args, **kwargs):

    visitor = MyOnIdleVisitor(todo_function, *args, **kwargs)

    if visitor.arm():
        pfm_svc = lx.service.Platform()
        pfm_svc.DoWhenUserIsIdle(visitor, lx.symbol.fUSERIDLE_CMD_STACK_EMPTY)

def get_selection_mode():
    """Returns the current selection mode as any of the following strings:
    vertex;edge;polygon;item;pivot;center;ptag
    """

    modes = 'vertex;edge;polygon;item;pivot;center;ptag'
    for mode in modes.split(';'):
        if lx.eval('select.typeFrom %s;%s ?' % (mode, modes)):
            return mode
    return False
    
class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class SceneStatuses(object):
    __metaclass__ = Singleton
    
    def __init__(self):
        self.active_scenes = set()
        
    def any_solo_active_scene(self):
        return len(self.active_scenes) != 0
    
    def current_scene_is_solo_active(self):
        scene = lx.object.Scene(lxu.select.SceneSelection().current())
        return scene.__peekobj__() in self.active_scenes
        
    def set_current_scene_active(self, flag):
        scene = lx.object.Scene(lxu.select.SceneSelection().current())
        if flag:
            self.active_scenes.add(scene.__peekobj__())
        else:
            self.active_scenes.remove(scene.__peekobj__())
            
    def handle_scene_delete(self, scene):
        scene = lx.object.Scene(scene)
        try:
            self.active_scenes.remove(scene.__peekobj__())
        except:
            pass
            
    def handle_scene_create(self, scene):
        scene = lx.object.Scene(scene)
        try:
            group = scene.ItemLookup(HIDDEN_GROUP_NAME)
            self.active_scenes.add(scene.__peekobj__())
        except:
            pass
            