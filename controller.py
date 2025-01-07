from core.control_logic import ControlLogic

class Controller(ControlLogic):
	def loop(self):
		robot = self.triangle
		# =========================================
		# TODO: Implement your control logic here
		# API: Triangle/Corner from core.sim.py
		# Corners: A, B, C
		#
		# robot.A/B/C (Corner object), robot.corners
		# robot.A/B/C.sensor_reading (color sensor)
		# robot.A/B/C.has_changed (color sensor)
		# robot.control_corner (default A)
		#
		# robot.move(dx, dy)
		# robot.move_in_normal_direction(step) (based on control points)
		# =========================================

		print("Control corner", robot.control_corner.label)
		robot.move_in_normal_direction(5)
