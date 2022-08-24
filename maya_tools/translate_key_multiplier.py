import maya.cmds as cmds


def get_key_range():
    rig_controls = cmds.ls(selection=True)
    key_ranges = []
    for rig_control in rig_controls:
        key_range = cmds.keyframe(rig_control + ".translate", timeChange=True, query=True)
        if not key_range:
            continue
        else:
            min_keyframe_float = min(key_range)
            max_keyframe_float = max(key_range)
            key_ranges.append(min_keyframe_float)
            key_ranges.append(max_keyframe_float)
    return key_ranges


def multiply_translate_keys(value="1.0"):
    key_range = get_key_range()
    min_key = min(key_range)
    max_key = max(key_range)
    rig_controls = cmds.ls(selection=True)
    for rig_control in rig_controls:
        x_keyframes = cmds.keyframe(rig_control + ".translateX", time=(int(min_key), int(max_key)), query=True)
        y_keyframes = cmds.keyframe(rig_control + ".translateY", time=(int(min_key), int(max_key)), query=True)
        z_keyframes = cmds.keyframe(rig_control + ".translateZ", time=(int(min_key), int(max_key)), query=True)

        x_key_value = cmds.keyframe(rig_control + ".translateX", time=(int(min_key), int(max_key)), query=True,
                                    valueChange=True)
        y_key_value = cmds.keyframe(rig_control + ".translateY", time=(int(min_key), int(max_key)), query=True,
                                    valueChange=True)
        z_key_value = cmds.keyframe(rig_control + ".translateZ", time=(int(min_key), int(max_key)), query=True,
                                    valueChange=True)

        if not x_keyframes:
            continue
        else:
            for x in range(0, len(x_keyframes)):
                cmds.keyframe(rig_control + ".translateX", time=(x_keyframes[x], x_keyframes[x]),
                              valueChange=(x_key_value[x] * float(value)))
        if not y_keyframes:
            continue
        else:
            for y in range(0, len(y_keyframes)):
                cmds.keyframe(rig_control + ".translateY", time=(y_keyframes[y], y_keyframes[y]),
                              valueChange=(y_key_value[y] * float(value)))
        if not z_keyframes:
            continue
        else:
            for z in range(0, len(z_keyframes)):
                cmds.keyframe(rig_control + ".translateZ", time=(z_keyframes[z], z_keyframes[z]),
                              valueChange=(z_key_value[z] * float(value)))
    return