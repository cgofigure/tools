2import maya.cmds as cmds

def find_xform_geo_nodes():
    affected_proxies = []
    xform_geo_nodes = cmds.ls(type="transformGeometry")
    for xform_geo_node in xform_geo_nodes:
        rs_proxy_mesh = cmds.listConnections(xform_geo_node, type="RedshiftProxyMesh")
        if rs_proxy_mesh:
            linked_mesh = cmds.listConnections(xform_geo_node, source=False, destination=True)[0]
            affected_proxies.append(linked_mesh)
    cmds.sets(affected_proxies, name="Affected_Proxies")
    return affected_proxies

def fix_selected_proxies():
    sel = cmds.ls(selection=True)
    xform_geo_nodes = cmds.ls(type="transformGeometry")
    for obj in sel:
        ws_rotate_pivot = cmds.xform(obj, rotatePivot=True, query=True, worldSpace=True)
        for xform_geo_node in xform_geo_nodes:
            if cmds.objExists(xform_geo_node):
                rs_proxy_mesh = cmds.listConnections(xform_geo_node, type="RedshiftProxyMesh")[0]
                if rs_proxy_mesh:
                    linked_mesh = cmds.listConnections(xform_geo_node, source=False, destination=True)[0]
                    if linked_mesh == obj:
                        cmds.xform(obj, scalePivot=[0, 0, 0], rotatePivot=[0, 0, 0], translation=ws_rotate_pivot)
                        cmds.connectAttr(rs_proxy_mesh + ".outMesh", linked_mesh + "Shape.inMesh", force=True)
                        cmds.delete(xform_geo_node)



