import maya.cmds as cmds
import pymel.core as pm
import constants


def create_turntable_lights(grp_name=constants.LIGHT_GRP, key_intensity=1, fill_intensity=.5, back_intensity=.2,
                            lgt_scale=50):
    """ Creates a key, fill, and back light, as well as, a group to hold them
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
    cmds.directionalLight(name=constants.KEY, intensity=key_intensity, rotation=(-30, -45, 0))
    cmds.xform(constants.KEY, scale=(lgt_scale, lgt_scale, lgt_scale), translation=(-150, 250, 150))

    print("Setting up fill light")
    cmds.directionalLight(name=constants.FILL, intensity=fill_intensity, rotation=(0, 45, 0))
    cmds.xform(constants.FILL, scale=(lgt_scale, lgt_scale, lgt_scale), translation=(150, 125, 150))

    print("Setting up back light")
    cmds.directionalLight(name=constants.BACK, intensity=back_intensity, rotation=(-15, -135, 0))
    cmds.xform(constants.BACK, scale=(lgt_scale, lgt_scale, lgt_scale), translation=(-150, 250, -150))

    turntable_light_grp = cmds.group(constants.KEY, constants.FILL, constants.BACK, name=grp_name)
    print("Created turntable lights : {}".format(turntable_light_grp))
    return turntable_light_grp


def frame_camera_to_asset(camera_node=None):
    """ Frames the camera to the geometry in the scene and creates a control
    Args:
        camera_node(str): name of the camera node
    Returns:
        turntable_ctrl(str): name of the turntable control
    """
    meshes = cmds.ls(type="mesh")
    cmds.select(meshes)
    pm.viewFit(camera_node, all=False, fitFactor=.98)

    # Gets Camera's translate Z and Y
    cam_translateZ = cmds.getAttr(camera_node + ".translateZ")
    cam_translateY = cmds.getAttr(camera_node + ".translateY")

    # Creates the turntable control, moves it to the Camera's translate y and
    turntable_ctrl = cmds.circle(name=constants.TURNTABLE_CTRL, normal=(0, 1, 0), constructionHistory=False)

    # Scales the control to the Camera's translate z and parent constrains the Camera
    cmds.scale(cam_translateZ, cam_translateZ, cam_translateZ, turntable_ctrl[0])
    cmds.move(0, cam_translateY, 0, turntable_ctrl[0])
    cmds.parentConstraint(turntable_ctrl, camera_node, maintainOffset=True)
    return turntable_ctrl


def add_cam_ring_animation(control_ring):
    """ Animates the turntable control
    Args:
        control_ring(str): name of the control to animate
    """
    cmds.setKeyframe(control_ring, attribute="rotate", time=constants.START_TIME)
    cmds.setAttr(control_ring[0] + ".rotateY", 360)
    cmds.setKeyframe(control_ring, attribute="rotate", time=constants.END_TIME * .5)
    return


def add_lgt_animation(lgt_grp):
    """ Animates the group of lights
    Args:
        lgt_grp(str): name of the group of lights to animate
    """
    cmds.setKeyframe(lgt_grp, attribute="rotate", time=constants.END_TIME * .5)
    cmds.setAttr(lgt_grp + ".rotateY", 360)
    cmds.setKeyframe(lgt_grp, attribute="rotate", time=constants.END_TIME)
    return


def create_turntable(start_frame=constants.START_TIME, end_frame=constants.END_TIME):
    """ Creates a turntable with basic 3 point lighting
    Args:
        start_frame(int): set the start frame, default is 1
        end_frame(int):  set the end frame, default is 720
    """
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
