#!/usr/bin/env python

import lx
import lxifc
import lxu
import modo
import lxu.command
import traceback
import solo

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
        if self.commander_arg_value(0) is not None:
            solo_is_active = not self.commander_arg_value(0)
        else:
            solo_is_active = lx.eval('user.value solo_is_active ?')

        if not solo_is_active:
            try:
                lx.eval('hide.unsel')
                lx.eval('item.refSystem')
                lx.eval('user.value solo_is_active 1')
            except Exception:
                lx.out(traceback.format_exc())
                lx.eval('layout.createOrClose EventLog "Event Log_layout" title:@macros.layouts@EventLog@ width:600 height:600 persistent:true open:true')

        else:
            try:
                lx.eval('unhide')
                lx.eval('item.refSystem {}')
                lx.eval('user.value solo_is_active 0')
            except Exception:
                lx.eval('unhide')
                lx.out(traceback.format_exc())
                lx.eval('layout.createOrClose EventLog "Event Log_layout" title:@macros.layouts@EventLog@ width:600 height:600 persistent:true open:true')


    def commander_query(self,index):
        if index == 0:
            return lx.eval('user.value solo_is_active ?')

    def basic_Enable(self,msg):
        if lx.eval('user.value solo_is_active ?'):
            return True
        elif modo.Scene().selected:
            return True
        else:
            return False

lx.bless(solo_toggle, "solo.toggle")
