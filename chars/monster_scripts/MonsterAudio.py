import aud

# load sound device
device = aud.device()

class MonsterAudio:

	def __init__(self):
		self.lastStepFrame = 0

	def playStepSound(self, current_frame, frames, audio):
		for frame in frames:
			r = range(frame-1, frame+1)
			if ( (current_frame >= frame and current_frame <= frame+1) and self.lastStepFrame != frame):
				self.lastStepFrame = frame
				device.play(audio)
