import maya.cmds as cmds

def select_keyed():
    """ Selects all keyed objects that are of the nodeType "camera' or "nurbsCurve"
    """
    transform_nodes = cmds.ls(type="transform", recursive=True)
    cmds.select(clear=True)

    for transform_node in transform_nodes:
        children = cmds.listRelatives(transform_node, children=True)
        child_node = cmds.nodeType(children[0])

        if child_node == "camera" or child_node == "nurbsCurve":
            keyed = cmds.keyframe(transform_node, query=True, keyframeCount=True)
            if keyed > 0:
                cmds.select(transform_node, add=True)
        else:
            print("{}'s nodeType isn't camera or nurbsCurve".format(transform_node))
