import maya.cmds as cmds
import os.path

def export_open():
    file_path = cmds.file(sceneName=True, query=True)
    file_name = os.path.basename(file_path)[:-3]

    if not cmds.objExists(file_name):
        print("Nothing to export, no object named : {}".format(file_name))
    else:
        cmds.select(file_name)

    cmds.file(file_path, type="mayaAscii", exportSelected=True, force=True)
    cmds.file(file_path, type="mayaAscii", open=True, force=True)