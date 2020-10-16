import bpy
from bpy.props import BoolProperty
from math import radians
from mathutils import Matrix
from .. utils.math import flatten_matrix
from .. utils.modifier import add_triangulate, remove_triangulate


class PrepareExport(bpy.types.Operator):
    bl_idname = "machin3.prepare_unity_export"
    bl_label = "MACHIN3: Prepare Unity Export"
    bl_options = {'REGISTER', 'UNDO'}

    prepare_only: BoolProperty(name="Only Prepare, don't export", description="Used by DECALmachine to skip Export even if the scene prop is set\nDECALmachine uses its own Export Operator Instead", default=False)

    @classmethod
    def poll(cls, context):
        return not [obj for obj in context.visible_objects if obj.M3.unity_exported]

    @classmethod
    def description(cls, context, properties):
        if context.scene.M3.unity_export:
            return "Prepare and Export %s objects" % ("selected" if context.selected_objects else "visible")
        else:
            return "Prepare %s objects for Export to Unity" % ("selected" if context.selected_objects else "visible")

    def execute(self, context):
        print("\nINFO: Preparing Unity Export")

        path = context.scene.M3.unity_export_path
        triangulate = context.scene.M3.unity_triangulate
        export = context.scene.M3.unity_export

        # force 'use_selection' mode, otherwise hidden child objects will be exported too if nothing is selected
        if not context.selected_objects:
            for obj in context.visible_objects:
                obj.select_set(True)

        sel = context.selected_objects

        # collect all current world matrices
        matrices = {obj: obj.matrix_world.copy() for obj in sel}

        # get root objects
        roots = [obj for obj in sel if not obj.parent]

        # get direct bone children, they need special treatment
        bone_children = [obj for obj in sel if obj.parent and obj.parent.type == 'ARMATURE' and obj.parent_bone]

        # prepare object transformations and modifiers
        for obj in roots:
            self.prepare_for_export(obj, sel, matrices, bone_children, triangulate=triangulate)

        if self.prepare_only:
            return {'FINISHED'}

        # export
        if export:
            bpy.ops.export_scene.fbx('EXEC_DEFAULT' if path else 'INVOKE_DEFAULT', filepath=path, use_selection=True, apply_scale_options='FBX_SCALE_ALL')

        return {'FINISHED'}

    def prepare_for_export(self, obj, sel, matrices, bone_children, triangulate=False, depth=0, child=False):
        '''
        recursively rotate an object and its children 90 degrees along X
        for meshes, compensate by rotating -90 along X
        also for meshes, store the original meshes for 2 reasons
        1. to easily restore the original mesh rotation
        2. to deal with instanced objects and also be able to restore these
        deal with modifers affecting by the rotations too, like mirror which needs a YZ swivel
        '''

        def prepare_object(obj, mx, depth, child):
            print("%sINFO: %sadjusting %s object's TRANSFORMATIONS: %s" % ('' if child else '\n', depth * '  ', 'child' if child else 'root', obj.name))
            obj.M3.unity_exported = True

            # get and store the current matrix
            mx = matrices[obj]
            obj.M3.pre_unity_export_mx = flatten_matrix(mx)

            obj.matrix_world = obj.matrix_world @ Matrix.Rotation(radians(90), 4, 'X')

        def prepare_modifiers(obj, swivel, depth):
            '''
            prepare/add modifiers
            '''

            # MIRROR MODS

            # skip swiveling if parent is direct bone child, bc the bone child was not transformed!
            if swivel:
                mirrors = [mod for mod in obj.modifiers if mod.type == 'MIRROR' and mod.show_viewport]

                if mirrors:
                    print("INFO: %sadjusting %s's MIRROR modifiers" % (depth * '  ', obj.name))

                    for mod in mirrors:
                        mod.use_axis[1:3] = mod.use_axis[2], mod.use_axis[1]
                        mod.use_bisect_axis[1:3] = mod.use_bisect_axis[2], mod.use_bisect_axis[1]
                        mod.use_bisect_flip_axis[1:3] = mod.use_bisect_flip_axis[2], mod.use_bisect_flip_axis[1]

        def add_triangulation(obj, triangulate):
            '''
            triangulate if the prop is set and the object is a mesh, also collapse all other mods!
            '''

            if triangulate and obj.type == 'MESH':
                print("INFO: %sadding %s's TRIANGULATE modifier" % (depth * '  ', obj.name))
                tri = add_triangulate(obj)

                for mod in [mod for mod in obj.modifiers if mod != tri]:
                    mod.show_expanded = False

        def prepare_mesh(obj, depth):
            '''
            apply the inverted transformation to the mesh to compensate for object transformation
            '''

            # store the original mesh and use a duplicate to be able to deal with instanced object, and to easily restore it later
            obj.M3.pre_unity_export_mesh = obj.data
            obj.data = obj.data.copy()

            print("INFO: %sadjusting %s's MESH to compensate" % (depth * '  ', obj.name))

            obj.data.transform(Matrix.Rotation(radians(-90), 4, 'X'))
            obj.data.update()

        def prepare_armature(obj, depth):
            '''
            apply the inverted transformation to the bones to compensate for object transformation
            '''

            # store the original armature and use a duplicate to be able to deal with instanced objects, and to easily restore it later
            obj.M3.pre_unity_export_armature = obj.data
            obj.data = obj.data.copy()

            print("INFO: %sadjusting %s's ARMATURE to compensate" % (depth * '  ', obj.name))
            obj.data.transform(Matrix.Rotation(radians(-90), 4, 'X'))

        def prepare_children(obj, bone_children, depth):
            if obj.children:
                depth += 1

                for child in obj.children:
                    if child in sel:
                        self.prepare_for_export(child, sel, matrices, bone_children, triangulate=triangulate, depth=depth, child=True)

        if obj in sel:

            if obj in bone_children:
                print("%sINFO: %skeeping %s object's TRANSFORMATIONS: %s" % ('' if child else '\n', depth * '  ', 'child' if child else 'root', obj.name))
                obj.M3.unity_exported = True

            else:

                # OBJECT TRANSFORM

                prepare_object(obj, matrices[obj], depth, child)

                # MODIFIERS

                prepare_modifiers(obj, swivel=False if obj.parent and obj.parent in bone_children else True, depth=depth)


                # OBJECT DATA

                if obj.type == 'MESH':
                    prepare_mesh(obj, depth)

                elif obj.type == 'ARMATURE':
                    prepare_armature(obj, depth)


            # TRIANGULATE

            add_triangulation(obj, triangulate)


            # OBJECT CHILDREN

            prepare_children(obj, bone_children, depth)


