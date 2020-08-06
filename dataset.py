# import the necessary packages
from abc import ABC # ABC = Abstract Method Class
from imutils import paths
import random
import os

################################################################################################################
############################     Dataset Abstract Class     ####################################################
################################################################################################################
#For abstract class look at: https://www.geeksforgeeks.org/abstract-classes-in-python/
class Dataset(ABC):

	def getLabelsAndPaths(self) -> "list of couple":
		""" Create a "list of couple" of lenght (nImgs) with key (1) the label of the person and value (2) the paths of its images. """
		pass

	def queryImgPath(self, queryNum: int=None) -> (int, str):
		""" 
			Return an image (label and path) to use as query. 
			queryNum: optionally chosen from the user: the image number to be used as query
		"""
		pass

############################     Negative People dataset functions     #########################################
class NegativePeopleDataset(Dataset):
	def __init__(self, nImgs: int=50, nTestDir: int=9) -> None:
		self.N_IMAGES = 518			#the number of images in the dataset (do not change)
		self.datasetPath = "../imagesIn/negativePeople_dataset/repeatedPeople"
		self.subFolderName = "set"
		self.setImgsGeneric = '/'.join([self.datasetPath, self.subFolderName])
		self.nTestDir = nTestDir	#how many folder of the dataset use to train (the next one is for test)
		self.nImgs = nImgs			#how many images to process
		if nImgs/nTestDir > self.N_IMAGES:
			self.nImgs = self.N_IMAGES*nTestDir
			print("Warning: not enoght images in the dataset (set to", self.nImgs, ")")

	### Private functions
	def __labelFromPath(self, pth):
		return( int(pth.split("/")[-1].split(".")[0]) )

	def __getLabelsAndPaths_fromFolder(self, folderPath, nImgs) -> "list of couple":
		labelsAndPaths = []
		imagesPaths = list(paths.list_images(folderPath))[:nImgs]
		for pth in imagesPaths:
			pth = pth.replace("\\", "/")
			label = self.__labelFromPath(pth)
			labelsAndPaths.append((label, pth))
		
		return(labelsAndPaths)

	### Public functions
	def getLabelsAndPaths(self) -> "list of couple":
		labelsAndPaths = []
		#take the same number of images from each of the 9 folders of the dataset (the 10th is used as testing folder)
		nImgsPartial = self.nImgs//self.nTestDir 

		for i in range(self.nTestDir):
			setImgs = ''.join([self.setImgsGeneric, str(i)])
			tmp = self.__getLabelsAndPaths_fromFolder(setImgs, nImgsPartial)
			[labelsAndPaths.append(el) for el in tmp]

		print("Added", nImgsPartial, "images, for each person/label:", [el[0] for el in labelsAndPaths[:nImgsPartial]], "\n")
		return(labelsAndPaths)

	def queryImgPath(self, queryNum: int=None) -> (int, str):
		setImgs = ''.join([self.setImgsGeneric, str(self.nTestDir), "/"])
		queryPath = ""
		if queryNum is None:
			#get a random image
			num = random.randint(0, self.nImgs//self.nTestDir)
			queryPath = list(paths.list_images(setImgs))[num]
			queryNum = self.__labelFromPath(queryPath)
		else:
			#get the image chosen from the user
			queryPath = "".join([setImgs, f'{queryNum:04}', ".jpg"])

		if not os.path.exists(queryPath):
			queryPath = None
		print("generated query:", (queryNum, queryPath))
		return((queryNum, queryPath))

############################     Street People dataset functions       #########################################
class StreetPeopleDataset(Dataset):
	def __init__(self, nImgs: int=20) -> None:
		self.datasetPath = "../imagesIn/streetPeople_dataset"
		self.nImgs = nImgs
		if nImgs>50:
			print("Warning: not enoght images in the dataset (set to 50)")
			self.nImgs = 50

	def getLabelsAndPaths(self) -> "list of couple":
		# get the path
		# str(os.path.sep) should be equal to '/', but for windows is not
		camera = '/'.join([self.datasetPath, "cam_a"])

		# select some images
		imagesPaths = list(paths.list_images(camera))[:self.nImgs]
		labelsAndPaths = list(enumerate(imagesPaths))
		return(labelsAndPaths)

	def queryImgPath(self, queryNum: int=None) -> (int, str):
		camera = '/'.join([self.datasetPath, "cam_b"])
		if queryNum is None:
			queryNum = random.randint(0, self.nImgs)
		queryPath = list(paths.list_images(camera))[queryNum]
		return((queryNum, queryPath))

############################     M100 dataset functions                #########################################
class M100Dataset(Dataset):
	def __init__(self, nImgs: int=20) -> None:
		self.N_IMAGES = 80 #the number of images in the dataset (do not change)
		self.datasetPath = "../imagesIn/100m_dataset"
		self.myQueryNum = None
		self.nImgs = nImgs
		if nImgs > self.N_IMAGES-1:
			print("Warning: not enoght images in the dataset (set to", self.N_IMAGES-1, ")")
			self.nImgs = self.N_IMAGES-1

	def getLabelsAndPaths(self) -> "list of couple":
		samples = random.sample(range(self.N_IMAGES), self.nImgs+1)
		self.myQueryNum = samples[0]

		imagesPaths = list(paths.list_images(self.datasetPath))
		labelsAndPaths = []
		for s in samples[1:]:
			#todo: check correctness with 19, 29, 39 and so on...
			print("sampled name:{}, \tid:{}, \tpath:{}".format(s, s//10, imagesPaths[s]))
			labelsAndPaths.append( (s//10, imagesPaths[s]) )

		print(labelsAndPaths)
		return(labelsAndPaths)

	def queryImgPath(self, queryNum: int=None) -> (int, str):
		if queryNum is None:
			queryNum = self.myQueryNum
		queryPath = list(paths.list_images(self.datasetPath))[queryNum]
		print("\nQUERY name:{}, id:{}, path:{}".format(queryNum, queryNum//10, queryPath))
		return((queryNum//10, queryPath))