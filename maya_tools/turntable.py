import maya.cmds as cmds
import pymel.core as pm
import constants


def create_turntable_lights():
    lgt_scale = 50

    print("Setting up key light")
    cmds.directionalLight(name=constants.KEY, rotation=(-30, -45, 0))
    cmds.xform(constants.KEY, scale=(lgt_scale, lgt_scale, lgt_scale), translation=(-150, 250, 150))

    print("Setting up fill light")
    cmds.directionalLight(name=constants.FILL, intensity=.5, rotation=(0, 45, 0))
    cmds.xform(constants.FILL, scale=(lgt_scale, lgt_scale, lgt_scale), translation=(150, 125, 150))

    print("Setting up back light")
    cmds.directionalLight(name=constants.BACK, intensity=.2, rotation=(-15, -135, 0))
    cmds.xform(constants.BACK, scale=(lgt_scale, lgt_scale, lgt_scale), translation=(-150, 250, -150))

    turntable_light_grp = cmds.group(constants.KEY, constants.FILL, constants.BACK, name=constants.LIGHT_GRP)
    print("Created turntable lights : {}".format(turntable_light_grp))
    return turntable_light_grp


def frame_camera_to_asset(cam_shape=None):
    meshes = cmds.ls(type="mesh")
    cmds.select(meshes)
    pm.viewFit(cam_shape, all=False, fitFactor=.98)

    # Get's Camera's translate Z and Y
    cam_translateZ = cmds.getAttr(camera_node + ".translateZ")
    cam_translateY = cmds.getAttr(camera_node + ".translateY")

    # Creates the turntable control, moves it to the Camera's translate y and
    turntable_ctrl = cmds.circle(name=constants.TURNTABLE_CTRL, normal=(0, 1, 0), constructionHistory=False)

    # Scales the control tot he Camera's translate z and parent constrains the Camera
    cmds.scale(cam_translateZ, cam_translateZ, cam_translateZ, turntable_ctrl[0])
    cmds.move(0, cam_translateY, 0, turntable_ctrl[0])
    cmds.parentConstraint(turntable_ctrl, camera_nde, maintainOffset=True)
    return turntable_ctrl


def add_cam_ring_animation(control_ring):
    cmds.setKeyframe(control_ring, attribute="rotate", time=constants.START_TIME)
    cmds.setAttr(control_ring[0] + ".rotateY", 360)
    cmds.setKeyframe(control_ring, attribute="rotate", time=constants.END_TIME * .5)
    return


def add_lgt_animation(lgt_grp):
    cmds.setKeyframe(lgt_grp, attribute="rotate", time=constants.END_TIME * .5)
    cmds.setAttr(lgt_grp + ".rotateY", 360)
    cmds.setKeyframe(lgt_grp, attribute="rotate", time=constants.END_TIME)
    return


def create_turntable(start_frame=constants.START_TIME, end_frame=constants.END_TIME):
    print("Creating {}".format(constants.TURNTABLE_CAM))
    cmds.camera()
    new_camera = cmds.ls(selection=True)
    cmds.rename(new_camera, constants.TURNTABLE_CAM)

    # Set start and end times on the timeline
    cmds.playbackOptions(min=start_frame, max=end_frame)

    # Create lights, camera, control, and animate them
    turntable_light_grp = create_turntable_lights()
    cam_ring_control = frame_camera_to_asset(constants.TURNTABLE_CAM)
    add_cam_ring_animation(cam_ring_control)
    add_lgt_animation(turntable_light_grp)
