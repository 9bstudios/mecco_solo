# python

import lx
from Notifier import Notifier
from MyOnIdleVisitor import MyOnIdleVisitor


def solo_set_status(value = None):

    if value is not None:
        lx.eval('user.value solo_is_active %s' % int(value))

    elif lx.eval('layer.setReference ?') == "":
        lx.eval('user.value solo_is_active 0')

    else:
        lx.eval('user.value solo_is_active 1')

    notifier = Notifier()
    notifier.Notify(lx.symbol.fCMDNOTIFY_CHANGE_ALL)


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
