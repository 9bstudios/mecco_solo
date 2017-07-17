#!/usr/bin/env python

import lx
import modo
import traceback
import solo


def create_hidden_group():
    lx.eval('!!group.create %s std' % solo.HIDDEN_GROUP_NAME)
    group = hidden_group()
    return group


def hidden_group():
    for group in modo.Scene().getGroups():
        if group.name == solo.HIDDEN_GROUP_NAME:
            return group
    return None


class solo_toggle(solo.CommanderClass):
    def commander_arguments(self):
        return [
            {
                'name': 'solo',
                'datatype': 'boolean',
                'flags': ['query', 'optional']
            }
        ]

    def commander_execute(self, msg, flags):

        # save current selection for later
        restore_mode = solo.get_selection_mode()
        restore_sel = modo.Scene().selected

        implicit_selection = solo.implicit_selection()

        # nothing is selected
        # this is virtually impossible to hit, since the command is disabled
        # if nothing is selected
        if not implicit_selection:
            try:
                modo.dialogs.alert(
                    lx.eval("query messageservice msgfind ? @mecco_solo_messages@NothingSelectedTitle@"),
                    lx.eval("query messageservice msgfind ? @mecco_solo_messages@NothingSelectedMessage@")
                )
            except:
                pass

            return

        sceneStatuses = solo.SceneStatuses()

        # do the magic
        if self.commander_arg_value(0) is not None:
            solo_is_active = not self.commander_arg_value(0)
        else:
            solo_is_active = sceneStatuses.current_scene_is_solo_active()

        # hide components
        if lx.eval('user.value solo_hide_components ?'):
            if restore_mode in ('polygon', 'edge', 'vertex'):
                if solo_is_active == False:
                    lx.eval('hide.unsel')
                else:
                    lx.eval('unhide')

        # change to item mode, drop selection, and select implicit_selection()
        lx.eval('select.typeFrom item true')
        lx.eval('select.drop item')

        for item in implicit_selection:
            item.select()

        if solo_is_active == False:
            try:
                hide = lx.eval('user.value solo_hide_items ?')
                if hide != 0:
                    if hide == 2:
                        items = list()
                        for item in modo.Scene().iterItems():
                            if item.isLocatorSuperType():
                                if not item in implicit_selection:
                                    items.append(item)

                        group = create_hidden_group()
                        group.addItems(items)
                        group.channel('visible').set('off')

                        for item in implicit_selection:
                            item.select()
                    else:
                        lx.eval('hide.unsel')

                if lx.eval('user.value solo_set_reference_center ?'):
                    lx.eval('item.refSystem {%s}' % implicit_selection[-1].id)

                sceneStatuses.set_current_scene_active(True)

            except Exception:
                lx.out(traceback.format_exc())
        else:
            try:
                if lx.eval('user.value solo_hide_items ?') != 0:
                    group = hidden_group()
                    # It will be wrong to check solo_hide_items here since it could be changed after solo activation
                    # Checking group validity
                    if group is None:
                        lx.eval('unhide')
                    else:
                        group.channel('visible').set('on')
                        modo.Scene().removeItems(group, False)

                if lx.eval('user.value solo_set_reference_center ?'):
                    lx.eval('item.refSystem {}')

                sceneStatuses.set_current_scene_active(False)

            except Exception:
                lx.out(traceback.format_exc())

        # restore selection
        lx.eval('select.drop item')

        for item in restore_sel:
            item.select()

        lx.eval('select.typeFrom %s true' % restore_mode)

        notifier = solo.Notifier()
        notifier.Notify(lx.symbol.fCMDNOTIFY_DATATYPE)

    def commander_query(self, index):
        sceneStatuses = solo.SceneStatuses()
        if index == 0:
            if sceneStatuses.current_scene_is_solo_active():
                return True
            else:
                return False

    def basic_Enable(self, msg):
        sceneStatuses = solo.SceneStatuses()
        if sceneStatuses.current_scene_is_solo_active():
            return True
        elif solo.implicit_selection():
            return True
        else:
            return False

    def commander_notifiers(self):
        return [("solo.notifier", "")]


lx.bless(solo_toggle, "solo.toggle")
