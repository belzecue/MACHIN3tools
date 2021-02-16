import bpy
from bpy.props import EnumProperty, BoolProperty
import bmesh
from mathutils import Vector, Matrix, geometry
from ... utils.math import get_center_between_verts, create_rotation_difference_matrix_from_quat, get_loc_matrix, create_selection_bbox, get_right_and_up_axes
from ... items import axis_items, align_type_items, axis_mapping_dict, align_direction_items, align_orientation_items
from ... utils.selection import get_selected_vert_sequences
from ... utils.ui import popup_message


class AlignEditMesh(bpy.types.Operator):
    bl_idname = "machin3.align_editmesh"
    bl_label = "MACHIN3: Align (Edit Mesh)"
    bl_options = {'REGISTER', 'UNDO'}
    bl_description = "Local Space Align\nALT: World Space Align\nCTRL: Cursor Space Align"

    type: EnumProperty(name="Type", items=align_type_items, default="MINMAX")

    axis: EnumProperty(name="Axis", items=axis_items, default="X")
    direction: EnumProperty(name="Axis", items=align_direction_items, default="LEFT")

    orientation: EnumProperty(name="Orientation", items=align_orientation_items, default="LOCAL")

    @classmethod
    def poll(cls, context):
        if context.mode == "EDIT_MESH":
            active = context.active_object
            bm = bmesh.from_edit_mesh(active.data)
            return [v for v in bm.verts if v.select]

    def invoke(self, context, event):
        if event.alt and event.ctrl:
            popup_message("Hold down ATL, CTRL or neither, not both!", title="Invalid Modifier Keys")
            return {'CANCELLED'}

        self.orientation = 'WORLD' if event.alt else 'CURSOR' if event.ctrl else 'LOCAL'

        self.align(context, self.type, axis_mapping_dict[self.axis], self.direction, self.orientation)
        return {'FINISHED'}

    def align(self, context, type, axis, direction, orientation):
        active = context.active_object

        mx = active.matrix_world if orientation == 'LOCAL' else context.scene.cursor.matrix if orientation == 'CURSOR' else Matrix()

        mode = context.scene.M3.align_mode

        # in VIEW mode the axis is calculated from from viewport direction giving in the pie
        if mode == 'VIEW':
            axis_right, axis_up, flip_right, flip_up = get_right_and_up_axes(context, mx=mx)

            if type == 'MINMAX':
                axis = axis_right if direction in ['RIGHT', 'LEFT'] else axis_up

            elif type in ['ZERO', 'AVERAGE', 'CURSOR']:
                axis = axis_right if direction == "HORIZONTAL" else axis_up

        bm = bmesh.from_edit_mesh(active.data)
        bm.normal_update()
        bm.verts.ensure_lookup_table()

        verts = [v for v in bm.verts if v.select]

        # axis coordinates in local space
        if orientation == 'LOCAL':
            axiscoords = [v.co[axis] for v in verts]

        # coordinates in world space
        elif orientation == 'WORLD':
            axiscoords = [(active.matrix_world @ v.co)[axis] for v in verts]

        # coordinates in cursor space
        elif orientation == 'CURSOR':
            axiscoords = [(mx.inverted_safe() @ active.matrix_world @ v.co)[axis] for v in verts]

        # get min or max target value
        if type == "MIN":
            target = min(axiscoords)

        elif type == "MAX":
            target = max(axiscoords)

        # min or max in VIEW mode
        elif type == 'MINMAX':
            if direction == 'RIGHT':
                target = min(axiscoords) if flip_right else max(axiscoords)

            elif direction == 'LEFT':
                target = max(axiscoords) if flip_right else min(axiscoords)

            elif direction == 'TOP':
                target = min(axiscoords) if flip_up else max(axiscoords)

            elif direction == 'BOTTOM':
                target = max(axiscoords) if flip_up else min(axiscoords)

        # get the zero target value
        elif type == "ZERO":
            target = 0

        # get the average target value
        elif type == "AVERAGE":
            target = sum(axiscoords) / len(axiscoords)

        # get cursor target value
        elif type == "CURSOR":
            if orientation == 'LOCAL':
                c_world = context.scene.cursor.location
                c_local = mx.inverted() @ c_world
                target = c_local[axis]

            elif orientation == 'WORLD':
                target = context.scene.cursor.location[axis]

            elif orientation == 'CURSOR':
                target = 0

        # set the new coordinates
        for v in verts:
            if orientation == 'LOCAL':
                v.co[axis] = target

            elif orientation == 'WORLD':
                # bring vertex coords into world space
                world_co = active.matrix_world @ v.co

                # set the target value
                world_co[axis] = target

                # bring it back into local space
                v.co = active.matrix_world.inverted_safe() @ world_co

            elif orientation == 'CURSOR':
                # bring vertex coords into cursor space
                cursor_co = mx.inverted_safe() @ active.matrix_world @ v.co

                # set the target value
                cursor_co[axis] = target

                # bring it back into local space
                v.co = active.matrix_world.inverted_safe() @ mx @ cursor_co

        bm.normal_update()
        bmesh.update_edit_mesh(active.data)


