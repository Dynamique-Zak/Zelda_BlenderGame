from bge import logic, types
import aud
import os
import bpy
import textwrap

scene = logic.getCurrentScene()
objects = scene.objects

# declare the other object we will used
finishCursor = objects["msgBox_finishCursor"]
msgBox_nextCursor = objects["msgBox_nextCursor"]
textObject = objects["msgText"]
boxObject = objects["msgBox"]

# State
DEACTIVATE_STATE = 0
PRINT_TEXT_STATE = 1
ANIM_SHOW_TEXT_STATE = 3
WAIT_NEXT_TEXT_STATE = 4
FINISH_CURRENT_TEXT = 5
END_SHOW_TEXT = 6
WAIT_INPUT_SHOW_TEXT = 7

# load message box sounds
device = aud.device()
# load sound file (it can be a video file with audio)
dialogueNextSound = aud.Factory( bpy.path.abspath("//../audio/hud_song/dialogue_next.wav") )
dialogueDoneSound = aud.Factory( bpy.path.abspath("//../audio/hud_song/dialogue_done.wav") )

class MessageBoxMode:
	SHOW_TYPE = 0
	WAIT_INPUT_TYPE = 1

class MessageBox(types.KX_GameObject):
	def __init__(self, own):
		self.currentText = ""
		self.currentTextEndIndex = 0
		self.speedShow = 3
		self.nextText = ""
		self.currentTextLen = 0
		self.type = MessageBoxMode.SHOW_TYPE
		self.timeWait = 53.0 # is the time to wait in show mode
		self.stateTime = 0.0
		self.active = False
		self.etat = DEACTIVATE_STATE
		self.hide()

	def playStateTime(self, limit):
		if (self.stateTime + 0.1 < limit):
			self.stateTime += 0.1
			return False
		else:
			self.stateTime = limit
			return True

	def hide(self):
		boxObject.setVisible(False)
		textObject.setVisible(False)
		finishCursor.setVisible(False)

	def display(self):
		boxObject.setVisible(True)
		textObject.setVisible(True)

	def displayFinishCursor(self):
		finishCursor.setVisible(True)

	def displayNextCursor(self):
		msgBox_nextCursor.setVisible(True)

	def switchState(self, etat):
		# reset state time
		self.stateTime = 0.0
		self.etat = etat

	def setText(self, text):
		# get of this text
		size = len(text)
		textObject['Text'] = ''

		if (size > 110):
			self.currentText = text[0:107] + "..."
			self.nextText = text[107:size]
			self.currentTextLen = 107
		else:
			# set current text of all
			self.currentText = text
			self.currentTextLen = size
			self.nextText = ''

	def changeNextText(self):
		"""
		If have a next text return True else False
		"""
		if (self.nextText != ''):
			self.setText(self.nextText);
			return True
		else:
			return False

	def haveNextText(self):
		if (self.nextText != ''):
			return True
		else:
			return False

	def startText(self, text):
		self.setText(text)
		self.switchState(ANIM_SHOW_TEXT_STATE)

	def updateTextWithAnimation(self):
		"""
		Update the show text animation

		Return : True if can anim again, else false when is finish
		"""
		# update end index
		result = True
		if (self.currentTextEndIndex + self.speedShow < self.currentTextLen):
			self.currentTextEndIndex += self.speedShow
			current_text = self.currentText[0: int(self.currentTextEndIndex)]
		else:
			current_text = self.currentText
			# reset end index anim for the next text
			self.currentTextEndIndex = 0
			result = False
		textObject['Text'] = textwrap.fill(current_text, 40)
		return result

	def displayText(self, text, mode=MessageBoxMode.SHOW_TYPE):
		self.type = mode
		self.active = True
		self.display()
		self.startText(text)

	def finish(self):
		self.active = False
		self.hide()

	def waitNextTextState(self):
		# if click to the next input
		# elif show mode just wait for continue
		if (self.haveNextText()):
			if ( self.type == MessageBoxMode.SHOW_TYPE and self.playStateTime(3.0)):
				if ( self.changeNextText()):
					self.switchState(ANIM_SHOW_TEXT_STATE)
			elif (self.type == MessageBoxMode.WAIT_INPUT_TYPE):
					self.start_waitInputShowTextState()
		else:
			# so is the last text ans play done audio
			handle = device.play(dialogueDoneSound)
			# hide cursor
			self.displayFinishCursor()
			# switch to finish current text
			self.switchState(FINISH_CURRENT_TEXT)

	def animNextTextState(self):
		if ( not self.updateTextWithAnimation() ):
			self.switchState(WAIT_NEXT_TEXT_STATE)

	def start_waitInputShowTextState(self):
		self.displayNextCursor()
		self.switchState(WAIT_INPUT_SHOW_TEXT)

	def end_waitInputShowTextState(self):
		handle = device.play(dialogueNextSound)
		msgBox_nextCursor.setVisible(False)

	def waitInputShowTextState(self):
		# Gamepad
		gamepad = logic.globalDict['Player']['Gamepad']
		# wait to input in the next key
		if ( gamepad.isActionPressed() ):
			self.end_waitInputShowTextState()
			self.changeNextText()
			self.switchState(ANIM_SHOW_TEXT_STATE)

	def finishCurrentTextState(self):
		# Gamepad
		gamepad = logic.globalDict['Player']['Gamepad']
		# wait to input in the next key
		if ( gamepad.isActionPressed() ):
			# finish
			self.finish()

	def main(self):
		# Si la message est activé
		if (self.active):
			# text the next state
			if (self.etat == WAIT_NEXT_TEXT_STATE):
				self.waitNextTextState()
			# anim the show text
			elif (self.etat == ANIM_SHOW_TEXT_STATE):
				self.animNextTextState()
			# wait input for display the next state
			elif (self.etat == WAIT_INPUT_SHOW_TEXT):
				self.waitInputShowTextState()
			# wait input for confirm the end text
			elif (self.etat == FINISH_CURRENT_TEXT):
				self.finishCurrentTextState()
