# import the necessary packages
from imutils.video import VideoStream, FileVideoStream, FPS
#imutils: https://github.com/jrosebr1/imutils/tree/master/imutils/video
import time
import os

class LoadVideo:
	# The class process a video file or the webcam to return a frame when request.

	def __init__(self, source: str="0", warmUp: float=1.0):
		""" 
		Initialization function of the LoadVideo class.
  
		Parameters: 
		source (str):		The path to the video to be load, or the number of the webcam.
		warmUp (float):		The number of seconds for warm up the webcam.
		"""
		if source=="-1":
			source="0"

		self.source = source
		self.fps = None
		
		if source.isdigit(): #loading form webcam stream
			self.realtime = True
			self.stream = VideoStream(src=int(source)).start()
			time.sleep(warmUp)	#warm up the camera
		
		else:				#loading form file stream
			self.realtime = False
			if os.path.exists(source):
				self.stream = FileVideoStream(source).start()
			else:
				print("Warning missing source file:", source)

	def read(self) -> "numpy.ndarray":
		""" Return a new frame of the stream. """
		if self.fps is None:
			# initialize the FPS counter
			self.fpsStart()
		else:
			# update the FPS counter
			self.fps.update()
		return self.stream.read()

	def fpsStart(self) -> None:
		""" Start the FramePerSecond calculator. """
		self.fps = FPS().start()

	def fps(self) -> float:
		""" Compute the fps rate of the reading processing time. """
		if self.fps is not None:
			self.fps.stop()
			return self.fps.fps()
		print("Warning: fps calculator not initialized.")
		return(0.0)

	def fpsOfSource(self) -> float:
		""" Return the original fps rate of the source video/webcam. """
		# To capture the fps rate of a video file the command should be: double fps = openedvideo.get(CV_CAP_PROP_FPS)
		# as stated here: https://answers.opencv.org/question/3294/get-video-fps-with-videocapture/
		#if self.realtime:
		#	print("todo: get fps of webcam")
		#else:
		#	return openedvideo.get(CV_CAP_PROP_FPS)
		print("todo: function not implemented yet.")


#from storeVideo import StoreVideo
#if __name__ == "__main__":
#	lv = LoadVideo()
#	sv = StoreVideo("pippo", show=True, fps=80)

#	# Loop to capture and store the frames
#	end = False
#	while not end:
#		end = sv.addFrame(lv.read())
#	print("\n\nEND\n\n")