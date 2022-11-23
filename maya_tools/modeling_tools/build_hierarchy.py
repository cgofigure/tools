import maya.cmds as cmds
import os.path
import constants

def build_hierarchy(asset_name=None):
    """ Build asset hierarchy based on file name if an asset_name is not given
    Args:
        asset_name(str): name of the parent group, defaults to the file name if None
    """
    # if package name is not defined, will name it based on the file name
    if not asset_name:
        asset_name = os.path.basename(cmds.file(sceneName=True, query=True))

    # desired list of groups we want to create
    asset_groups = constants.ASSET_GROUPS

    # creates the groups and names them
    for asset_group in asset_groups:
        cmds.CreateEmptyGroup()
        cmds.rename(asset_group)

    # groups our created groups and names the group based on the scene
    cmds.group(asset_name[:-3], asset_groups)
