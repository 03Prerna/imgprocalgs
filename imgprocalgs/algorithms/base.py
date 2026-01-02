import abc
from imgprocalgs.algorithms.utilities import Image

class ImageProcessingAlgorithm(metaclass=abc.ABCMeta):
    def __init__(self, image_path):
        self.image_path = image_path
        self.image = Image(image_path)

    @abc.abstractmethod
    def process(self, *args, **kwargs):
        pass
