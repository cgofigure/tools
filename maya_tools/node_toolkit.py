import maya.cmds as cmds

def get_obj_node_type(obj=None):
    """
    Args:
        obj(str): name of object to find the nodeType of, if none will get the nodeType of the first selected object.
    Returns:
        node_type(str): nodeType of the object
    """
    if not obj:
        obj = cmds.ls(selection=True)[0]
    node_type = cmds.nodeType(obj)
    cmds.textFieldGrp("node_type_field", edit=True, text=node_type)
    print(obj + " Node Type : {}".format(node_type))
    return node_type

def select_objs_by_node_type(type):
    """
    Args:
        type(str): Maya nodeType you want to select
    Returns:
        objs(list): selected objects
    """
    type = cmds.textFieldGrp("node_type_field", query=True, text=True)
    objs = cmds.ls(type=type)
    cmds.select(clear=True)
    for obj in objs:
        print("Selected : {}".format(obj))
        cmds.select(obj, add=True)
    return objs

def delete_objs_by_node_type(type):
    """
    Args:
        type(str): Maya nodeType you want to delete
    Returns:
        objs(list): selected objects
    """
    type = cmds.textFieldGrp("node_type_field", query=True, text=True)
    objs = cmds.ls(type=type)
    for obj in objs:
        cmds.delete(obj)
        print("Deleted : {}".format(obj))
    return objs

def create_node_toolkit():
    if cmds.window("node_toolkit", exists=True):
        cmds.deleteUI("node_toolkit")

    cmds.window("node_toolkit", title="Node Toolkit", sizeable=False, toolbox=True, resizeToFitChildren=True)

    cmds.columnLayout(adjustableColumn=True)
    cmds.text("Node Toolset", height=30, align="center", font="boldLabelFont")
    cmds.button("obj_node_type", label="Get Node Type", command=get_obj_node_type)
    cmds.textFieldGrp("node_type_field", adjustableColumn=True,
                                        text="nodeType ex: mesh, transform, locator, etc")
    cmds.button("select_objs_by_node_type", label="Select Node Type", command=select_objs_by_node_type)
    cmds.button("delete_objs_by_node_type", label="Delete Node Type", command=delete_objs_by_node_type)

    cmds.showWindow("node_toolkit")
