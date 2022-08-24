import maya.cmds as cmds

def find_instances():
    """ If nothing is selected, find all instances in the scene. Else find instances of the selected geometry.
    Returns:
        instances(list) - list of instances
    """
    instances = []
    cur_sel = cmds.ls(selection=True)
    if not cur_sel:
        shape_list = cmds.ls(type="mesh")
        for shape in shape_list:
            parents = cmds.listRelatives(shape, allParents=True)
            if len(parents) > 1:
                for p in parents:
                    instances.append(p)
    else:
        selection_shape = cmds.listRelatives(cur_sel)
        for shape in selection_shape:
            if len(cmds.listRelatives(shape, allParents=True)) > 1:
                instances.append(shape)
    return instances

def uninstance():
    """
    Duplicates, deletes the original instance, and renames the unique duplicate on all instances if nothing is selected,
    otherwise only "uninstance" all instances of the selected geometry
    """
    instances = find_instances()
    for instance in instances:
        dupe = cmds.duplicate(instance)
        cmds.delete(instance)
        cmds.rename(dupe, instance)
        print("Uninstanced : {}".format(instance))
    return

def select_instances():
    """
    Selects all instances if nothing is selected, otherwise only select geometry of the same instance
    """
    instances = find_instances()
    cmds.select(clear=True)
    for instance in instances:
        cmds.select(instance, add=True)
    return
