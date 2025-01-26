import bpy
from typing import List, TYPE_CHECKING
from .. import bfu_utils

from . import bfu_process_time_logs

def get_process_time_logs() -> List[bfu_process_time_logs.BFU_OT_ExportProcessTimeLog]:
    scene = bpy.context.scene
    return scene.bfu_export_process_time_logs

def start_time_log(process_name: str)-> bfu_process_time_logs.BFU_OT_ExportProcessTimeLog:
    scene = bpy.context.scene
    process_task = scene.bfu_export_process_time_logs.add()
    if TYPE_CHECKING:
        process_task: bfu_process_time_logs.BFU_OT_ExportProcessTimeLog
    process_task.start_process(process_name)
    return process_task

def clear_process_time_logs():
    scene = bpy.context.scene
    scene.bfu_export_process_time_logs.clear()

def get_process_time_logs_details():

    export_log = ""
    for log in get_process_time_logs():
        export_log += f"- {log.get_process_detail()} \n"

    return export_log