class CenterEditMesh(bpy.types.Operator):
    bl_idname = "machin3.center_editmesh"
    bl_label = "MACHIN3: Center (Edit Mesh)"
    bl_options = {'REGISTER', 'UNDO'}
    bl_description = "Local Space Center\nALT: World Space Center\nCTRL: Cursor Space Center"

    axis: EnumProperty(name="Axis", items=axis_items, default="X")
    direction: EnumProperty(name="Axis", items=align_direction_items, default="HORIZONTAL")

    # local: BoolProperty(name="Local Space", default=True)
    orientation: EnumProperty(name="Orientation", items=align_orientation_items, default="LOCAL")

    @classmethod
    def poll(cls, context):
        if context.mode == "EDIT_MESH":
            active = context.active_object
            bm = bmesh.from_edit_mesh(active.data)
            return [v for v in bm.verts if v.select]

    def invoke(self, context, event):
        if event.alt and event.ctrl:
            popup_message("Hold down ATL, CTRL or neither, not both!", title="Invalid Modifier Keys")
            return {'CANCELLED'}

        self.orientation = 'WORLD' if event.alt else 'CURSOR' if event.ctrl else 'LOCAL'

        self.center(context, axis_mapping_dict[self.axis], self.direction, self.orientation)
        return {'FINISHED'}

    def center(self, context, axis, direction, orientation):
        active = context.active_object
        mx = active.matrix_world if orientation == 'LOCAL' else context.scene.cursor.matrix if orientation == 'CURSOR' else Matrix()

        mode = context.scene.M3.align_mode

        # calculate axis from viewport
        if mode == 'VIEW':
            axis_right, axis_up, flip_right, flip_up = get_right_and_up_axes(context, mx=mx)

            axis = axis_right if direction == "HORIZONTAL" else axis_up

        bm = bmesh.from_edit_mesh(active.data)
        bm.normal_update()
        bm.verts.ensure_lookup_table()

        verts = [v for v in bm.verts if v.select]

        # use the single vert's coordinate as the origin
        if len(verts) == 1:
            origin = verts[0].co

        # use the midpoint between two verts/one edge as the origin
        elif len(verts) == 2:
            origin = get_center_between_verts(*verts)

        # use the bounding box center as the origin
        else:
            _, origin = create_selection_bbox([v.co for v in verts])

        # the target location will be the origin with the axis zeroed out
        if orientation == 'LOCAL':
            target = origin.copy()
            target[axis] = 0

            # create translation matrix
            mxt = get_loc_matrix(target - origin)

        elif orientation == 'WORLD':
            # bring into world space
            origin = active.matrix_world @ origin
            target = origin.copy()
            target[axis] = 0

            # create translation matrix (in local space again)
            mxt = get_loc_matrix(active.matrix_world.inverted().to_3x3() @ (target - origin))

        elif orientation == 'CURSOR':
            # bring into cursor space
            origin = mx.inverted_safe() @ active.matrix_world @ origin
            target = origin.copy()
            target[axis] = 0

            # create translation matrix (in local space again)
            mxt = get_loc_matrix(active.matrix_world.inverted().to_3x3() @ mx.to_3x3() @ (target - origin))

        # move the selection
        for v in verts:
            v.co = mxt @ v.co

        bmesh.update_edit_mesh(active.data)


