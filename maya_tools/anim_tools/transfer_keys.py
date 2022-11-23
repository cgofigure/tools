import maya.cmds as cmds
from maya_tools import transfer_xform as tx

def transfer_keys(source, target):
    for i in range(0, len(source)):
        source_keys = tx.get_keys(source[i])
        target_keys = tx.get_keys(target[i])

        if not source_keys and not target_keys:
            print("No keys to transfer, consolidating xforms to target")
            tx.fix_target_xforms(source[i], target[i])
        if source_keys and not target_keys:
            print("No keys on {}, setting keyframe on target from source".format(source[i]))
            for source_key in source_keys:
                cmds.currentTime(source_key, edit=True)
                cmds.setKeyframe(target[i])
            keys = tx.get_keys((source[i], target[i]))
            for key in keys:
                cmds.currentTime(key, edit=True)
                tx.fix_target_xforms(source[i], target[i])
    return