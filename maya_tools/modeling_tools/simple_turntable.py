import maya.cmds as cmds
import pymel.core as pm


def create_turntable_lights(grp_name="Turntable_Light_grp", key_intensity=1, fill_intensity=.5, back_intensity=.2,
                            lgt_scale=50):
    """ Creates a group, key, fill, and back lights
    Args:
        grp_name(str): the name of the group for the lights
        key_intensity(float): key light intensity
        fill_intensity(float): fill light intensity
        back_intensity(float): back light intensity
        lgt_scale(float): scale of lights
    Returns:
        turntable_light_grp(str): the name of the turntable light group
    """
    print("Setting up key light")
    cmds.directionalLight(name="Key",intensity=key_intensity, rotation=(-30, -45, 0))
    cmds.xform("Key", scale=(lgt_scale, lgt_scale, lgt_scale), translation=(-150, 250, 150))

    print("Setting up fill light")
    cmds.directionalLight(name="Fill", intensity=fill_intensity, rotation=(0, 45, 0))
    cmds.xform("Fill", scale=(lgt_scale, lgt_scale, lgt_scale), translation=(150, 125, 150))

    print("Setting up back light")
    cmds.directionalLight(name="Back", intensity=back_intensity, rotation=(-15, -135, 0))
    cmds.xform("Back", scale=(lgt_scale, lgt_scale, lgt_scale), translation=(-150, 250, -150))

    turntable_light_grp = cmds.group("Key", "Fill", "Back", name=grp_name)
    print("Created turntable lights : {}".format(turntable_light_grp))
    return turntable_light_grp


def frame_camera_to_asset(camera_node=None):
    """ Frames the camera to the geometry in the scene and creates a control
    Args:
        camera_node(str): name of the camera node
    Returns:
        turntable_ctrl(str): name of the turntable control
    """
    print("Framing camera to asset")
    meshes = cmds.ls(type="mesh")
    cmds.select(meshes)
    pm.viewFit(camera_node, all=False, fitFactor=.98)

    cam_translateZ = cmds.getAttr("{}.translateZ".format(camera_node))
    cam_translateY = cmds.getAttr("{}.translateY".format(camera_node))

    print("Creating, scaling, and moving turntable control")
    turntable_ctrl = cmds.circle(name="Turntable_ctrl", normal=(0, 1, 0), constructionHistory=False)
    cmds.scale(cam_translateZ, cam_translateZ, cam_translateZ, turntable_ctrl[0])
    cmds.move(0, cam_translateY, 0, turntable_ctrl[0])

    print("Parent constraining camera to turntable control")
    cmds.parentConstraint(turntable_ctrl, camera_node, maintainOffset=True)
    return turntable_ctrl


def add_cam_ring_animation(control_ring):
    """ Animates the turntable control
    Args:
        control_ring(str): name of the control to animate
    """
    print("Animating turntable control")
    cmds.setKeyframe(control_ring, attribute="rotate", time=1)
    cmds.setAttr("{}.rotateY".format(control_ring[0]), 360)
    cmds.setKeyframe(control_ring, attribute="rotate", time=360)
    return


def add_lgt_animation(lgt_grp):
    """ Animates the group of lights
    Args:
        lgt_grp(str): name of the group of lights to animate
    """
    print("Animating {}".format(lgt_grp))
    cmds.setKeyframe(lgt_grp, attribute="rotate", time=360)
    cmds.setAttr("{}.rotateY".format(lgt_grp), 360)
    cmds.setKeyframe(lgt_grp, attribute="rotate", time=720)
    return


def create_turntable(start_frame=1, end_frame=720):
    print("Creating Turntable_Camera")
    cmds.camera()
    new_camera = cmds.ls(selection=True)
    turntable_cam = cmds.rename(new_camera, "Turntable_Camera")

    # Set start and end times on the timeline
    cmds.playbackOptions(min=start_frame, max=end_frame)

    # Create lights, control, and animate them
    turntable_light_grp = create_turntable_lights()
    cam_ring_control = frame_camera_to_asset(turntable_cam)
    add_cam_ring_animation(cam_ring_control)
    add_lgt_animation(turntable_light_grp)
    cmds.group(turntable_cam, turntable_light_grp, cam_ring_control, name="Turntable")