class AlignObjectToEdge(bpy.types.Operator):
    bl_idname = "machin3.align_object_to_edge"
    bl_label = "MACHIN3: Align Object to Edge"
    bl_description = "Align one or more objects to edge in active object\nALT: Snap objects to edge by proximity\nCTRL: Snap objects to edge by midpoint"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        if context.mode == 'EDIT_MESH':
            active = context.active_object
            sel = [obj for obj in context.selected_objects if obj != active]

            if active and sel:
                for obj in [active] + sel:
                    bm = bmesh.from_edit_mesh(obj.data)

                    if len([e for e in bm.edges if e.select]) != 1:
                        return False
                return True

    def invoke(self, context, event):
        target = context.active_object
        objs = [obj for obj in context.selected_objects if obj != target]

        for obj in objs:

            # get alignment edges
            v_obj, v_target, mid, coords = self.get_vectors_from_alignment_edges(obj, target)

            if v_obj and v_target:
                loc, _, _ = obj.matrix_world.decompose()

                # get rotation matrix
                rmx = create_rotation_difference_matrix_from_quat(v_obj, v_target)

                # bring into the origin, rotate and bring back
                obj.matrix_world = get_loc_matrix(loc) @ rmx @ get_loc_matrix(-loc) @ obj.matrix_world

                # snap the objects together
                if event.alt or event.ctrl:
                    # the mid point was returned in local space, and is now brough into world space AFTER the obj was rotated
                    mid_world = obj.matrix_world @ mid

                    # determine closed point on target edge to obj edge mid ponit
                    co, _ = geometry.intersect_point_line(mid_world, *coords)

                    # snap the obj to the edge
                    if co:
                        obj.matrix_world = Matrix.Translation(co - mid_world) @ obj.matrix_world

                        # snap the edge midpoints together as well
                        if event.ctrl:
                            mid_target = (coords[0] + coords[1]) / 2
                            mid_obj = obj.matrix_world @ mid

                            mxt = Matrix.Translation(mid_target - mid_obj)

                            obj.matrix_world = mxt @ obj.matrix_world

        return {'FINISHED'}

    def get_vectors_from_alignment_edges(self, obj, target):
        """
        return vectors from both edges, oriented to point in the same direction
        also return the obj edge's midpoint(local space) as well as both vertex coordinates of the target edge (world space)
        """

        bm = bmesh.from_edit_mesh(obj.data)
        edges = [e for e in bm.edges if e.select]

        v_obj = (obj.matrix_world.to_3x3() @ Vector(edges[0].verts[0].co - edges[0].verts[1].co)).normalized() if len(edges) == 1 else None
        mid = get_center_between_verts(*edges[0].verts) if edges else None

        bm = bmesh.from_edit_mesh(target.data)
        edges = [e for e in bm.edges if e.select]

        v_target = (target.matrix_world.to_3x3() @ Vector(edges[0].verts[0].co - edges[0].verts[1].co)).normalized() if len(edges) == 1 else None
        coords = [target.matrix_world @ v.co for v in edges[0].verts] if edges else None

        if v_obj and v_target:

            # align them both the same
            dot = v_obj.dot(v_target)

            if dot < 0:
                v_obj.negate()

            return v_obj, v_target, mid, coords
        return None, None, None, None


