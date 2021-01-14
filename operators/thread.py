import bpy
from bpy.props import IntProperty, FloatProperty
import bmesh
from mathutils import Vector, Matrix
from .. utils.selection import get_boundary_edges, get_edges_vert_sequences
from .. utils.math import average_locations
from .. utils.geometry import calculate_thread


class Thread(bpy.types.Operator):
    bl_idname = "machin3.add_thread"
    bl_label = "MACHIN3: Add Thread"
    bl_description = ""
    bl_options = {'REGISTER', 'UNDO'}

    radius: FloatProperty(name="Radius", min=0, default=1)
    segments: IntProperty(name="Segments", min=5, default=32)
    loops: IntProperty(name="Loops", min=1, default=4)

    depth: FloatProperty(name="Depth", description="Depth in Percentage of minor Diamater", min=0, max=100, default=5, subtype='PERCENTAGE')
    fade: FloatProperty(name="Fade", description="Percentage of Segments fading into inner Diameter", min=1, max=50, default=15, subtype='PERCENTAGE')

    h1: FloatProperty(name="Under Side", min=0, default=0.2, step=0.1)
    h2: FloatProperty(name="Width", min=0, default=0.05, step=0.1)
    h3: FloatProperty(name="Upper Side", min=0, default=0.2, step=0.1)
    h4: FloatProperty(name="Space", min=0, default=0.05, step=0.1)

    @classmethod
    def poll(cls, context):
        return context.mode == 'EDIT_MESH'

    def draw(self, context):
        layout = self.layout

        column = layout.column(align=True)

        row = column.row(align=True)
        row.prop(self, 'loops')
        row.prop(self, 'depth')
        row.prop(self, 'fade')

        row = column.row(align=True)
        row.prop(self, 'h1', text='')
        row.prop(self, 'h3', text='')
        row.prop(self, 'h2', text='')
        row.prop(self, 'h4', text='')

    def execute(self, context):
        active = context.active_object

        bm = bmesh.from_edit_mesh(active.data)
        bm.normal_update()

        selverts = [v for v in bm.verts if v.select]
        selfaces = [f for f in bm.faces if f.select]

        if selfaces:
            boundary = get_boundary_edges(selfaces)
            sequences = get_edges_vert_sequences(selverts, boundary, debug=False)

            # if there are 2 sequences
            if len(sequences) == 2:
                seq1, seq2 = sequences

                verts1, cyclic1 = seq1
                verts2, cyclic2 = seq2

                # if they are both cyclic and have the same amount of verts,and at least 5
                if cyclic1 == cyclic2 and cyclic1 is True and len(verts1) == len(verts2) and len(verts1) >= 5:
                    smooth = selfaces[0].smooth

                    if smooth:
                        active.data.use_auto_smooth = True

                    # deselect verts
                    for v in verts1 + verts2:
                        v.select_set(False)

                    bm.select_flush(False)

                    # set amount of segments
                    self.segments = len(verts1)

                    # get selection mid points
                    center1 = average_locations([v.co for v in verts1])
                    center2 = average_locations([v.co for v in verts2])

                    # get the radii, and set the radius as an average
                    radius1 = (center1 - verts1[0].co).length
                    radius2 = (center2 - verts2[0].co).length
                    self.radius = (radius1 + radius2) / 2

                    # create point coordinates and face indices
                    thread, bottom, top, height = calculate_thread(segments=self.segments, loops=self.loops, radius=self.radius, depth=self.depth / 100, h1=self.h1, h2=self.h2, h3=self.h3, h4=self.h4, fade=self.fade / 100)

                    # build the faces from those coords and indices
                    verts, faces = self.build_faces(bm, thread, bottom, top, smooth=smooth)

                    # scale the thread geometry to fit the selection height
                    selheight = (center1 - center2).length
                    bmesh.ops.scale(bm, vec=Vector((1, 1, selheight / height)), space=Matrix(), verts=verts)

                    # move the thread geometry into alignment with the first selection center
                    bmesh.ops.translate(bm, vec=center1, space=Matrix(), verts=verts)

                    # then rotate it into alignment too, this is done in two steps, first the up vectors are aligned
                    selup = (center2 - center1).normalized()

                    selrot = Vector((0, 0, 1)).rotation_difference(selup)
                    bmesh.ops.rotate(bm, cent=center1, matrix=selrot.to_matrix(), verts=verts, space=Matrix())

                    # then the first verts are aligned too, get the first vert from the active face if its part of the selection
                    if bm.faces.active and bm.faces.active in selfaces:
                        active_loops = [loop for v in bm.faces.active.verts if v in verts1 for loop in v.link_loops if loop.face == bm.faces.active]

                        if active_loops[0].link_loop_next.vert == active_loops[1].vert:
                            v1 = active_loops[1].vert
                        else:
                            v1 = active_loops[0].vert
                    else:
                        v1 = verts1[0]

                    threadvec = verts[0].co - center1
                    selvec = v1.co - center1

                    matchrot = threadvec.rotation_difference(selvec)
                    bmesh.ops.rotate(bm, cent=center1, matrix=matchrot.to_matrix(), verts=verts, space=Matrix())

                    # remove doubles
                    bmesh.ops.remove_doubles(bm, verts=verts + verts1 + verts2, dist=0.00001)

                    # remove the initially selected faces
                    bmesh.ops.delete(bm, geom=selfaces, context='FACES')

                    # recalculate the normals, usefull when doing inverted thread
                    bmesh.ops.recalc_face_normals(bm, faces=faces)

                    bmesh.update_edit_mesh(active.data)

                    return {'FINISHED'}
        return {'CANCELLED'}

    def build_faces(self, bm, thread, bottom, top, smooth=False):
        verts = []

        for co in thread[0]:
            v = bm.verts.new(co)
            verts.append(v)

        faces = []

        for ids in thread[1]:
            f = bm.faces.new([verts[idx] for idx in ids])
            f.smooth = smooth
            faces.append(f)

            if smooth:
                f.edges[0].smooth = False
                f.edges[-2].smooth = False

        bottom_verts = []

        for co in bottom[0]:
            v = bm.verts.new(co)
            bottom_verts.append(v)

        bottom_faces = []

        for ids in bottom[1]:
            f = bm.faces.new([bottom_verts[idx] for idx in ids])
            f.smooth = smooth
            bottom_faces.append(f)

            if smooth:
                if len(ids) == 4:
                    f.edges[-2].smooth = False
                else:
                    f.edges[-1].smooth = False

        top_verts = []

        for co in top[0]:
            v = bm.verts.new(co)
            top_verts.append(v)

        top_faces = []

        for ids in top[1]:
            f = bm.faces.new([top_verts[idx] for idx in ids])
            f.smooth = smooth
            top_faces.append(f)

            if smooth:
                if len(ids) == 4:
                    f.edges[0].smooth = False
                else:
                    f.edges[-1].smooth = False

        return [v for v in verts + bottom_verts + top_verts if v.is_valid], faces + bottom_faces + top_faces
