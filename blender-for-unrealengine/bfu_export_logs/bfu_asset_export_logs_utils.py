import bpy
from typing import List
from .. import bfu_utils

from . import bfu_asset_export_logs

def get_asset_list() -> List[bfu_asset_export_logs.BFU_OT_UnrealExportedAsset]:
    scene = bpy.context.scene
    return scene.bfu_unreal_exported_assets_logs

def create_new_asset_log()-> bfu_asset_export_logs.BFU_OT_UnrealExportedAsset:
    scene = bpy.context.scene
    return scene.bfu_unreal_exported_assets_logs.add()

def clear_asset_logs():
    scene = bpy.context.scene
    scene.bfu_unreal_exported_assets_logs.clear()

def get_exported_asset_list():
    # TODO Need add a check to know how many asset is realy exported
    scene = bpy.context.scene
    len(scene.bfu_unreal_exported_assets_logs)

def get_export_asset_logs():
    # Write Export log with exported assets in scene.bfu_unreal_exported_assets_logs

    scene = bpy.context.scene
    StaticNum = 0
    SkeletalNum = 0
    AlembicNum = 0
    AnimNum = 0
    CameraNum = 0
    SplineNum = 0

    # Get number per asset type
    for assets in get_asset_list():
        if assets.asset_type == "StaticMesh":
            StaticNum += 1
        if assets.asset_type == "SkeletalMesh":
            SkeletalNum += 1
        if assets.asset_type == "Alembic":
            AlembicNum += 1
        if bfu_utils.GetIsAnimation(assets.asset_type):
            AnimNum += 1
        if assets.asset_type == "Camera":
            CameraNum += 1
        if assets.asset_type == "Spline":
            SplineNum += 1

    asset_number = len(scene.bfu_unreal_exported_assets_logs)
    exported_assets = StaticNum+SkeletalNum+AlembicNum+AnimNum+CameraNum+SplineNum

    OtherNum = asset_number - exported_assets

    # Asset number string
    AssetNumberByType = str(StaticNum)+" StaticMesh(s) | "
    AssetNumberByType += str(SkeletalNum)+" SkeletalMesh(s) | "
    AssetNumberByType += str(AlembicNum)+" Alembic(s) | "
    AssetNumberByType += str(AnimNum)+" Animation(s) | "
    AssetNumberByType += str(CameraNum)+" Camera(s) | "
    AssetNumberByType += str(CameraNum)+" Spline(s) | "
    AssetNumberByType += str(OtherNum)+" Other(s)" + "\n"

    ExportLog = ""
    ExportLog += AssetNumberByType
    ExportLog += "\n"
    for asset in get_asset_list():

        if (asset.asset_type == "NlAnim"):
            primaryInfo = "Animation (NLA)"
        elif (asset.asset_type == "Action"):
            primaryInfo = "Animation (Action)"
        elif (asset.asset_type == "Pose"):
            primaryInfo = "Animation (Pose)"
        else:
            if asset.object:
                if asset.object.bfu_export_as_lod_mesh:
                    primaryInfo = asset.asset_type+" (LOD)"
                else:
                    primaryInfo = asset.asset_type
            else:
                primaryInfo = asset.asset_type

        ExportLog += (
            asset.asset_name+" ["+primaryInfo+"] EXPORTED IN " + str(round(asset.GetExportTime(), 2))+"s\r\n")
        for file in asset.files:
            
            ExportLog += (file.file_path + "\\" + file.file_name + "\n")
        ExportLog += "\n"

    return ExportLog