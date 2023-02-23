import maya.cmds as cmds

def get_keys(obj):
    """ Gets the keyframes of an object
    Args:
        obj(str/list): name of object or list of objects
    Return:
        keys(list): all the keys on the object
    """
    key_frames = cmds.keyframe(obj, query=True)
    if not(key_frames):
        keys = None
        print("No keyframes on : {}".format(obj))
    else:
        keys = list(set(key_frames))
        print("Keys : {}".format(keys))
    return keys

def get_and_set_attributes(source, target, time=None, key_frame=False):
    """ Gets the source objects keyable attributes to apply.
        Args:
            source(str): name of the object that attributes will be sourced from
            target(str): name of the object that the sourced attribtues will be applied to
            time(float): time/keyframe to pull the attribute data from, default is None
            key_frame(bool): set a key on the given time, default is False
    """
    attrs = cmds.listAttr(source, keyable=True)
    if not attrs:
        print("{} doesn't have keyable attributes, skipping...".format(source))
    else:
        for attr in attrs:
            if not time:
                attr_value = cmds.getAttr("{}.{}".format(source, attr))
                print("No Keyframe >>> {}.{} : {}".format(source, attr, attr_value))
                try:
                    cmds.setAttr("{}.{}".format(target, attr), attr_value)
                    print("Set {}.{} to : {}".format(target, attr, attr_value))
                except:
                    print("{}.{} is locked, skipping... ".format(target, attr))
                    continue
            else:
                attr_value = cmds.getAttr("{}.{}".format(source, attr), time=time)
                print("Keyframe {} >>> {}.{} : {}".format(time, source, attr, attr_value))
                try:
                    cmds.setAttr("{}.{}".format(target, attr), attr_value)
                    print("Set {}.{} to : {}".format(target, attr, attr_value))
                except:
                    print("{}.{} is locked, skipping... ".format(target, attr))
                    continue

            if key_frame:
                cmds.setKeyframe(target, attribute=attr, time=time)
                print("{}.{} set to {} and keyed on frame {}".format(target, attr, attr_value, time))

    print("Attributes applied : {}".format(target))
    return

def transfer_attributes(source, target):
    """ Transfers attribtues from the source ot the target, keys the target as needed
    Args:
        source(str): name of the object you want to transfer keyable attributes from
        target(str): name of the object you want to transfer keyable attributes to
    """
    print("Preparing to transfer attributes : {} >>> {}".format(source, target))
    source_keys = get_keys(source)
    target_keys = get_keys(target)

    # Checks if objects have keys or not and processes it appropriately
    if target_keys:
        print("{} has keys, removing them to perform a clean transfer.".format(target))
        cmds.cutKey(target)
    if not(source_keys):
        print("No keys, transferring attributes to : {}".format(target))
        get_and_set_attributes(source, target)
    else:
        print("Transferring keyed attributes to : {}".format(target))
        for key in source_keys:
            get_and_set_attributes(source, target, time=key, key_frame=True)

    print("Attribute Transfer Complete : {} >>> {}".format(source, target))

def transfer_anim(source=None, targets=None):
    """ Provide a string or list of objects for the source and target to transfer animation. If none, will default to
    your first and second selection.
    Args:
        source(str/list): name or list of objects you want to transfer keys from, defaults to your first selection
        targets(str/list): name or list of objects you want to transfer keys from, defaults to your second selection
    """
    print("Starting Animation Transfer")
    if (source is None) or (targets is None):
        cur_sel = cmds.ls(selection=True)
        if not cur_sel:
            LOGGER.warning("Don't have a source or target to transfer anim. Returning...")
            return
        if not source:
            source = str(cur_sel.pop(0))
            print("Setting the source as : {}".format(source))
        if not targets:
            if not cur_sel:
                LOGGER.warning("Don't have a valid target to transfer too. Returning...")
                return
            targets = cur_sel

    if isinstance(source, str) and isinstance(targets, str) and "*" in source:
        print("* found in string, converting to list")
        source = cmds.ls(source)
        targets = cmds.ls(targets)
        for obj in source:
            if "Spring" in obj:
                print("Skipping Spring Control : {}".format(obj))
                continue
            for target in targets:
                if obj.split(":")[1] == target.split(":")[1]:
                    transfer_attributes(source=obj, target=target)
    elif isinstance(source, list) and isinstance(targets, list):
        print("Processing Lists")
        for obj in source:
            if "Spring" in obj:
                print("Skipping Spring Control : {}".format(obj))
                continue
            for target in targets:
                if obj.split(":")[1] == target.split(":")[1]:
                    transfer_attributes(source=obj, target=target)
    elif isinstance(source, str) and isinstance(targets, list):
        print("Source is string, Targets is list")
        for target in targets:
            if "Spring" in target:
                print("Skipping Spring Control : {}".format(targets))
                continue
            transfer_attributes(source, target)
    else:
        print("Processing Strings")
        transfer_attributes(source, targets)

    print("Animation Transfer Complete")
