import maya.cmds as cmds

def startup_selection():
    if cmds.ls(selection=True):
        selection = cmds.ls(selectection=True)
        good_asset = selection[0]
        bad_asset = selection[1]
        split_good_asset_instance = good_asset.split("_")
        split_bad_asset_instance = bad_asset.split("_")

        good_asset_instance = split_good_asset_instance[0] + "_" + split_good_asset_instance[1] + ":"
        bad_asset_instance = split_bad_asset_instance[0] + "_" + split_bad_asset_instance[1] + ":"
        cmds.textFieldGrp("good_asset_instance_field", editable=True, text=good_asset_instance)
        cmds.textFieldGrp("good_asset_instance_field", editable=True, text=bad_asset_instance)

def match_pose(*args):
    good_asset_instance = cmds.textFieldGrp("good_asset_instance_field", query=True, text=True)
    bad_asset_instance = cmds.textFieldGrp("bad_asset_instance_field", query=True, text=True)
    cmds.select(good_asset_instance + "Global_ctrl", hierarchy=True)
    selected_ctrls = cmds.ls(selection=True)
    for ctrl in selected_ctrls:
        if ctrl.endswith("_ctrl"):
            og_ctrl = ctrl.split(":")[1]
            translate_values = cmds.xform(ctrl, query=True, translation=True)
            rotate_values = cmds.xform(ctrl, query=True, rotation=True)

            cmds.xform(bad_asset_instance + og_ctrl, t=(translate_values[0], translate_values[1], translate_values[2]))
            cmds.xform(bad_asset_instance + og_ctrl, ro=(rotate_values[0], rotate_values[1], rotate_values[2]))
    cmds.select(clear=True)


def correct_connections(*args):
    good_asset_instance = cmds.textFieldGrp("good_asset_instance_field", query=True, text=True)
    bad_asset_instance = cmds.textFieldGrp("bad_asset_instance_field", query=True, text=True)
    cmds.select(good_asset_instance + "Locators", hierarchy=True)
    good_nulls = cmds.ls(selection=True)
    cmds.select(clear=True)
    for good_null in good_nulls:
        if good_null.endswith("_loc"):
            parent_constraint = cmds.listRelatives(good_null, type="parentConstraint")[0]
            source = cmds.listConnections(parent_constraint, destination=False, type="joint")[0]
            parent_obj = source.split(":")[1]
            null_loc = good_null.split(":")[1]
            bad_asset_bnd = bad_asset_instance + parent_obj
            bad_asset_loc = bad_asset_instance + null_loc
            cmds.parentConstraint(bad_asset_bnd, bad_asset_loc, maintainOffset=True)


def connector_ui():
    """Select the Source followed by the Target asset"""
    if cmds.window("Connector", exists=True):
        cmds.deleteUI("Connector")

    cmds.window("Connector", title="Connector", resizeToFitChildren=True)

    cmds.columnLayout(adj=True)
    cmds.textFieldGrp("good_asset_instance_field", label="Good Asset Namespace:")
    cmds.textFieldGrp("bad_asset_instance_field", label="Bad Asset Namespace:")
    cmds.button(label="Match Pose", command=match_pose)
    cmds.button(label="Correct Connections", command=correct_connections)
    startup_selection()

    cmds.showWindow("Connector")
