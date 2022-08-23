import maya.cmds as cmds
import pymel.core as pm


def create_turntable_lights():
    lgt_scale = 50

    print("Setting up key light")
    cmds.directionalLight(name="Key", rotation=(-30, -45, 0))
    cmds.xform("Key", scale=(lgt_scale, lgt_scale, lgt_scale), translation=(-150, 250, 150))

    print("Setting up fill light")
    cmds.directionalLight(name="Fill", intensity=.5, rotation=(0, 45, 0))
    cmds.xform("Fill", scale=(lgt_scale, lgt_scale, lgt_scale), translation=(150, 125, 150))

    print("Setting up back light")
    cmds.directionalLight(name="Back", intensity=.2, rotation=(-15, -135, 0))
    cmds.xform("Back", scale=(lgt_scale, lgt_scale, lgt_scale), translation=(-150, 250, -150))

    turntable_light_grp = cmds.group("Key", "Fill", "Back", name="TurntableLight_grp")
    print("Created turntable lights : {}".format(turntable_light_grp))
    return turntable_light_grp


def frame_camera_to_asset(cam_shape=None):
    print("Framing camera to asset")
    meshes = cmds.ls(type="mesh")
    cmds.select(meshes)
    pm.viewFit(cam_shape, all=False, fitFactor=.98)

    cam_translateZ = cmds.getAttr(cam_shape + ".translateZ")
    cam_translateY = cmds.getAttr(cam_shape + ".translateY")

    print("Creating, scaling, and moving turntable control")
    turntable_ctrl = cmds.circle(name="Turntable_ctrl", normal=(0, 1, 0), constructionHistory=False)
    cmds.scale(cam_translateZ, cam_translateZ, cam_translateZ, turntable_ctrl[0])
    cmds.move(0, cam_translateY, 0, turntable_ctrl[0])

    print("Parent constraining camera to turntable control")
    cmds.parentConstraint(turntable_ctrl, cam_shape, maintainOffset=True)
    return turntable_ctrl


def add_cam_ring_animation(control_ring):
    print("Animating turntable control")
    cmds.setKeyframe(control_ring, attribute="rotate", time=1)
    cmds.setAttr(control_ring[0] + ".rotateY", 360)
    cmds.setKeyframe(control_ring, attribute="rotate", time=360)
    return


def add_lgt_animation(lgt_grp):
    print("Animating {}".format(lgt_grp))
    cmds.setKeyframe(lgt_grp, attribute="rotate", time=360)
    cmds.setAttr(lgt_grp + ".rotateY", 360)
    cmds.setKeyframe(lgt_grp, attribute="rotate", time=720)
    return


def create_turntable(start_frame=1, end_frame=720):
    print("Creating Turntable_Camera")
    cmds.camera()
    new_camera = cmds.ls(selection=True)
    turntable_cam = cmds.rename(new_camera, "Turntable_Camera")

    # Set start and end times on the timeline
    cmds.playbackOptions(min=start_frame, max=end_frame)

    # Create lights, camera, control, and animate them
    turntable_light_grp = create_turntable_lights()
    cam_ring_control = frame_camera_to_asset(turntable_cam)
    add_cam_ring_animation(cam_ring_control)
    add_lgt_animation(turntable_light_grp)
    cmds.group(turntable_cam, turntable_light_grp, cam_ring_control, name="Turntable")