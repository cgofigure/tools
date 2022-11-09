import maya.cmds as cmds
import os.path

def get_publish_path():
    path = cmds.file(sceneName=True, query=True)
    file_name = os.path.basename(path)[:-3]
    local_file_path_split = path.split(file_name)[0]
    local_file_path = local_file_path_split.split("D:")[0]
    publish_path = "B:" + local_file_path + file_name + "/Prep/"

    return publish_path

def publish():
    file_path = cmds.file(sceneName=True, query=True)
    file_name = os.path.basename(file_path)[:-3]
    publish_path = get_publish_path()

    if cmds.objExists("Publish"):
        if cmds.nodeType("Publish") == "objectSet":
            publish_nodes = cmds.sets("Publish", nodesOnly=True, query=True)
            for node in publish_nodes:
                export_path = publish_path + file_name + "__" + node
                cmds.select(node)
                cmds.file(export_path, type="mayaAscii", exportSelected=True, force=True)
