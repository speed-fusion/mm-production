from io import BytesIO
from pathlib import Path
from PIL import Image
from concurrent.futures import ThreadPoolExecutor,as_completed

class ImageGenerator:
    def __init__(self) -> None:
        self.sizes = [
            {
                "name":"thumb",
                "h":270,
                "w":180
            },
            {
                "name":"large",
                "h":900,
                "w":600
            },
        ]
        
        self.files_dir = Path("/files")
    
    def convert_image(self, image, size=None):
        if image.format == 'PNG' and image.mode == 'RGBA':
            background = self._Image.new('RGBA', image.size, (255, 255, 255))
            background.paste(image, image)
            image = background.convert('RGB')
        elif image.mode == 'P':
            image = image.convert("RGBA")
            background = self._Image.new('RGBA', image.size, (255, 255, 255))
            background.paste(image, image)
            image = background.convert('RGB')
        elif image.mode != 'RGB':
            image = image.convert('RGB')

        if size:
            image = image.copy()
            image.thumbnail((size["h"],size["w"]), Image.Resampling.LANCZOS)

        buf = BytesIO()
        
        image.save(buf, 'JPEG')
        
        return image, buf

    def read_image(self,imagePath):
        img = None
        
        with open(imagePath,"rb") as f:
            img = Image.open(BytesIO(f.read()))
        return img
    
    def generateImages(self,websiteId,listingId,imageId,imagePath,imageUrl,position,processedImages):
        processedImages["id"] = imageId
        processedImages["url"] = imageUrl
        processedImages["position"] = position
        processedImages["status"] = False
        
        try:
            rawImage = self.read_image(imagePath)
            
            orgImagePath = f'S{websiteId}/ad{listingId}/org_{imageId}.jpg'
            tmp = {}
            tmp["path"] = orgImagePath
            tmp["type"] = "org"
            tmp["size"] = None
            
            processedImages["org"] = tmp
            
            for size in self.sizes:
                tmp = {}
                imagePathTmp = f'S{websiteId}/ad{listingId}/{size["name"]}_{imageId}.jpg'
                tmp['path'] = imagePathTmp
                tmp['type'] = size["name"]
                tmp["size"] = size
                processedImages[size["name"]] = tmp
                
            
            
            org_image_path = self.files_dir.joinpath(orgImagePath)
            
            if org_image_path.exists() == False:
                _,orgImage = self.convert_image(rawImage)
                # upload image in server through ftp
                org_image_path.write_bytes(orgImage)
            
            for size in self.sizes:
                imagePathTmp = f'S{websiteId}/ad{listingId}/{size["name"]}_{imageId}.jpg'
                img_path_tmp = self.files_dir.joinpath(imagePathTmp)
                if img_path_tmp.exists() == False:
                    _,buff = self.convert_image(rawImage,size)
                    img_path_tmp.write_bytes(buff)
            
            processedImages["status"] = True
            
            return processedImages
        
        except Exception as e:
            print(f'error : {str(e)}')
        
        return processedImages
        
    def processListing(self,images,websiteId,listingId):
        processedImages = []
        
        threads = []

        website_dir = self.files_dir.joinpath(f'S{websiteId}')
        
        if website_dir.exists() == False:
            website_dir.mkdir()

        listing_img_dir = website_dir.joinpath(f'ad{listingId}')
        
        if listing_img_dir.exists() == False:
            listing_img_dir.mkdir()
        
        with ThreadPoolExecutor(max_workers=15) as executor:
            for item in images:
                
                imageId = item["_id"]
                
                imagePath = item["path"]
                
                imageUrl = item["url"]
                
                position = None
                
            
                position = item["position"]
                
                threads.append(executor.submit(self.generateImages,websiteId,listingId,imageId,imagePath,imageUrl,position,item))
        
            for task in as_completed(threads):
                data = task.result()
                
                processedImages.append(data)
        
        return processedImages



# if __name__ == "__main__":
#     ig = imageGenerator()
    
#     cwd = Path.cwd()
    
#     imageDir = cwd.joinpath("images")
    
    
#     images = [
#         {
#             "id":"hjshja",
#             "path":f'{imageDir.joinpath("test.png")}',
#             "url":"xyz"
#         }
#     ]
#     websiteId = "s56"
#     listingId = "a12345"
    
    
#     t = ig.processListing(images,websiteId,listingId)
#     print(t)
    # cwd = Path.cwd()
    
    # imagePath = cwd.joinpath("test.png")
    
    # img = ig.read_image(imagePath)
    
    # for size in ig.sizes:
    #     print(f'size :{size}')
    #     im,buff = ig.convert_image(img,size)
    #     with open(f'{size["name"]}.jpg',"wb") as f:
    #         f.write(buff.getvalue())
    
    