import maya.cmds as cmds

def bake_pair_blends():
    invalid_pair_blends = validate_pair_blends()
    bake_targets = []

    start_time = cmds.playbackOptions(query=True, minTime=True)
    end_time = cmds.playbackOptions(query=True, maxTime=True)

    for pair_blend in invalid_pair_blends:
        target = cmds.listConnections(pair_blend)[0]
        bake_targets.append(target)

    cmds.bakeResults(bake_targets, time=(start_time, end_time), simulation=True)
    print("Baked animation ({}-{}) : {}".format(start_time, end_time, bake_targets))

    cmds.delete(invalid_pair_blends)
    print("Deleted pairBlend nodes : {}".format(invalid_pair_blends))


def validate_pair_blends():
    invalid_nodes = []
    pair_blends = cmds.ls(type="pairBlend")

    for pair_blend in pair_blends:
        if not cmds.referenceQuery(pair_blend, isNodeReferenced=True):
            invalid_nodes.append(pair_blend)
    return invalid_nodes

