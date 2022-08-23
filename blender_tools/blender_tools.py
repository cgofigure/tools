import bpy
import bmesh

def center_vertices():
    # Behavior - Averages selected vertices position (x, y, z)
    obj = bpy.context.object
    me = obj.data
    bm = bmesh.from_edit_mesh(me)

    # Vertex Objects
    sel_v = [v.co for v in bm.verts if v.select]
    sel_v_x = [v.co.x for v in bm.verts if v.select]
    sel_v_y = [v.co.y for v in bm.verts if v.select]
    sel_v_z = [v.co.z for v in bm.verts if v.select]

    # Math: Averages the Vertex Objects (x, y, z)
    x_avg = sum(sel_v_x)/len(sel_v_x)
    y_avg = sum(sel_v_y)/len(sel_v_y)
    z_avg = sum(sel_v_z)/len(sel_v_z)

    # Sets Selected Vertices (x, y, z) to the average values
    for sel in sel_v:
        sel.xyz = (x_avg, y_avg, z_avg)

    # Updates the Blender Viewport to Reflect Changes
    bmesh.update_edit_mesh(me)