class RestoreExport(bpy.types.Operator):
    bl_idname = "machin3.restore_unity_export"
    bl_label = "MACHIN3: Restore Unity Export"
    bl_description = "Restore Pre-Export Object Transformations, Meshes and Modifiers"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return [obj for obj in context.visible_objects if obj.M3.unity_exported]

    def execute(self, context):
        print("\nINFO: Restoring Pre-Unity-Export Status")

        detriangulate = context.scene.M3.unity_triangulate

        exported = [obj for obj in context.visible_objects if obj.M3.unity_exported]
        meshes = []
        armatures = []

        # get root objects
        roots = [obj for obj in exported if not obj.parent]

        # get direct bone children, they need special treatment
        bone_children = [obj for obj in exported if obj.parent and obj.parent.type == 'ARMATURE' and obj.parent_bone]

        # restore objects, meshesand modifiers
        for obj in roots:
            self.restore_exported(obj, exported, bone_children, meshes, armatures, detriangulate=detriangulate)


        # remove the unique meshes
        bpy.data.batch_remove(meshes)

        # remove the unique armatures
        bpy.data.batch_remove(armatures)

        return {'FINISHED'}

    def restore_exported(self, obj, exported, bone_children, meshes, armatures, detriangulate=True, depth=0, child=False):
        '''
        recursively restore an the original transformation and data of an exported object and its children
        '''

        def restore_object(obj, depth, child):
            print("%sINFO: %srestoring %s object's TRANSFORMATIONS: %s" % ('' if child else '\n', depth * '  ', 'child' if child else 'root', obj.name))

            obj.matrix_world = obj.M3.pre_unity_export_mx
            obj.M3.pre_unity_export_mx = flatten_matrix(Matrix())
            obj.M3.unity_exported = False

        def restore_modifiers(obj, swivel, depth):
            '''
            restore/remove modifiers
            '''

            # MIRROR MODS

            if swivel:

                mirrors = [mod for mod in obj.modifiers if mod.type == 'MIRROR' and mod.show_viewport]

                if mirrors:
                    print("INFO: %srestoring %s's mirror modifiers" % (depth * '  ', obj.name))

                    for mod in mirrors:
                        mod.use_axis[1:3] = mod.use_axis[2], mod.use_axis[1]
                        mod.use_bisect_axis[1:3] = mod.use_bisect_axis[2], mod.use_bisect_axis[1]
                        mod.use_bisect_flip_axis[1:3] = mod.use_bisect_flip_axis[2], mod.use_bisect_flip_axis[1]

        def remove_triangulation(obj, detriangulate):
            if detriangulate:
                if remove_triangulate(obj):
                    print("INFO: %sremoved %s's TRIANGULATE modifier" % (depth * '  ', obj.name))

        def restore_mesh(obj, depth, meshes):
            print("INFO: %srestoring %s's original pre-export MESH" % (depth * '  ', obj.name))
            meshes.append(obj.data)

            obj.data = obj.M3.pre_unity_export_mesh
            obj.M3.pre_unity_export_mesh = None

        def restore_armature(obj, depth, armatures):
            print("INFO: %srestoring %s's original pre-export ARMATURE" % (depth * '  ', obj.name))
            armatures.append(obj.data)

            obj.data = obj.M3.pre_unity_export_armature
            obj.M3.pre_unity_export_armature = None

        def restore_children(obj, bone_children, depth):
            if obj.children:
                depth += 1

                for child in obj.children:
                    if child in exported:
                        self.restore_exported(child, exported, bone_children, meshes, armatures, detriangulate=detriangulate, depth=depth, child=True)

        if obj in exported:

            # BONE CHILDREN

            if obj in bone_children:
                print("%sINFO: %skeeping %s object's TRANSFORMATIONS: %s" % ('' if child else '\n', depth * '  ', 'child' if child else 'root', obj.name))
                obj.M3.unity_exported = False

            else:

                # OBJECT TRANSFORM

                restore_object(obj, depth, child)


                # MODIFIERS

                restore_modifiers(obj, swivel=False if obj.parent and obj.parent in bone_children else True, depth=depth)


                # OBJECT DATA

                if obj.type == 'MESH' and obj.M3.pre_unity_export_mesh:
                    restore_mesh(obj, depth, meshes)

                elif obj.type == 'ARMATURE' and obj.M3.pre_unity_export_armature:
                    restore_armature(obj, depth, armatures)


            # TRIANGULATION

            remove_triangulation(obj, detriangulate)


            # OBJECT CHILDREN

            restore_children(obj, bone_children, depth)
