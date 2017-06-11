# python

import lx
import solo

class CommandClass(solo.CommanderClass):
    def commander_arguments(self):
        return [
                {
                    'name': 'value',
                    'datatype': 'string',
                    'default': "",
                    'values_list_type': self.arg_values_list_type,
                    'values_list': self.arg_values_list,
                    'flags': ['variable', 'query'],
                }, {
                    'name': 'name',
                    'datatype': 'string',
                    'flags': ['reqforvariable'],
                }
            ]

    def commander_execute(self, msg, flags):
        value = self.commander_arg_value(0)
        name = self.commander_arg_value(1)

        lx.eval("user.value %s %s" % (name, value))

        notifier = solo.Notifier()
        notifier.Notify(lx.symbol.fCMDNOTIFY_DATATYPE)
        
    def basic_Enable(self, msg):
        sceneStatuses = solo.SceneStatuses()
        if sceneStatuses.any_solo_active_scene():
            return False
        name = self.commander_arg_value(1)
        if name == "hide_with_group":
            return lx.eval("user.value solo_hide_items ?") == 1
        return True

    def cmd_Query(self, index, vaQuery):
        name = self.commander_arg_value(1)

        # Create the ValueArray object
        va = lx.object.ValueArray()
        va.set(vaQuery)

        va.AddInt(lx.eval("user.value %s ?" % name))
        
        return lx.result.OK
        
    def basic_ArgType(self, argIndex):
        name = self.commander_arg_value(1)
        if name == "solo_hide_items":
            return 'integer'
        return 'boolean'
        
    def arg_values_list_type(self):
        name = self.commander_arg_value(1)
        if name == "solo_hide_items":
            return 'popup'
        return None
        
    def arg_values_list(self):
        name = self.commander_arg_value(1)
        if name == "solo_hide_items":
            return ['off', 'hide']
        return None

    def commander_notifiers(self):
        return [("solo.notifier", "")]

lx.bless(CommandClass, "solo.preference")
