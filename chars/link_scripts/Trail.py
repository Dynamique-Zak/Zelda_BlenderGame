__author__ = 'SolarLune'

from bge import logic, types

class Trail():

	def __init__(self, stretch=True, spacing=3, reverse=False, vertex_axis="y",
				 update_on_moving_only=False, trail_target_obj=None, trail_obj=None):
		"""
		Creates a Trail object. Trail objects influence the vertices of their mesh to react to a trail owner object's
		movements. Think of a light trail, or a cape. When the owner moves or jumps or whatever, the trail reacts
		accordingly.
		:param stretch: Bool - If the vertices of the trail should stretch and stay in their position until movement.
		Think of the difference between a trail from a light cycle from Tron, and a cape. The trail stretches (it starts
		with a "nub", and then gets longer as the cycle drives along). The cape, on the other hand, doesn't
		stretch (it's always the same length).
		:param spacing: Int - The number of frames between the movement and the vertex update (or the vertex update and
		the following vertex update). Higher spacing = more delayed reaction on the trail vertices, which means a more
		"rough" trail, and a longer trail when stretch is on. Lower spacing = less of a pronounced reaction on the
		trail vertices, and a smoother overall trail. Also, a shorter trail when stretch is on.
		:param reverse: Bool - If the trail should reverse it's orientation based on the movement of the trail owner.
		E.G. If reverse is on, and a sword swings left, its trail swings left too.
		:param vertex_axis: Str - The axis that the vertices of the trail move on, going away from the origin of the
		trail object's mesh. Should be "x", "y", or "z".
		:param update_on_moving_only: Bool - If the trail should update only when the object's moving.
		:param trail_target_obj: KX_GameObject reference - The object that influences the trail. The trail object will
		snap to the trail target object's position and orientation. If left to None, this will default to the trail
		object's parent. Although, to get the best results, the trail shouldn't be parented to its owner. See the
		example blend file.
		:param trail_obj: The object to manipulate to achieve a trail. If left to None, will default to the "calling"
		object.
		:return: Trail
		"""

		if not trail_obj:
			o = logic.getCurrentController().owner
		else:
			o = trail_obj

		assert isinstance(o, types.KX_GameObject)

		self.obj = o

		sce = self.obj.scene

		#if trail_mesh is None:

		mesh = self.obj.meshes[0]

		#else:

		#   mesh = trail_mesh

		self.trail_axis = vertex_axis

		self.trail_verts = []

		for mat in range(mesh.numMaterials):

			for v in range(mesh.getVertexArrayLength(mat)):
				vert = mesh.getVertex(mat, v)

				self.trail_verts.append(vert)  # Get all verts

		self.vert_offsets = {}

		for vert in self.trail_verts:
			self.vert_offsets[vert] = vert.XYZ

		vert_pairs = {}

		for vert in self.trail_verts:

			if self.trail_axis.lower() == 'x':
				vert_y = round(vert.x,2)  # Round it off to ensure that verts that have very close X positions
				# (i.e. 0 and 0.01) get grouped together
			elif self.trail_axis.lower() == 'y':
				vert_y = round(vert.y, 2)
			else:
				vert_y = round(vert.z, 2)

			if vert_y not in vert_pairs:
				vert_pairs[vert_y] = []

			vert_pairs[vert_y].append(vert)  # Get the verts paired with their positions

		self.vert_pairs = []

		for vp in vert_pairs:
			self.vert_pairs.append([vp, vert_pairs[vp]])

		self.vert_pairs = sorted(self.vert_pairs, key=lambda x: x[0], reverse=True)

		self.target_positions = []

		self.trail_stretch = stretch  # Stretch the trail to 'fit' the movements

		self.trail_spacing = spacing  # Number of frames between each edge in the trail

		self.trail_reverse = reverse  # If the bending of the trail should be reversed

		self.update_on_moving_only = update_on_moving_only  # Update the trail only when moving

		self.trail_counter = spacing  # Number of frames between each 'keyframe'

		if not trail_target_obj:

			self.target = self.obj.parent

		else:

			self.target = trail_target_obj

		self.target_past_pos = self.target.worldPosition.copy()
		self.target_past_ori = self.target.worldOrientation.copy()

		for x in range(len(self.vert_pairs) * self.trail_spacing):
			self.target_positions.insert(0, [self.target.worldPosition.copy(), self.target.worldOrientation.copy()])

	def update(self):

		"""
		Update the trail.
		:return:
		"""

		if not self.obj.parent == self.target:
			self.obj.worldPosition = self.target.worldPosition
			self.obj.worldOrientation = self.target.worldOrientation

		target_info = [self.target.worldPosition.copy(), self.target.worldOrientation.copy()]

		insert = 0

		if not self.update_on_moving_only:
			insert = 1
		else:

			pos_diff = (self.target.worldPosition - self.target_past_pos).magnitude
			ori_diff = (self.target.worldOrientation - self.target_past_ori).median_scale
			threshold = 0.0001

			if pos_diff > threshold or ori_diff > threshold:
				insert = 1

		if insert:
			self.target_positions.insert(0, target_info)

		if len(self.target_positions) > len(self.vert_pairs) * self.trail_spacing:
			self.target_positions.pop()  # Remove oldest position value

		for vp in range(0, len(self.vert_pairs)):

			verts = self.vert_pairs[vp][1]

			if len(self.target_positions) > vp * self.trail_spacing:

				pos = self.target_positions[vp * self.trail_spacing][0]
				ori = self.target_positions[vp * self.trail_spacing][1]

				for vert in verts:

					if not self.trail_reverse:

						if self.trail_stretch:  # Factor in position of the target to 'stretch' (useful for trails,
						# where the end point stays still, hopefully, until the rest 'catches up'')
							diff = (pos - self.target.worldPosition) * ori
							vert.XYZ = (self.vert_offsets[vert] + diff) * self.target.worldOrientation
						else:  # Don't factor in movement of the trail
						# (useful for things that wouldn't stretch, like scarves)
							vert.XYZ = self.vert_offsets[vert] * self.target.worldOrientation
						vert.XYZ = vert.XYZ * ori.inverted()

					else:  # Reverse the trail's direction

						if self.trail_stretch:
							diff = (pos - self.target.worldPosition) * ori  # .inverted()
							vert.XYZ = (self.vert_offsets[vert] + diff) * self.target.worldOrientation.inverted()
						else:
							vert.XYZ = self.vert_offsets[vert] * self.target.worldOrientation.inverted()
						vert.XYZ = vert.XYZ * ori

		self.target_past_pos = self.target.worldPosition.copy()
		self.target_past_ori = self.target.worldOrientation.copy()
