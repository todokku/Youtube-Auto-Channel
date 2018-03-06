from PIL import Image as image
import random
import os
import hashlib


#!changed thumbnail to resize so it should always change images to right size now

#ALSO IT WONT WORK FOR IMAGES THAT HAVE SLIGHTLY DIFFERENT COLORS IN ONE PLACE
#SO COMPARING COMPRESSED AND UNCOMPRESSED IMAGES MIGHT HECK IT BUT WHO KNOWS

def hash(img_path):
    img = image.open(img_path)
    img = img.convert('LA') #converts to grayscale
    img.resize((50,50))
    file_name = str(random.random()) + '.png'
    with open(file_name, 'wb') as f: #pretty ghetto, should be using virtual files or whatever
        img.save(file_name)
    with open(file_name, 'rb') as f:
        data = f.read()
    os.remove(file_name)
    return hashlib.md5(data).hexdigest()

if __name__ == "__main__":
    h = hash('images_OLD\\aclvcpnxrzpw.jpg')
    
