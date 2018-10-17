import maya.cmds as cmds
import maya.api.OpenMaya as om


KILL_CALLBACK_IDS = list()

_CALLBACKS = (om.MSceneMessage.kAfterImport,
              om.MSceneMessage.kAfterOpen,
              om.MSceneMessage.kAfterNew,
              )

def createCallbacks():
    global KILL_CALLBACK_IDS
    for callback in _CALLBACKS:
        callbackID = om.MSceneMessage.addCallback(callback, killTurtle)
        KILL_CALLBACK_IDS.append(callbackID)

def removeCallbacks():
    global KILL_CALLBACK_IDS
    for callbackID in KILL_CALLBACK_IDS:
        om.MMessage.removeCallback(callbackID)
    KILL_CALLBACK_IDS = list()

def killTurtle(*args, **kwargs):
    turtlesNodesTypes = cmds.pluginInfo("Turtle", query=True, dependNode=True)
    turtleNodes = cmds.ls(type=turtlesNodesTypes)

    if turtleNodes:
        deleteNodes(turtleNodes)
        print("killTurtle : Removed TurtleNodes: \n {0}".format(turtleNodes))

    unloadTurtlePlugin()

def deleteNodes(nodes):
    cmds.lockNode(nodes, lock=False)
    cmds.delete(nodes)

def unloadTurtlePlugin():
    if cmds.pluginInfo("Turtle", query=True, loaded=True):
        cmds.unloadPlugin("Turtle")

#------------------------------------------------------------
def initializePlugin(mobject):
    createCallbacks()

def uninitializePlugin(mobject):
    removeCallbacks()


