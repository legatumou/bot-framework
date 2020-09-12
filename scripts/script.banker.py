from __future__ import absolute_import
import logging
logging.basicConfig()
from pynput.mouse import Listener
from pynput.mouse import Button, Controller
import time

class Script:
    name = "Banker"
    itemPos = None
    bankPos = None
    status = "stopped"

    def __init__(self, outputEngine):
        self.output = outputEngine
        self.output.log("Banker script initialized")

    def process(self, statusLabel):
        self.statusLabel = statusLabel
        statusLabel.set("Banker process started.")
        self.requestItemPos()

    def halt(self):
        self.status = "stopped"

    def setContainer(container):
        self.container = container

    def startBanking(self):
        self.statusLabel.set("Banking, bank deposit interval 20 sec.")
        time.sleep(2)
        self.status = "running"
        while 1:
            self.statusLabel.set("Waiting")
            time.sleep(20)
            self.statusLabel.set("Banking")
            self.dragMouse(self.itemPos, self.bankPos)
            if self.status == "stopped":
                break


    def dragMouse(self, fromPos, toPos):
        mouse = Controller()
        originalPosition = mouse.position
        mouse.position = (fromPos[0], fromPos[1])
        time.sleep(0.5)
        mouse.press(Button.left)
        time.sleep(0.25)
        mouse.position = (toPos[0], toPos[1])
        time.sleep(0.5)
        mouse.release(Button.left)

    def requestBankPos(self):
        self.statusLabel.set("Left click to bank to record position.")
        self.listeningType = "bank"
        self.mouseListener = Listener(on_click=self.onClick)
        self.mouseListener.start()
        self.mouseListener.wait()

    def requestItemPos(self):
        self.statusLabel.set("Left click to item to record position.")
        self.listeningType = "item"
        self.mouseListener = Listener(on_click=self.onClick)
        self.mouseListener.start()
        self.mouseListener.wait()

    def onClick(self, x, y, button, pressed):
        if button == Button.left:
            if pressed:
                if self.listeningType is not None:
                    self.statusLabel.set("Left click pressed. Type: " + self.listeningType)
                    if self.listeningType == "item":
                        self.itemPos = [x, y]
                        self.mouseListener.stop()
                        self.requestBankPos()
                    else:
                        self.bankPos = [x, y]
                        self.mouseListener.stop()
                        self.startBanking()
