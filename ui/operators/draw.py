import bpy
from bpy.props import FloatProperty, StringProperty, FloatVectorProperty
from ... utils.draw import draw_label


class DrawLabel(bpy.types.Operator):
    bl_idname = "machin3.draw_label"
    bl_label = "MACHIN3: draw_label"
    bl_description = ""
    bl_options = {'INTERNAL'}

    text: StringProperty(name="Text to draw the HUD", default='Text')
    coords: FloatVectorProperty(name='Screen Coordinates', size=2, default=(100, 100))
    color: FloatVectorProperty(name='Screen Coordinates', size=3, default=(1, 1, 1))

    time: FloatProperty(name="", default=1, min=0.1)
    alpha: FloatProperty(name="Alpha", default=0.5, min=0.1, max=1)

    @classmethod
    def poll(cls, context):
        return context.space_data.type == 'VIEW_3D'

    def draw_HUD(self, context):
        alpha = self.countdown / self.time * self.alpha
        draw_label(context, title=self.text, coords=self.coords, color=self.color, alpha=alpha)


    def modal(self, context, event):
        context.area.tag_redraw()

        # FINISH when countdown is 0

        if self.countdown < 0:
            # print("Countdown of %d seconds finished" % (self.time))

            # remove time handler
            context.window_manager.event_timer_remove(self.TIMER)

            # remove draw handler
            bpy.types.SpaceView3D.draw_handler_remove(self.HUD, 'WINDOW')
            return {'FINISHED'}

        # COUNT DOWN

        if event.type == 'TIMER':
            self.countdown -= 0.1

        return {'PASS_THROUGH'}

    def execute(self, context):
        self.HUD = bpy.types.SpaceView3D.draw_handler_add(self.draw_HUD, (context, ), 'WINDOW', 'POST_PIXEL')

        # time handler
        self.TIMER = context.window_manager.event_timer_add(0.1, window=context.window)

        # initalize time from prefs
        self.countdown = self.time

        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}
