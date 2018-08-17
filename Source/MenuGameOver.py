# Created by Guilherme Teres Nunes

import bge
from collections import OrderedDict

class MenuGameOver(bge.types.KX_PythonComponent):
	args = OrderedDict([

	])
	def start(self, args):
		self.text = self.object.scene.objects["GameOverText"]

	def update(self):
		if self.object["timer"] > 2.0:
			bge.logic.getSceneList()["Gameplay"].restart()
			self.object.scene.end()
			bge.logic.globalDict["level"] = "level"+str(int(bge.logic.globalDict["level"][5:])+1)

			levels = bge.logic.getBlendFileList(bge.logic.expandPath("//Scenes//"))
			if not bge.logic.globalDict["level"]+".blend" in levels:
				print(levels)
				for obj in bge.logic.getSceneList():
					obj.end()
		elif self.object["timer"] > 0.5:
			self.text.visible = True