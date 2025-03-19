import bpy
from typing import List, TYPE_CHECKING
from .. import bfu_utils

from . import bfu_process_time_logs

class safe_time_log_handle():
    # I need to store a proxy class 
    # because BFU_OT_ExportProcessTimeLog ref is lost 
    # when scene update and this produce a crash.

    def __init__(self, process_id):
        self.process_id = process_id
        self.should_print_log = False

        self.print_log(self.get_process_info(), "Start!")

    def get_process_ref(self) -> bfu_process_time_logs.BFU_OT_ExportProcessTimeLog:
        scene = bpy.context.scene
        for process_task in scene.bfu_export_process_time_logs:
            if TYPE_CHECKING:
                process_task: bfu_process_time_logs.BFU_OT_ExportProcessTimeLog
            if process_task.process_id == self.process_id:
                return process_task

    def get_process_info(self):
        return self.get_process_ref().process_info

    def end_time_log(self):
        process_task = self.get_process_ref()
        self.print_log(process_task.process_info, "End!")
        process_task.finish_process()
            
    def print_log(self, *args):
        if self.should_print_log:
            print(*args)
                


def get_process_time_logs() -> List[bfu_process_time_logs.BFU_OT_ExportProcessTimeLog]:
    scene = bpy.context.scene
    return scene.bfu_export_process_time_logs

def get_process_time_unique_id():
    scene = bpy.context.scene
    prefix = "pid_"
    index = str(len(scene.bfu_export_process_time_logs))
    return prefix + index

def start_time_log(process_info: str, sub_step = 0)-> safe_time_log_handle:
    process_id = get_process_time_unique_id()

    scene = bpy.context.scene
    process_task = scene.bfu_export_process_time_logs.add()
    if TYPE_CHECKING:
        process_task: bfu_process_time_logs.BFU_OT_ExportProcessTimeLog
    process_task.start_process(process_id, process_info, sub_step)
    process_task_proxy = safe_time_log_handle(process_id)
    return process_task_proxy

def clear_process_time_logs():
    scene = bpy.context.scene
    scene.bfu_export_process_time_logs.clear()

def get_process_time_logs_details():

    export_log = ""
    for log in get_process_time_logs():
        export_log += f"- {log.get_process_detail()} \n"

    return export_log