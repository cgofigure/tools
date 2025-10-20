import maya.cmds as cmds
import random

def rotate_selection(x=False, y=True, z=False):
    """ Randomly rotates your selected objects
    Args:
        x(bool): sets axis to a random value if True
        y(bool): sets axis to a random value if True
        z(bool): sets axis to a random value if True
    """
    axis_list = []

    multiplier = 360
    sel = cmds.ls(selection=True)

    if not sel:
        print("Nothing selected, please select objects and run again.")
        return

    if x:
        axis_list.append("x")
    if y:
        axis_list.append("y")
    if z:
        axis_list.append("z")

    for obj in sel:
        print("{} :".format(obj))
        for axis in axis_list:
            if axis:
                rand_value = random.random() * multiplier
                cmds.setAttr("{}.rotate{}".format(obj, axis.capitalize()), rand_value)
                print("    Set rotate{} to : {}".format(axis.capitalize(), rand_value))
