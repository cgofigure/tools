import maya.cmds as cmds
import os.path


def build_structure():
    # gets the Maya file name
    scene_name = os.path.basename(cmds.file(q=True, sn=True))

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
    cmds.group(scene_name[:-3], asset_groups)

def compare_shaders():
    shader_groups = cmds.ls(type="shadingEngine")

    for i in range(0, len(shader_groups)):
        for j in range(i + 1, len(shader_groups)):
            comparison = cmds.shadingNetworkCompare(shader_groups[i], shader_groups[j])
            shader_compare_result = cmds.shadingNetworkCompare(comparison, query=True, equivalent=True)
            if shader_compare_result == True:
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
    shaders_to_remove = []

    for shader in shaders:
        if shader == "initialParticleSE":
            continue
        elif shader == "initialShadingGroup":
            continue
        else:
            shaders_to_remove.append(shader)

    for sg in shaders_to_remove:
        print(sg)

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

    for instance in instances:
        dupe = cmds.duplicate(instance)
        cmds.delete(instance)
        cmds.rename(dupe, instance)

def select_instances():
    instances = find_instances()
    cmds.select(clear=True)
    for instance in instances:
        cmds.select(instance, add=True)
        