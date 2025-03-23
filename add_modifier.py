import bpy

bl_info = {
    "name": "Add Modifier",
    "author": "Jakub Jaszewski",
    "description": "Add modifier to selected objects.",
    "version": (1, 0),
    "blender": (4, 2, 0),
    "location": "3D Viewport",
    "category": "Object",
}

addon_keymaps = []

class AddModifier(bpy.types.Operator):
    bl_idname = "custom.add_modifier"
    bl_label = "Add Modifier"
    bl_description = "Add Modifier of Choice to Selected Objects"
    bl_options = {'REGISTER', 'UNDO'}

    modifier_type: bpy.props.StringProperty()

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        bpy.context.view_layer.objects.active = context.active_object
        bpy.ops.wm.call_menu(name="OBJECT_MT_modifier_add")
        bpy.app.driver_namespace["add_modifier_operator"] = self
        context.window_manager.modal_handler_add(self)

        return {'RUNNING_MODAL'}

    def modal(self, context, event):
        act = context.active_object
        sel = context.selected_objects

        if context.active_operator and context.active_operator.bl_idname == "OBJECT_OT_modifier_add":
            mod = context.active_operator.properties.get('type')
            # ng = context.active_operator.properties.get('asset_library_identifier')
            # print(mod)
            # print(ng)
            modifier_types = bpy.types.Modifier.bl_rna.properties['type'].enum_items
            # nodegroup_types = bpy.types.Modifier.bl_rna.properties['asset_library_identifier'].enum_items
            mod_type = None

            for modifier_type in modifier_types:
                if modifier_type.value == mod:
                    mod_type = modifier_type.identifier
                    break

            for obj in sel:
                if obj != act:
                    context.view_layer.objects.active = obj
                    bpy.ops.object.modifier_add(type=mod_type)

            del bpy.app.driver_namespace["add_modifier_operator"]

            return {'FINISHED'}

        elif event.type in {'RIGHTMOUSE', 'ESC'}:
            print("Operation Cancelled")
            del bpy.app.driver_namespace["add_modifier_operator"]

            return {'CANCELLED'}

        return {'PASS_THROUGH'}

def register_hotkey():
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon

    if kc:
        km = wm.keyconfigs.addon.keymaps.new(name='Object Mode', space_type='EMPTY')
        kmi = km.keymap_items.new(AddModifier.bl_idname, 'A', 'PRESS', ctrl=True, shift=True)
        addon_keymaps.append((km, kmi))

def unregister_hotkey():
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon

    if kc:
        for km, kmi in addon_keymaps:
            km.keymap_items.remove(kmi)
        addon_keymaps.clear()

def register():
    bpy.utils.register_class(AddModifier)
    register_hotkey()

def unregister():
    bpy.utils.unregister_class(AddModifier)
    unregister_hotkey()

if __name__ == "__main__":
    register()

