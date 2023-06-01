import maya.cmds as cmds

def transfer_uvs():
    # grab all the selected objects
    selection = cmds.ls(sl=True)

    # save first one into variable
    # pop first one out of the selected objects list
    driver = selection.pop(0)

    # for each object in the selected objects list
    for object in selection:
        cmds.select([driver,object])
        # transfer attributes
        cmds.transferAttributes(sampleSpace=4, transferUVs=2, transferColors=2)