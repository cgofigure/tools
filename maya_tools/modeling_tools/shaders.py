import maya.cmds as cmds

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
            print("{} doesn't have shader assigned.".format(obj))

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
        if shader == "initialParticleSE" or shader == "initialShadingGroup":
            continue
        else:
            print(shader)
