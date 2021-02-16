import bpy
from bpy.props import IntProperty
from math import degrees, radians
from mathutils import Matrix
from ... utils.registration import get_prefs


solid_show_overlays = True
material_show_overlays = False
rendered_show_overlays = False
wire_show_overlays = True


def get_description(context, shadetype):
    shading = context.space_data.shading
    overlay = context.space_data.overlay

    if shading.type == shadetype:
        return '%s Overlays for %s Shading' % ('Disable' if overlay.show_overlays else 'Enable', shadetype.capitalize())

    else:
        return 'Switch to %s shading' % (shadetype.capitalize())


class ShadeSolid(bpy.types.Operator):
    bl_idname = "machin3.shade_solid"
    bl_label = "Shade Solid"
    bl_options = {'REGISTER'}

    @classmethod
    def description(cls, context, properties):
        return get_description(context, 'SOLID')

    def execute(self, context):
        global solid_show_overlays

        overlay = context.space_data.overlay
        shading = context.space_data.shading

        # toggle overlays
        if shading.type == 'SOLID':
            solid_show_overlays = not solid_show_overlays
            overlay.show_overlays = solid_show_overlays

        # change shading to SOLID
        else:
            shading.type = 'SOLID'
            overlay.show_overlays = solid_show_overlays

        return {'FINISHED'}


class ShadeMaterial(bpy.types.Operator):
    bl_idname = "machin3.shade_material"
    bl_label = "Shade Material"
    bl_options = {'REGISTER'}

    @classmethod
    def description(cls, context, properties):
        return get_description(context, 'MATERIAL')

    def execute(self, context):
        global material_show_overlays

        overlay = context.space_data.overlay
        shading = context.space_data.shading

        # toggle overlays
        if shading.type == 'MATERIAL':
            material_show_overlays = not material_show_overlays
            overlay.show_overlays = material_show_overlays

        # change shading to MATERIAL
        else:
            shading.type = 'MATERIAL'
            overlay.show_overlays = material_show_overlays

        return {'FINISHED'}


class ShadeRendered(bpy.types.Operator):
    bl_idname = "machin3.shade_rendered"
    bl_label = "Shade Rendered"
    bl_options = {'REGISTER'}

    @classmethod
    def description(cls, context, properties):
        return get_description(context, 'RENDERED')

    def execute(self, context):
        global rendered_show_overlays

        overlay = context.space_data.overlay
        shading = context.space_data.shading

        # toggle overlays
        if shading.type == 'RENDERED':
            rendered_show_overlays = not rendered_show_overlays
            overlay.show_overlays = rendered_show_overlays

        # change shading to RENDERED
        else:
            shading.type = 'RENDERED'
            overlay.show_overlays = rendered_show_overlays

        return {'FINISHED'}


class ShadeWire(bpy.types.Operator):
    bl_idname = "machin3.shade_wire"
    bl_label = "Shade Wire"
    bl_options = {'REGISTER'}

    @classmethod
    def description(cls, context, properties):
        return get_description(context, 'WIREFRAME')

    def execute(self, context):
        global wire_show_overlays

        overlay = context.space_data.overlay
        shading = context.space_data.shading

        # toggle overlays
        if shading.type == 'WIREFRAME':
            wire_show_overlays = not wire_show_overlays
            overlay.show_overlays = wire_show_overlays

        # change shading to WIRE
        else:
            shading.type = 'WIREFRAME'
            overlay.show_overlays = wire_show_overlays

        return {'FINISHED'}


class ToggleOutline(bpy.types.Operator):
    bl_idname = "machin3.toggle_outline"
    bl_label = "Toggle Outline"
    bl_description = "Toggle Object Outlines"
    bl_options = {'REGISTER'}

    def execute(self, context):
        shading = context.space_data.shading

        shading.show_object_outline = not shading.show_object_outline

        return {'FINISHED'}


class ToggleCavity(bpy.types.Operator):
    bl_idname = "machin3.toggle_cavity"
    bl_label = "Toggle Cavity"
    bl_description = "Toggle Cavity (Screen Space Ambient Occlusion)"
    bl_options = {'REGISTER'}

    def execute(self, context):
        scene = context.scene

        scene.M3.show_cavity = not scene.M3.show_cavity

        return {'FINISHED'}


class ToggleCurvature(bpy.types.Operator):
    bl_idname = "machin3.toggle_curvature"
    bl_label = "Toggle Curvature"
    bl_description = "Toggle Curvature (Edge Highlighting)"
    bl_options = {'REGISTER'}

    def execute(self, context):
        scene = context.scene

        scene.M3.show_curvature = not scene.M3.show_curvature

        return {'FINISHED'}


matcap1_color_type = None


class MatcapSwitch(bpy.types.Operator):
    bl_idname = "machin3.matcap_switch"
    bl_label = "Matcap Switch"
    bl_description = "Quickly Switch between two Matcaps"
    bl_options = {'REGISTER'}

    @classmethod
    def poll(cls, context):
        shading = context.space_data.shading
        return shading.type == "SOLID" and shading.light == "MATCAP"

    def execute(self, context):
        shading = context.space_data.shading
        matcap1 = get_prefs().switchmatcap1
        matcap2 = get_prefs().switchmatcap2

        force_single = get_prefs().matcap2_force_single
        global matcap1_color_type

        if matcap1 and matcap2 and "NOT FOUND" not in [matcap1, matcap2]:
            if shading.studio_light == matcap1:
                shading.studio_light = matcap2

                if force_single and shading.color_type != 'SINGLE':
                    matcap1_color_type = shading.color_type
                    shading.color_type = 'SINGLE'

            elif shading.studio_light == matcap2:
                shading.studio_light = matcap1

                if force_single and matcap1_color_type:
                    shading.color_type = matcap1_color_type
                    matcap1_color_type = None

            else:
                shading.studio_light = matcap1

        return {'FINISHED'}


class RotateStudioLight(bpy.types.Operator):
    bl_idname = "machin3.rotate_studiolight"
    bl_label = "MACHIN3: Rotate Studiolight"
    bl_options = {'REGISTER', 'UNDO'}

    angle: IntProperty(name="Angle")

    @classmethod
    def description(cls, context, properties):
        return "Rotate Studio Light by %d degrees\nALT: Rotate visible lights too" % (int(properties.angle))

    def invoke(self, context, event):
        current = degrees(context.space_data.shading.studiolight_rotate_z)
        new = (current + self.angle)

        # deal with angles beyond 360
        if new > 360:
            new = new % 360

        # shift angle into blender's -180 to 180 range
        if new > 180:
            new = -180 + (new - 180)

        context.space_data.shading.studiolight_rotate_z = radians(new)

        if event.alt:
            rmx = Matrix.Rotation(radians(self.angle), 4, 'Z')
            lights = [obj for obj in context.visible_objects if obj.type == 'LIGHT']

            for light in lights:
                light.matrix_world = rmx @ light.matrix_world

        return {'FINISHED'}
