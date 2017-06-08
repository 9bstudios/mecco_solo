# python

import lx, modo

def implicit_selection():
    """Tries to return a list of selected items. If no items are selected, tries
    to return active mesh layers. If there are no active mesh layers, returns
    an empty list."""

    selected = [i for i in modo.Scene().selected if i.isLocatorSuperType()]
    if selected:
        return selected

    active = get_active_layers()
    if active:
        return active

    return []

def get_active_layers():
    """Returns a list of all currently active mesh layers (regardless of selection state)."""

    lyr_svc = lx.service.Layer ()
    scan = lx.object.LayerScan (lyr_svc.ScanAllocate (lx.symbol.f_LAYERSCAN_ACTIVE))
    itemCount = scan.Count ()
    if itemCount > 0:
        items = [modo.Mesh( scan.MeshItem(i) ) for i in range(itemCount)]
    scan.Apply ()

    return items
