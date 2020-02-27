
classes = {"CORE": [("ui.UILists", [("AppendMatsUIList", "")]),
                    ("properties", [("AppendMatsCollection", "")]),
                    ("properties", [("HistoryObjectsCollection", ""),
                                    ("HistoryUnmirroredCollection", ""),
                                    ("HistoryEpochCollection", ""),
                                    ("M3SceneProperties", "")]),
                    ("preferences", [("MACHIN3toolsPreferences", "")]),
                    ("operators.quadsphere", [("QuadSphere", "quadsphere")])],

           "SMART_VERT": [("operators.smart_vert", [("SmartVert", "smart_vert")])],
           "SMART_EDGE": [("operators.smart_edge", [("SmartEdge", "smart_edge")])],
           "SMART_FACE": [("operators.smart_face", [("SmartFace", "smart_face")])],
           "CLEAN_UP": [("operators.clean_up", [("CleanUp", "clean_up")])],
           "CLIPPING_TOGGLE": [("operators.clipping_toggle", [("ClippingToggle", "clipping_toggle")])],
           "FOCUS": [("operators.focus", [("Focus", "focus")])],
           "MIRROR": [("operators.mirror", [("Mirror", "mirror"),
                                            ("Unmirror", "unmirror")])],
           "ALIGN": [("operators.align", [("Align", "align")])],
           "APPLY": [("operators.apply", [("Apply", "apply_transformations")])],
           "SELECT": [("operators.select", [("SelectCenterObjects", "select_center_objects")])],
           "MESH_CUT": [("operators.mesh_cut", [("MeshCut", "mesh_cut")])],
           "CUSTOMIZE": [("operators.customize", [("Customize", "customize"),
                                                  ("RestoreKeymaps", "restore_keymaps")])],

           "FILEBROWSER": [("operators.filebrowser", [("Open", "filebrowser_open"),
                                                      ("Toggle", "filebrowser_toggle")])],

           "MODES_PIE": [("ui.pies", [("PieModes", "modes_pie")]),
                         ("ui.operators.modes", [("EditMode", "edit_mode"),
                                                 ("MeshMode", "mesh_mode")]),
                         ("ui.operators.modes", [("ImageMode", "image_mode"),
                                                 ("UVMode", "uv_mode"),
                                                 ("SurfaceDrawMode", "surface_draw_mode")]),
                         ("ui.operators.open_blend", [("OpenLibraryBlend", "open_library_blend")])],

           "SAVE_PIE": [("ui.pies", [("PieSave", "save_pie")]),
                        ("ui.menus", [("MenuAppendMaterials", "append_materials")]),
                        ("ui.operators.save", [("New", "new"),
                                               ("Save", "save"),
                                               ("SaveIncremental", "save_incremental"),
                                               ("LoadMostRecent", "load_most_recent"),
                                               ("LoadPrevious", "load_previous"),
                                               ("LoadNext", "load_next")]),
                        ("ui.operators.save", [("AppendWorld", "append_world"),
                                               ("AppendMaterial", "append_material"),
                                               ("LoadWorldSource", "load_world_source"),
                                               ("LoadMaterialsSource", "load_materials_source")]),
                        ("ui.operators.appendmats", [("AddSeparator", "add_separator"),
                                                     ("Populate", "populate_appendmats"),
                                                     ("Move", "move_appendmat"),
                                                     ("Rename", "rename_appendmat"),
                                                     ("Clear", "clear_appendmats"),
                                                     ("Remove", "remove_appendmat")])],
           "SHADING_PIE": [("ui.pies", [("PieShading", "shading_pie")]),
                           ("ui.operators.shading", [("ShadeSolid", "shade_solid"),
                                                     ("ShadeMaterial", "shade_material"),
                                                     ("ShadeRendered", "shade_rendered"),
                                                     ("ShadeWire", "shade_wire")]),
                           ("ui.operators.toggle_grid_wire_outline", [("ToggleGrid", "toggle_grid"),
                                                                      ("ToggleWireframe", "toggle_wireframe"),
                                                                      ("ToggleOutline", "toggle_outline"),
                                                                      ("ToggleCavity", "toggle_cavity"),
                                                                      ("ToggleCurvature", "toggle_curvature")]),
                           ("ui.operators.shade_smooth_flat_auto", [("ShadeSmooth", "shade_smooth"),
                                                                    ("ShadeFlat", "shade_flat"),
                                                                    ("ToggleAutoSmooth", "toggle_auto_smooth")]),
                           ("ui.operators.colorize", [("ColorizeMaterials", "colorize_materials"),
                                                      ("ColorizeObjectsFromActive", "colorize_objects_from_active"),
                                                      ("ColorizeObjectsFromCollections", "colorize_objects_from_collections"),
                                                      ("ColorizeObjectsFromMaterials", "colorize_objects_from_materials")]),
                           ("ui.operators.matcap_switch", [("MatcapSwitch", "matcap_switch")]),
                           ("ui.operators.toggle_object_axes", [("ToggleObjectAxes", "toggle_object_axes")])],
           "VIEWS_PIE": [("ui.pies", [("PieViews", "views_pie")]),
                         ("ui.operators.views_and_cams", [("ViewAxis", "view_axis"),
                                                          ("MakeCamActive", "make_cam_active"),
                                                          ("SmartViewCam", "smart_view_cam"),
                                                          ("NextCam", "next_cam"),
                                                          ("ToggleCamPerspOrtho", "toggle_cam_persportho"),
                                                          ("ToggleViewPerspOrtho", "toggle_view_persportho")])],
           "ALIGN_PIE": [("ui.pies", [("PieAlign", "align_pie"),
                                      ("PieUVAlign", "uv_align_pie")]),
                         ("ui.operators.align", [("AlignEditMesh", "align_editmesh"),
                                                 ("CenterEditMesh", "center_editmesh"),
                                                 ("AlignObjectToEdge", "align_object_to_edge"),
                                                 ("AlignObjectToVert", "align_object_to_vert"),
                                                 ("Straighten", "straighten")]),
                         ("ui.operators.uv_align", [("AlignUV", "align_uv")])],
           "CURSOR_PIE": [("ui.pies", [("PieCursor", "cursor_pie")]),
                          ("ui.operators.cursor", [("CursorToOrigin", "cursor_to_origin"),
                                                   ("CursorToSelected", "cursor_to_selected")]),
                          ("ui.operators.origin", [("OriginToActive", "origin_to_active")])],

           "TRANSFORM_PIE": [("ui.pies", [("PieTransform", "transform_pie")]),
                             ("ui.operators.set_transform_preset", [("SetTransformPreset", "set_transform_preset")])],

           "COLLECTIONS_PIE": [("ui.pies", [("PieCollections", "collections_pie")]),
                               ("ui.operators.collections", [("CreateCollection", "create_collection"),
                                                             ("AddToCollection", "add_to_collection"),
                                                             ("RemoveFromCollection", "remove_from_collection"),
                                                             ("MoveToCollection", "move_to_collection"),
                                                             ("SortGroupProGroups", "sort_grouppro_groups"),
                                                             ("Purge", "purge_collections"),
                                                             ("Select", "select_collection")])],

           "WORKSPACE_PIE": [("ui.pies", [("PieWorkspace", "workspace_pie")]),
                             ("ui.operators.switch_workspace", [("SwitchWorkspace", "switch_workspace")])],

           "OBJECT_CONTEXT_MENU": [("ui.menus", [("MenuMACHIN3toolsObjectContextMenu", "machin3tools_object_context_menu")])],
           }


