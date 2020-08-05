# import the necessary packages
from abc import ABC # ABC = Abstract Method Class
import cv2

################################################################################################################
############################     Model Super Class        ######################################################
################################################################################################################
class Model(ABC):
	#variables
	modelPath:  str=None		#path to the model
	modelPath2: str=None		#path to the second part of the model
	layer: str=None				#the name of the layer where to end the DNN
	net: "cv2.dnn.net"=None		#the opencv network model

	def __init__():
		pass

	def setNetwork(self, net: "cv2.dnn.net") -> None:
		""" Set the network given. """
		self.net = net

	def setLayer(self, layer: str=None) -> None:
		""" Set the output layer name of the network (if None the last one is chosen). """
		self.layer = layer
		
	def blob(self, image) -> "blob":
		""" Create the blob form the images given. """
		return cv2.dnn.blobFromImages(images=[image], scalefactor=1, size=(224, 224), mean=(0.485, 0.456, 0.406))

	def setInput(self, blob) -> None:
		""" Set the input blob for the DNN. """
		self.net.setInput(blob)

	def forward(self) -> list:
		""" Process the given input through the DNN and return a list of float that is the feature vector (encodings) of the input blob. """
		return self.net.forward(self.layer) 
	
	def feed(self, blob) -> list:
		""" Do in one function the setInput and forward pass. """
		self.setInput(blob)
		return self.forward()

	def getLayerNames(self, show: bool=False) -> list:
		""" Return and eventually show the list of layers of the model. """
		layerNames = self.net.getLayerNames()
		if show:
			for (i, l) in enumerate(layerNames):
				print(i, "->", l)
			print("\n")
		return(layerNames)

################################################################################################################
############################     Image Classification     ######################################################
################################################################################################################

#>>>>>>>>>>>>>>>>>>>>>>>>>>>     ResNet50 Model           <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
class ResNet50(Model):
	def __init__(self, 
			  modelPath: str="../models/resnet50-caffe2/resnet50-caffe2.onnx", 
			  layer: str="OC2_DUMMY_0"):

		self.modelPath = modelPath
		self.layer = layer
		self.net = cv2.dnn.readNetFromONNX(self.modelPath)


#>>>>>>>>>>>>>>>>>>>>>>>>>>>     GoogleNet Model          <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
class GoogleNet(Model):
	def __init__(self, 
			  modelPath: str="../models/googleNet/bvlc_googlenet.prototxt",
			  modelPath2: str="../models/googleNet/bvlc_googlenet.caffemodel",
			  layer: str="pool5/7x7_s1"):

		self.modelPath = modelPath
		self.modelPath2 = modelPath2
		self.layer = layer
		self.net = cv2.dnn.readNetFromCaffe(self.modelPath, self.modelPath2)


