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
                'name': 'mode',
                'datatype': 'string',
                'flags': ['optional']
            }, {
                'name': 'isActive',
                'datatype': 'boolean',
                'flags': ['query', 'optional']
            }
        ]


    def commander_execute(self, msg, flags):

        # See if the user value exists
        if lx.eval("query scriptsysservice userValue.isDefined ? solo") == 0:
            lx.eval( 'user.defNew solo boolean' );
            lx.eval( 'user.def solo username value:0' );

        solo_is_active = lx.eval('user.value solo ?')

        if solo_is_active == 0:
            try:
                lx.eval('hide.unsel')
                lx.eval('item.refSystem')
                lx.eval('user.value solo 1')
            except Exception:
                lx.out(traceback.format_exc())
                lx.eval('layout.createOrClose EventLog "Event Log_layout" title:@macros.layouts@EventLog@ width:600 height:600 persistent:true open:true')

        else:
            try:
                lx.eval('unhide')
                lx.eval('item.refSystem {}')
                lx.eval('user.value solo 0')
            except Exception:
                lx.eval('unhide')
                lx.out(traceback.format_exc())
                lx.eval('layout.createOrClose EventLog "Event Log_layout" title:@macros.layouts@EventLog@ width:600 height:600 persistent:true open:true')

    def checkState(self):
		if lx.eval("query scriptsysservice userValue.isDefined ? solo")==0:
			lx.eval( 'user.defNew solo boolean' );
			lx.eval( 'user.def solo username value:0' );
		return int(lx.eval('user.value solo ?'))


    def commander_query(self,index):
        if index == 1:
            # The active argument is at index 1
            return self.checkState()

    def basic_Enable(self,msg):
        if self.checkState():
            return True
        elif modo.Scene().selected:
            return True
        else:
            return False

lx.bless(solo_toggle, "solo.toggle")