class AlignObjectToVert(bpy.types.Operator):
    bl_idname = "machin3.align_object_to_vert"
    bl_label = "MACHIN3: Align Object to Vert"
    bl_description = "Align one or more objects to vertice in active object"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        if context.mode == 'EDIT_MESH':
            active = context.active_object
            sel = [obj for obj in context.selected_objects if obj != active]

            if active and sel:
                for obj in [active] + sel:
                    bm = bmesh.from_edit_mesh(obj.data)

                    if len([v for v in bm.verts if v.select]) != 1:
                        return False
                return True

    def invoke(self, context, event):
        target = context.active_object
        objs = [obj for obj in context.selected_objects if obj != target]

        mx_target = target.matrix_world
        bm_target = bmesh.from_edit_mesh(target.data)
        v_target = [v for v in bm_target.verts if v.select][0]

        for obj in objs:
            mx_obj = obj.matrix_world
            bm_obj = bmesh.from_edit_mesh(obj.data)
            v_obj = [v for v in bm_obj.verts if v.select][0]

            obj.matrix_world = Matrix.Translation(mx_target @ v_target.co - mx_obj @ v_obj.co) @ obj.matrix_world
        return {'FINISHED'}


class Straighten(bpy.types.Operator):
    bl_idname = "machin3.straighten"
    bl_label = "MACHIN3: Straighten"
    bl_description = "Straighten verts or edges"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        if context.mode == 'EDIT_MESH':
            bm = bmesh.from_edit_mesh(context.active_object.data)
            return len([v for v in bm.verts if v.select]) > 2 and not [f for f in bm.faces if f.select]

    def execute(self, context):
        active = context.active_object

        bm = bmesh.from_edit_mesh(active.data)
        bm.normal_update()
        bm.verts.ensure_lookup_table()

        verts = [v for v in bm.verts if v.select]

        # if in edge mode, check if there are connected vert sequences, that are non-cyclic and have at least 3 verts, then straighten each sequence
        if context.scene.tool_settings.mesh_select_mode[1]:
            sequences = get_selected_vert_sequences(verts.copy(), ensure_seq_len=True, debug=False)

            if sequences:
                vert_lists = [seq for seq, cyclic in sequences if len(seq) > 2 and not cyclic]

                if vert_lists:
                    for verts in vert_lists:
                        v_start = verts[0]
                        v_end = verts[-1]

                        self.straighten(bm, verts, v_start, v_end)

                    bmesh.update_edit_mesh(active.data)

                    return {'FINISHED'}

        # if the sequence check didn't produce actionable results, try to get start and end verts from selection history
        v_start, v_end = self.get_start_and_end_from_history(bm)

        # and if that fails as well, pick the most distant ones
        if not v_start:
            v_start, v_end = self.get_start_and_end_from_distance(verts)

        # straighten
        self.straighten(bm, verts, v_start, v_end)

        bmesh.update_edit_mesh(active.data)

        return {'FINISHED'}

    def straighten(self, bm, verts, v_start, v_end):
        # move all verts but the start and end verts on the vector described by the two
        verts.remove(v_start)
        verts.remove(v_end)

        for v in verts:
            co, _ = geometry.intersect_point_line(v.co, v_start.co, v_end.co)
            v.co = co

        bm.normal_update()

    def get_start_and_end_from_distance(self, verts):
        # get vert pairs from selection, using a set of frozensets removes duplicate pairings like [v, v2] and [v2, v], etc
        pairs = {frozenset([v, v2]) for v in verts for v2 in verts if v2 != v}

        # get distances for each vert pair
        distances = [((v2.co - v.co).length, (v, v2)) for v, v2 in pairs]

        # get the straight's start and end verts based on distance
        return max(distances, key=lambda x: x[0])[1]

    def get_start_and_end_from_history(self, bm):
        history = list(bm.select_history)

        # check if the selection history has at least 2 verts - and if so, determine the start and end vert from it
        if len(history) >= 2 and all([isinstance(h, bmesh.types.BMVert) for h in history]):
            return history[0], history[-1]
        return None, None
