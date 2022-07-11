import base64
from fastai.vision import *
from pathlib import Path
from imageDownloader import ImageDownloader
import os

class Predictor:
    def __init__(self):
        print("image predictor init")

        self.model = load_learner('model')
        
        self.cwd = Path.cwd()
        
        self.downloader = ImageDownloader()
        
    def predict(self,urls,websiteId,sourceId):
        
        predicted = []
        
        downloadedImagesTemp = self.downloader.download_multiple_images(urls,websiteId,sourceId)
        
        downloadedImages = sorted(downloadedImagesTemp, key = lambda i: i['position'])
        
        for image in downloadedImages:
            
            if len(predicted) >= 15:
                break
            
            if image["data"]["image_download_status"] == 2:
                predicted.append(image)
                continue
            
            img = open_image(image["data"]["path"])
            
            pred_class,pred_idx,outputs = self.model.predict(img)
            
            image["data"]["pred_class"] = str(pred_class)
            
            if not str(pred_class) in ["cars"]:
                image["data"]["is_car_image"] = False
            else:
                image["data"]["is_car_image"] = True
            
            predicted.append(image)
            
        return predicted
    
    def encode_image_base64(self,imagePath):
        
        base64str = base64.b64encode(imagePath.read_bytes()).decode("utf-8")
        
        return base64str