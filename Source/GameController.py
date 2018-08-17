# Created by Guilherme Teres Nunes

import bge
from mathutils import Vector
from collections import OrderedDict

try:
	from Scripts.GameUtils import *
except:
	from Source.Scripts.GameUtils import *

class GameController(bge.types.KX_PythonComponent):
	args = OrderedDict([
		("Ball Name"			,""),
		("Ball Deacceleration"	, 0.01),
		("End Point Name"		, "")
	])

	def start(self, args):
		self.ball = self.object.scene.objects[args["Ball Name"]]
		self.endPoint = self.object.scene.objects[args["End Point Name"]]

		self.shootDirection	= None
		self.shootSpeed 	= 1.0

		self.__ballDeacceleration = args["Ball Deacceleration"]

		# To store the Game state:
		#	0 = Waiting the player
		#	1 = Simulating everything
		#	2 = Win/Lose Screen
		self.__state = 0

		self.__aux = False
		self.__auxPos = None

		bge.render.showMouse(True)

		self.__changeColors(True)

		# Loading the Level
		if not "level" in bge.logic.globalDict:
			bge.logic.globalDict["level"] = "level0"

		loadLevel()

		self.__start = [obj for obj in self.object.scene.objects if "startPoint" in obj][0]
		self.__end   = [obj for obj in self.object.scene.objects if "endPoint" in obj][0]

		self.ball.worldPosition = self.__start.worldPosition.copy()
		self.endPoint.worldPosition = self.__end.worldPosition.copy()

	def __changeColors(self, active):
		color = [0.8, 0.0, 0.0, 1.0]
		if active:
			color = [0.0, 0.8, 0.0, 1.0]

		for obj in self.object.scene.objects:
			if "color" in obj:
				obj.color = color

	def __runState0(self):
		mouse = bge.logic.mouse.inputs
		keyTAP = bge.logic.KX_INPUT_JUST_ACTIVATED

		if not self.__aux:
			if mouse[bge.events.LEFTMOUSE].values[-1]:
				obj, mPos = mouseOver("Player")
				if obj == self.ball:
					# Clicked on the player

					self.__aux = True
					self.__auxPos = mPos
		else:
			if not mouse[bge.events.LEFTMOUSE].values[-1]:
				# Released the mouse button (shoot now!)

				_, mPos = mouseOver("")

				self.shootDirection = Vector(mPos) - Vector(self.__auxPos)
				self.shootSpeed = self.shootDirection.length

				if self.shootSpeed == 0.0:
					return
				elif self.shootSpeed >= 1.5:
					self.shootSpeed = 1.5

				self.shootDirection = Vector(
					[self.shootDirection.x, self.shootDirection.y, 0])

				self.shootDirection.y *= -1
				aspect = bge.render.getWindowWidth() / bge.render.getWindowHeight()

				self.shootDirection.x *= aspect

				# Normalizing the vector:
				self.shootDirection /= self.shootDirection.length

				self.__aux = False
				self.__state = 1
				self.__changeColors(False)


	def __runState1(self):
		if self.shootSpeed > 0:
			self.shootSpeed -= self.__ballDeacceleration

			target = self.ball.worldPosition + self.shootDirection
			obHit, obPos, obNormal = self.ball.rayCast(target, self.ball, 1.0,
													   "wall", 1, 1, 0)

			if obHit != None:
				self.shootDirection = self.shootDirection.reflect(obNormal)
				bge.logic.sendMessage("Shake_Small")

				lst = self.object.scene.addObject("Explosion1", self.object, 200)
				scale = self.shootSpeed*2.0
				lst.worldPosition = obPos
				lst.worldScale = [scale, scale, scale]
				lst.alignAxisToVect(obNormal, 2, 1)

			self.ball.applyMovement(self.shootDirection*self.shootSpeed, False)
		else:
			self.__state = 0
			self.__changeColors(True)



	def update(self):
		[self.__runState0, self.__runState1][self.__state]()

		if self.ball.getDistanceTo(self.endPoint) < 1.5:
			self.object.scene.suspend()
			bge.logic.addScene("Menu_GameOver")

