import maya.cmds as cmds
import os.path


def build_structure(grp_name=None):
    """ Build asset structure based on file name if a scene_name is not given
    Args:
        grp_name(str): name of the parent group, defaults to the file name if None
    """
    # if package name is not defined, will name it based on the file name
    if not grp_name:
        grp_name = os.path.basename(cmds.file(q=True, sn=True))

    # desired list of groups we want to create
    asset_groups = [
        "Meshes",
        "Rig",
        "Lights"
    ]

    # creates the groups and names them
    for asset_group in asset_groups:
        cmds.CreateEmptyGroup()
        cmds.rename(asset_group)

    # groups our created groups and names the group based on the scene
    cmds.group(grp_name[:-3], asset_groups)

def compare_shaders():
    shader_groups = cmds.ls(type="shadingEngine")

    for i in range(0, len(shader_groups)):
        for j in range(i + 1, len(shader_groups)):
            comparison = cmds.shadingNetworkCompare(shader_groups[i], shader_groups[j])
            if not cmds.shadingNetworkCompare(comparison, query=True, equivalent=True):
                print(cmds.shadingNetworkCompare(comparison, query=True, network1=True))

def check_meshes_without_shaders():
    meshes = cmds.ls(type="mesh")
    parents = []

    for mesh in meshes:
        parent = cmds.listRelatives(mesh, parent=True)
        parents.append(parent[0])

    parents = list(dict.fromkeys(parents))

    for obj in parents:
        children = cmds.listRelatives(obj, children=True) or []
        shader = cmds.listConnections(children[0], type="shadingEngine")
        if not shader:
            print(obj + " doesn't have shader assigned.")

def check_unassigned_shaders():
    shading_groups = cmds.ls(type="shadingEngine")
    unassigned_shaders = []

    for shading_group in shading_groups:
        shading_connections = cmds.listConnections(shading_group)
        for shading_connection in shading_connections:
            if cmds.nodeType(shading_connection) != "transform":
                unassigned_shaders.append(shading_group)

    shaders = list(dict.fromkeys(unassigned_shaders))

    for shader in shaders:
        if shader == "initialParticleSE":
            continue
        elif shader == "initialShadingGroup":
            continue
        else:
            print(shader)
