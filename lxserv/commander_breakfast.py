import lx, modo, mecco_solo

"""A simple example of a blessed MODO command using the commander module.
https://github.com/adamohern/commander for details"""

def get_mode():
    """Returns the current selection mode as any of the following strings:
    vertex;edge;polygon;item;pivot;center;ptag
    """

    modes = 'vertex;edge;polygon;item;pivot;center;ptag'
    for mode in modes.split(';'):
        if lx.eval('select.typeFrom %s;%s ?' % (mode, modes)):
            return mode
    return False

class CommandClass(mecco_solo.CommanderClass):
    _commander_last_used = []

    def commander_arguments(self):
        return [
            {
                'name': 'solo',
                'datatype': 'boolean',
                'flags': ['query', 'optional']
            }
        ]

    def commander_execute(self, msg, flags):
        state = self.commander_arg_value(0)

        restore_mode = get_mode()

        # Enable
        lx.eval('select.typeFrom item true')
        lx.eval('item.refSystem')
        lx.eval('hide.unsel')
        lx.eval('select.typeFrom %s true' % restore_mode)

        #disable
        lx.eval('select.typeFrom item true')
        lx.eval('unhide')
        lx.eval('item.refSystem {}')
        lx.eval('select.typeFrom %s true' % restore_mode)

lx.bless(CommandClass, 'solo.set')
