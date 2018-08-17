# Created by: Guilherme Teres Nunes

import bge


def mouseOver(prop):
	scene = bge.logic.getCurrentScene()
	cam = scene.active_camera
	mPos = bge.logic.mouse.position

	obj = cam.getScreenRay(mPos[0], mPos[1], 10000, prop)
	return obj, mPos

def loadLevel():
	if "path" in bge.logic.globalDict:
		if bge.logic.globalDict["path"] != None:
			bge.logic.LibFree(bge.logic.globalDict["path"])
			bge.logic.globalDict["path"] = None

	bge.logic.globalDict["path"] = bge.logic.expandPath(
		"//Scenes//" + bge.logic.globalDict["level"] + ".blend")
	bge.logic.LibLoad(bge.logic.globalDict["path"], "Scene")