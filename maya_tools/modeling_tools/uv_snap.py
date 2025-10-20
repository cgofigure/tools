import maya.cmds as cmds
import os


def resolution_settings(*args):
    iterations = 8
    res_min = 32
    res_max = 32 * (2 ** iterations)

    tex_width_value = cmds.intSlider("width_slider", query=True, value=True)
    tex_height_value = cmds.intSlider("height_slider", query=True, value=True)

    # width value for slider
    width_res = res_min
    for i in range(0, iterations + 1, 1):
        if tex_width_value == i:
            cmds.text("width_resolution", edit=True, label=str(width_res))
        width_res *= 2

    # height value for slider
    height_res = res_min
    for i in range(0, iterations + 1, 1):
        if tex_height_value == i:
            cmds.text("height_resolution", edit=True, label=str(height_res))
        height_res *= 2


def ui_settings():
    cmds.text(label="Create UV Snapshot for Selection")
    cmds.text(label="Set Resolution:")

    # width controller
    cmds.rowLayout(adjustableColumn3=2, numberOfColumns=3)
    cmds.text(label="Width: ")
    cmds.intSlider("width_slider", min=0, max=8, value=6, step=1, width=150, dragCommand=resolution_settings)
    cmds.text("width_resolution", label="")
    cmds.setParent("..")

    # height controller
    cmds.rowLayout(adjustableColumn3=2, numberOfColumns=3)
    cmds.text(label="Height:")
    cmds.intSlider("height_slider", min=0, max=8, value=6, step=1, width=150, dragCommand=resolution_settings)
    cmds.text("height_resolution", label="")
    cmds.setParent("..")

    resolution_settings()


def save_snapshot(*args):
    filters = "tga(*.tga);; png(*.png);; tif(*.tif)"

    # get values from resolution sliders for texture size
    texture_width = int(cmds.text("width_resolution", query=True, label=True))
    texture_height = int(cmds.text("height_resolution", query=True, label=True))

    # get Open File and Anti Alias checkbox values
    auto_load = cmds.checkBox("open_file", query=True, value=True)
    anti_alias = cmds.checkBox("anti_aliasing", query=True, value=True)

    file_path = cmds.fileDialog2(ff=filters, rf=True)

    # generate and save UVs
    cmds.uvSnapshot(name=file_path[0], xr=texture_width, yr=texture_height, o=True, aa=anti_alias, ff=file_path[1])

    # if Open File checkbox is on then it'll open the texture after it saves
    if auto_load:
        os.startfile(file_path[0])


def uv_snapshot():
    # checkboxes for Open File and Anti Alias
    cmds.rowLayout(numberOfColumns=2)
    cmds.checkBox("open_file", label="Open File", value=True)
    cmds.checkBox("anti_aliasing", label="Anti Alias", value=True)
    cmds.setParent("..")

    cmds.button(label="Save Snapshot", command=save_snapshot)


def create_uv_snap_ui():
    if cmds.window("UVSnapshot", exists=True):
        cmds.deleteUI("UVSnapshot")

    cmds.window("UVSnapshot", title="UVSnap", resizeToFitChildren=True, sizeable=False, toolbox=False)

    cmds.columnLayout(adj=True)
    ui_settings()
    uv_snapshot()

    cmds.showWindow("UVSnapshot")

