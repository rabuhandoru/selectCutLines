import bpy
import bmesh

bl_info = {
	"name": "select cut lines",
	"author": "rabuhandoru",
	"version": (1, 0),
	"blender": (3, 4, 0),
	"location": "View3D > Edit > Select",
	"description": "切れ目を選択するアドオン",
	"warning": "",
	"wiki_url": "",
	"tracker_url": "",
	"category": "Object",
}

translationDict = {
	"en_US": {
		("*", "Select Cut Lines"):"Select Cut Lines",
	},
	"ja_JP": {
		("*", "Select Cut Lines"):"切れ目選択",
	}
}

class SELECT_OT_selectCutLines(bpy.types.Operator):

	bl_idname = "object.select_cut_lines"
	bl_label = bpy.app.translations.pgettext("Select Cut Lines")
	bl_description = "切れ目を選択します"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):

		bpy.ops.object.mode_set(mode='OBJECT')
		bpy.ops.object.mode_set(mode='EDIT')
		bpy.ops.mesh.select_all(action='DESELECT')

		obj=bpy.context.edit_object
		bMesh = bmesh.from_edit_mesh(obj.data)

		selectMode = bpy.context.tool_settings.mesh_select_mode[:]

		for e in bMesh.edges:
			if len(e.link_faces) == 1:
				for v in e.verts:
					if len(v.link_faces) < 4:
						if selectMode[2] == True:
							for f in v.link_faces:
								f.select = True
						else:
							e.select = True

		bMesh.select_flush_mode()

		return {'FINISHED'}

def addMenu(self, context):
	self.layout.separator()
	self.layout.operator(SELECT_OT_selectCutLines.bl_idname,text=bpy.app.translations.pgettext("Select Cut Lines"))

classes = [
	SELECT_OT_selectCutLines,
]

def register():
	bpy.app.translations.register(__name__, translationDict)
	for c in classes:
		bpy.utils.register_class(c)
	bpy.types.VIEW3D_MT_select_edit_mesh.append(addMenu)


def unregister():
	bpy.app.translations.unregister(__name__)
	bpy.types.VIEW3D_MT_select_edit_mesh.remove(addMenu)
	for c in classes:
		bpy.utils.unregister_class(c)


if __name__ == "__main__":
	register()
