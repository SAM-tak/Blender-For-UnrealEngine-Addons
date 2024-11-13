import os
import bpy
from .. import bfu_export_nomenclature
from .. import bfu_export_filter
from .. import bfu_export_process

class BFU_PT_Export(bpy.types.Panel):
    # Is Export panel

    bl_idname = "BFU_PT_Export"
    bl_label = "UE AE Export"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Unreal Engine"


    class BFU_MT_NomenclaturePresets(bpy.types.Menu):
        bl_label = 'Nomenclature Presets'
        preset_subdir = 'blender-for-unrealengine/nomenclature-presets'
        preset_operator = 'script.execute_preset'
        draw = bpy.types.Menu.draw_preset

    from bl_operators.presets import AddPresetBase

    class BFU_OT_AddNomenclaturePreset(AddPresetBase, bpy.types.Operator):
        bl_idname = 'object.add_nomenclature_preset'
        bl_label = 'Add or remove a preset for Nomenclature'
        bl_description = 'Add or remove a preset for Nomenclature'
        preset_menu = 'BFU_MT_NomenclaturePresets'

        def get_export_global_preset_propertys():
            preset_values = []
            preset_values += bfu_export_nomenclature.bfu_export_nomenclature_props.get_preset_values()
            preset_values += bfu_export_filter.bfu_export_filter_props.get_preset_values()
            preset_values += bfu_export_process.bfu_export_process_props.get_preset_values()
            return preset_values

        # Common variable used for all preset values
        preset_defines = [
                            'obj = bpy.context.object',
                            'scene = bpy.context.scene'
                         ]

        # Properties to store in the preset
        preset_values = get_export_global_preset_propertys()

        # Directory to store the presets
        preset_subdir = 'blender-for-unrealengine/nomenclature-presets'


    def draw(self, context):
        
        layout = self.layout

        # Presets
        row = self.layout.row(align=True)
        row.menu('BFU_MT_NomenclaturePresets', text='Export Presets')
        row.operator('object.add_nomenclature_preset', text='', icon='ADD')
        row.operator(
            'object.add_nomenclature_preset',
            text='',
            icon='REMOVE').remove_active = True

        # Export sections
        bfu_export_nomenclature.bfu_export_nomenclature_ui.draw_ui(layout, context)
        bfu_export_filter.bfu_export_filter_ui.draw_ui(layout, context)
        bfu_export_process.bfu_export_process_ui.draw_ui(layout, context)

# -------------------------------------------------------------------
#   Register & Unregister
# -------------------------------------------------------------------

classes = (
    BFU_PT_Export,
    BFU_PT_Export.BFU_MT_NomenclaturePresets,
    BFU_PT_Export.BFU_OT_AddNomenclaturePreset,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
