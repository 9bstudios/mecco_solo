#!/usr/bin/env python

import lx
import lxifc
import lxu
import modo
import lxu.command
import traceback
import solo

def get_mode():
    """Returns the current selection mode as any of the following strings:
    vertex;edge;polygon;item;pivot;center;ptag
    """

    modes = 'vertex;edge;polygon;item;pivot;center;ptag'
    for mode in modes.split(';'):
        if lx.eval('select.typeFrom %s;%s ?' % (mode, modes)):
            return mode
    return False

class solo_toggle(solo.CommanderClass):

    def commander_arguments(self):
        return [
            {
                'name': 'active',
                'datatype': 'boolean',
                'flags': ['query', 'optional']
            }
        ]


    def commander_execute(self, msg, flags):

        # save current selection for later
        restore_mode = get_mode()
        restore_sel = modo.Scene().selected

        # change to item mode, drop selection, and select implicit_selection()
        lx.eval('select.typeFrom item true')
        lx.eval('select.drop item')
        for item in solo.implicit_selection():
            item.select()

        # do the magic
        if self.commander_arg_value(0) is not None:
            solo_is_active = not self.commander_arg_value(0)
        else:
            solo_is_active = lx.eval('user.value solo_is_active ?')

        if solo_is_active == 'false':
            try:
                lx.eval('hide.unsel')
                lx.eval('item.refSystem')
                lx.eval('user.value solo_is_active 1')
            except Exception:
                lx.out(traceback.format_exc())
        else:
            try:
                lx.eval('unhide')
                lx.eval('item.refSystem {}')
                lx.eval('user.value solo_is_active 0')
            except Exception:
                lx.eval('unhide')
                lx.out(traceback.format_exc())

        # restore selection
        lx.eval('select.drop item')
        for item in restore_sel:
            item.select()
        lx.eval('select.typeFrom %s true' % restore_mode)

        notifier = solo.Notifier()
        notifier.Notify(lx.symbol.fCMDNOTIFY_DATATYPE)

    def commander_query(self,index):
        if index == 0:
            if lx.eval('user.value solo_is_active ?') in ('true', 1, True):
                return True
            else:
                return False

    def basic_Enable(self,msg):
        if lx.eval('user.value solo_is_active ?'):
            return True
        elif solo.implicit_selection():
            return True
        else:
            return False

    def commander_notifiers(self):
        return [("select.event", "item +ldt"), ("solo.notifier", "")]


lx.bless(solo_toggle, "solo.toggle")