keys = {"SMART_VERT": [{"label": "Merge Last", "keymap": "Mesh", "idname": "machin3.smart_vert", "type": "ONE", "value": "PRESS", "properties": [("mode", "MERGE"), ("mergetype", "LAST"), ("slideoverride", False)]},
                       {"label": "Merge Center", "keymap": "Mesh", "idname": "machin3.smart_vert", "type": "ONE", "value": "PRESS", "shift": True, "properties": [("mode", "MERGE"), ("mergetype", "CENTER"), ("slideoverride", False)]},
                       {"label": "Merge Paths", "keymap": "Mesh", "idname": "machin3.smart_vert", "type": "ONE", "value": "PRESS", "alt": True, "properties": [("mode", "MERGE"), ("mergetype", "PATHS"), ("slideoverride", False)]},
                       {"label": "Connect Paths", "keymap": "Mesh", "idname": "machin3.smart_vert", "type": "ONE", "value": "PRESS", "alt": True, "ctrl": True, "properties": [("mode", "CONNECT"), ("slideoverride", False)]},
                       {"label": "Slide Extend", "keymap": "Mesh", "idname": "machin3.smart_vert", "type": "ONE", "value": "PRESS", "shift": True, "alt": True, "properties": [("slideoverride", True)]}],
        "SMART_EDGE": [{"label": "Smart Edge", "keymap": "Mesh", "idname": "machin3.smart_edge", "type": "TWO", "value": "PRESS", "properties": [("sharp", False)]},
                       {"label": "Toggle Sharp", "keymap": "Mesh", "idname": "machin3.smart_edge", "type": "TWO", "shift": True, "value": "PRESS", "properties": [("sharp", True)]}],
        "SMART_FACE": [{"keymap": "Mesh", "idname": "machin3.smart_face", "type": "FOUR", "value": "PRESS"}],
        "CLEAN_UP": [{"keymap": "Mesh", "idname": "machin3.clean_up", "type": "THREE", "value": "PRESS"}],
        "CLIPPING_TOGGLE": [{"keymap": "3D View Generic", "space_type": "VIEW_3D", "idname": "machin3.clipping_toggle", "type": "BUTTON5MOUSE", "value": "PRESS"}],
        "FOCUS": [{"label": "View Selected", "keymap": "3D View Generic", "space_type": "VIEW_3D", "idname": "machin3.focus", "type": "F", "value": "PRESS", "properties": [("method", "VIEW_SELECTED")]},
                  {"label": "Local View", "keymap": "Object Mode", "idname": "machin3.focus", "type": "F", "value": "PRESS", "ctrl": True, "properties": [("method", "LOCAL_VIEW")]}],
        "MIRROR": [{"label": "X Axis", "keymap": "Object Mode", "idname": "machin3.mirror", "type": "X", "value": "PRESS", "alt": True, "shift": True, "properties": [("use_x", True), ("use_y", False), ("use_z", False)]},
                   {"label": "Y Axis", "keymap": "Object Mode", "idname": "machin3.mirror", "type": "Y", "value": "PRESS", "alt": True, "shift": True, "properties": [("use_x", False), ("use_y", True), ("use_z", False)]},
                   {"label": "Z Axis", "keymap": "Object Mode", "idname": "machin3.mirror", "type": "Z", "value": "PRESS", "alt": True, "shift": True, "properties": [("use_x", False), ("use_y", False), ("use_z", True)]}],
        "ALIGN": [{"keymap": "Object Mode", "idname": "machin3.align", "type": "A", "value": "PRESS", "alt": True}],

        "FILEBROWSER": [{"label": "Open Filebrowser", "keymap": "File Browser", "space_type": "FILE_BROWSER", "idname": "machin3.filebrowser_open", "type": "O", "value": "PRESS"},
                        {"label": "Toggle Sortign", "keymap": "File Browser", "space_type": "FILE_BROWSER", "idname": "machin3.filebrowser_toggle", "type": "ONE", "value": "PRESS", "properties": [("type", "SORT")]},
                        {"label": "Toggle Display", "keymap": "File Browser", "space_type": "FILE_BROWSER", "idname": "machin3.filebrowser_toggle", "type": "TWO", "value": "PRESS", "properties": [("type", "DISPLAY_TYPE")]},
                        {"label": "Toggle Hidden", "keymap": "File Browser", "space_type": "FILE_BROWSER", "idname": "machin3.filebrowser_toggle", "type": "THREE", "value": "PRESS", "properties": [("type", "HIDDEN")]}],

        "MODES_PIE": [{"label": "3D View", "keymap": "Object Non-modal", "idname": "wm.call_menu_pie", "type": "TAB", "value": "PRESS", "properties": [("name", "MACHIN3_MT_modes_pie")]},
                      {"label": "Image Editor", "keymap": "Image", "space_type": "IMAGE_EDITOR", "idname": "wm.call_menu_pie", "type": "TAB", "value": "PRESS", "properties": [("name", "MACHIN3_MT_modes_pie")]}],
        "SAVE_PIE": [{"keymap": "Window", "idname": "wm.call_menu_pie", "type": "S", "value": "PRESS", "ctrl": True, "properties": [("name", "MACHIN3_MT_save_pie")]}],
        "SHADING_PIE": [{"keymap": "3D View Generic", "space_type": "VIEW_3D", "idname": "wm.call_menu_pie", "type": "PAGE_UP", "value": "PRESS", "properties": [("name", "MACHIN3_MT_shading_pie")]}],
        "VIEWS_PIE": [{"keymap": "3D View Generic", "space_type": "VIEW_3D", "idname": "wm.call_menu_pie", "type": "PAGE_DOWN", "value": "PRESS", "properties": [("name", "MACHIN3_MT_views_pie")]}],
        "ALIGN_PIE": [{"label": "Edit Mode", "keymap": "Mesh", "idname": "wm.call_menu_pie", "type": "A", "value": "PRESS", "alt": True, "properties": [("name", "MACHIN3_MT_align_pie")]},
                      {"label": "UV Editor", "keymap": "UV Editor", "idname": "wm.call_menu_pie", "type": "A", "value": "PRESS", "alt": True, "properties": [("name", "MACHIN3_MT_uv_align_pie")]}],
        "CURSOR_PIE": [{"keymap": "3D View Generic", "space_type": "VIEW_3D", "idname": "wm.call_menu_pie", "type": "S", "value": "PRESS", "shift": True, "properties": [("name", "MACHIN3_MT_cursor_pie")]}],
        "TRANSFORM_PIE": [{"keymap": "3D View Generic", "space_type": "VIEW_3D", "idname": "wm.call_menu_pie", "type": "BUTTON4MOUSE", "value": "PRESS", "shift": True, "properties": [("name", "MACHIN3_MT_transform_pie")]}],
        "COLLECTIONS_PIE": [{"keymap": "3D View Generic", "space_type": "VIEW_3D", "idname": "wm.call_menu_pie", "type": "C", "value": "PRESS", "shift": True, "properties": [("name", "MACHIN3_MT_collections_pie")]}],
        "WORKSPACE_PIE": [{"keymap": "Window", "idname": "wm.call_menu_pie", "type": "PAUSE", "value": "PRESS", "properties": [("name", "MACHIN3_MT_workspace_pie")]}],
        }
