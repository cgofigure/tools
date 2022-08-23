import maya.cmds as cmds

def find_instances(*args):
    if len(cmds.ls(selection=True)) > 0:
        instances = []

        selection_shape = cmds.listRelatives(cmds.ls(selection=True))
        cmds.select(clear=True)

        for shape in selection_shape:
            if len(cmds.listRelatives(shape, allParents=True)) > 1:
                instances.append(shape)

        return instances
    else:
        instances = []
        shape_list = cmds.ls(type="mesh")

        for shape in shape_list:
            parents = cmds.listRelatives(shape, allParents=True)

            if len(parents) > 1:
                for p in parents:
                    instances.append(p)

        return instances

def uninstance():
    instances = find_instances()

    for each in instances:
        dupe = cmds.duplicate(each)
        cmds.delete(each)
        cmds.rename(dupe, each)

def select_instances():
    instance = find_instances()
    cmds.select(clear=True)
    for each in instances:
        cmds.select(add=True)

def instance_manager_ui():
    if cmds.window("InstanceManager", exists=True):
        cmds.deleteUI("InstanceManager")

    cmds.window("InstanceManager", title="Instance Manager", resizeToFitChildren=True)

    cmds.columnLayout()
    cmds.button(label="Select Instances", command=select_instances)
    cmds.radioCollection()
    cmds.radioButton(label="All")
    cmds.radioButton(label="Selection")
    cmds.button(label="Uninstance", command=uninstance)

    cmds.showWindow("InstanceManager")
