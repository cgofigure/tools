import maya.cmds as cmds
import os.path
import constants

def build_hierarchy(asset_name=None):
    """ Build asset hierarchy based on file name if an asset_name is not given
    Args:
        asset_name(str): name of the parent group, defaults to the file name if None
    """
    # desired list of groups we want to create
    asset_grps = constants.ASSET_GRPS

    ## Checks the file name if an asset_name is not given
    if not asset_name:
        asset_name = os.path.basename(cmds.file(sceneName=True, query=True))

    ## Creates the source group
    source_grp = cmds.group(asset_name[:-3])

    # Creates and parents the asset groups to the source group
    for asset_grp in asset_grps:
        cmds.group(name=asset_grp, parent=source_grp, empty=True)

