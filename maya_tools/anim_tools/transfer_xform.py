import maya.cmds as cmds


def get_keys(obj):
    """ Gets the keyframes of an object
    Args:
        obj(str/list): name of object
    Return:
        keys(list): all the keys on the object
    """
    key_frames = cmds.keyframe(obj, query=True)
    if not key_frames:
        keys = None
        print("No keyframes on : {}".format(obj))
    else:
        keys = list(set(key_frames))
    return keys


def get_xform(obj, xform="translation"):
    """ Get xyz coordinates of the object
    Args:
        obj(str): name of object
        xform(str): takes in "translation", "rotation", "scale", Default is "translation"
    Return:
        xyz(list): objects xyz coordinates of the set type
    """
    xform_list = [
        "translation",
        "rotation",
        "scale"
    ]
    if xform in xform_list:
        if xform == xform_list[0]:
            xyz = cmds.xform(obj, query=True, translation=True)
        if xform == xform_list[1]:
            xyz = cmds.xform(obj, query=True, rotation=True)
        if xform == xform_list[2]:
            xyz = cmds.xform(obj, query=True, scale=True)
        print("Getting xform : {}".format(obj + "'s " + xform + " = " + str(xyz)))
    else:
        print("{} isn't in xform_list, returning : None".format(xform))
        xyz = None
    return xyz


def add_xyz(a, b):
    """ Gets the sum of xyz coordinates and returns the new coordinates
    Args:
        a(list): takes in a list of xyz values to add with b's xyz. Input Ex. [0.0, 1.0, 0.0]
        b(list): takes in a list of xyz values to add with a's xyz. Input Ex. [0.0, 1.0, 1.0]
    Return:
        xyz(list): sum of object a and object b's xyz coordinates
    """
    xyz = []
    # Gets the sum of the source and targets translate xyz float values
    for i in range(0, len(a)):
        sum = a[i] + b[i]
        xyz.append(sum)
    return xyz


def multiply_xyz(a, b):
    """ Gets the product of xyz coordinates and returns the new coordinates
    Args:
        a(list): takes in a list of xyz values to multiply with b's xyz. Input Ex. [0.0, 1.0, 0.0]
        b(list): takes in a list of xyz values to multiply with a's xyz. Input Ex. [0.0, 1.0, 1.0]
    Return:
        xyz(list): product of object a and object b's xyz coordinates
    """
    xyz = []
    for i in range(0, len(a)):
        product = a[i] * b[i]
        xyz.append(product)
    return xyz


def source_to_target_xforms(source, target):
    """ Adds source and target's translation and rotation. Multiplies source and target scale and apply new values
    to the target.
        Args:
            source(str) = name of the object that will not be xformed
            target(str) = name of the object that will be xformed
    """
    # Source object's translation, rotation, and scale
    source_translation = get_xform(source)
    source_rotation = get_xform(source, xform="rotation")
    source_scale = get_xform(source, xform="scale")

    # Target object's translation, rotation, and scale
    target_translation = get_xform(target)
    target_rotation = get_xform(target, xform="rotation")
    target_scale = get_xform(target, xform="scale")

    # Target object's new translation, rotation, and scale
    t_xyz = add_xyz(source_translation, target_translation)
    print("New target translation = {}".format(t_xyz))

    r_xyz = add_xyz(source_rotation, target_rotation)
    print("New target rotation = {}".format(r_xyz))

    s_xyz = multiply_xyz(source_scale, target_scale)
    print("New target scale = {}".format(s_xyz))

    cmds.xform(target, rotation=[r_xyz[0], r_xyz[1], r_xyz[2]], scale=[s_xyz[0], s_xyz[1], s_xyz[2]],
               translation=[t_xyz[0], t_xyz[1], t_xyz[2]])
    return


def transfer_xforms(source=None, target=None):
    """ Transfers the translation and rotation values from the first selected object to the second
    Args:
        source(str) = name of the object you want to transfer values from, defaults to your first selection
        target(str) = name of the object you want to transfer values to, defaults to your second selection
    """
    cur_sel = cmds.ls(selection=True)
    if not source or not target and len(cur_sel > 1):
        index = 0
        if not source:
            source = cur_sel[index]
            index = index + 1
        if not target:
            target = cur_sel[index]
    print("Preparing to transfer xforms from : {}".format(source + " >>> " + target))

    # Get keys
    source_keys = get_keys(source)
    target_keys = get_keys(target)

    if not source_keys and not target_keys:
        print("No keys to process, transferring xforms : {}".format(source + " >>> " + target))
        source_to_target_xforms(source, target)
    elif not source_keys and target_keys:
        print("No keys on {}, setting keyframe based off target keys.".format(source))
        for target_key in target_keys:
            cmds.currentTime(target_key, edit=True)
            cmds.setKeyframe(source)
        keys = get_keys([source, target])
        for key in keys:
            cmds.currentTime(key, edit=True)
            source_to_target_xforms(source, target)
            cmds.setKeyframe(target)
    elif source_keys and not target_keys:
        print("No keys on {}, setting keyframe based off source keys.".format(target))
        for source_key in source_keys:
            cmds.currentTime(source_key, edit=True)3
            cmds.setKeyframe(target)
        keys = get_keys([source, target])
        for key in keys:
            cmds.currentTime(key, edit=True)
            source_to_target_xforms(source, target)
            cmds.setKeyframe(target)
    else:
        print("Source and target both have keys, continuing process.")
        source_to_target_xforms(source, target)
        cmds.setKeyframe(target)

    # Remove keys on source object and move to origin
    start_time = cmds.playbackOptions(query=True, animationStartTime=True)
    end_time = cmds.playbackOptions(query=True, animationEndTime=True)
    cmds.cutKey(source, time=(start_time, end_time))
    cmds.xform(source, rotation=[0.0, 0.0, 0.0], scale=[1.0, 1.0, 1.0], translation=[0.0, 0.0, 0.0])
    print("Process Complete")
