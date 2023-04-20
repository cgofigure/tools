import maya.cmds as cmds


def get_key_range():
    rig_ctrls = cmds.ls(selection=True)
    key_ranges = []
    for rig_ctrl in rig_ctrls:
        key_range = cmds.keyframe("{}.translate".format(rig_ctrl), timeChange=True, query=True)
        if not key_range:
            continue
        else:
            key_ranges.append(min(key_range))
            key_ranges.append(max(key_range))
    return key_ranges


def multiply_translate_keys(value="1.0"):
    key_range = get_key_range()
    min_key = min(key_range)
    max_key = max(key_range)
    rig_ctrls = cmds.ls(selection=True)
    for rig_ctrl in rig_ctrls:
        x_keyframes = cmds.keyframe("{}.translateX".format(rig_ctrl), time=(int(min_key), int(max_key)), query=True)
        y_keyframes = cmds.keyframe("{}.translateY".format(rig_ctrl), time=(int(min_key), int(max_key)), query=True)
        z_keyframes = cmds.keyframe("{}.translateZ".format(rig_ctrl), time=(int(min_key), int(max_key)), query=True)

        x_key_value = cmds.keyframe("{}.translateX".format(rig_ctrl), time=(int(min_key), int(max_key)), query=True,
                                    valueChange=True)
        y_key_value = cmds.keyframe("{}.translateY".format(rig_ctrl), time=(int(min_key), int(max_key)), query=True,
                                    valueChange=True)
        z_key_value = cmds.keyframe(".translateZ".format(rig_ctrl), time=(int(min_key), int(max_key)), query=True,
                                    valueChange=True)

        if not x_keyframes:
            continue
        else:
            for x in range(0, len(x_keyframes)):
                cmds.keyframe("{}.translateX".format(rig_ctrl), time=(x_keyframes[x], x_keyframes[x]),
                              valueChange=(x_key_value[x] * float(value)))
        if not y_keyframes:
            continue
        else:
            for y in range(0, len(y_keyframes)):
                cmds.keyframe("{}.translateY".format(rig_ctrl), time=(y_keyframes[y], y_keyframes[y]),
                              valueChange=(y_key_value[y] * float(value)))
        if not z_keyframes:
            continue
        else:
            for z in range(0, len(z_keyframes)):
                cmds.keyframe("{}.translateZ".format(rig_ctrl), time=(z_keyframes[z], z_keyframes[z]),
                              valueChange=(z_key_value[z] * float(value)))

