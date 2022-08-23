import maya.cmds as cmds

def select_keyed():
    transform_nodes = cmds.ls(type="transform", recursive=True)
    cmds.select(clear=True)

    for transform_node in transform_nodes:
        children = cmds.listRelatives(transform_node, children=True)
        child_node = cmds.nodeType(children[0])

        if not children:
            continue
        elif child_node == "camera" or child_node == "nurbsCurve":
            keyed = cmds.keyframe(transform_node, query=True, keyframeCount=True)
            if keyed > 0:
                cmds.select(transform_node, add=True)
