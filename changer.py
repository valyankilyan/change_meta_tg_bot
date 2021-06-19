from loggingconfig import getLogger
log = getLogger(__name__)

import os
from PIL import Image
import piexif 
from config import src_image_path

src_photo = Image.open(src_image_path)

def properCords(cord):
    ans = len(str(cord).split('.')[1])
    m = 10 ** ans
    return int(cord * m), m

def getSrcExif(image):
    # берем размеры
    w, h = image.size
    
    # грузим готовый exif
    src_exif = piexif.load(src_photo.info['exif'])
    
    # меняем размеры и ориентацию готового эксифа
    src_exif["0th"][piexif.ImageIFD.XResolution] = (w, 1)
    src_exif["0th"][piexif.ImageIFD.YResolution] = (h, 1)
    src_exif["0th"][piexif.ImageIFD.Orientation] = 1

    return src_exif

def changeGPS(path, cords):
    # открываем фотку
    image = Image.open(path)
    
    # берем для неё готовый эксиф
    src_exif = getSrcExif(image)
    
    # меняем gps кординаты
    src_exif["GPS"][piexif.GPSIFD.GPSLatitudeRef] = cords.latitude_ref    
    src_exif["GPS"][piexif.GPSIFD.GPSLatitude] = [properCords(cords.latitude)]
    src_exif["GPS"][piexif.GPSIFD.GPSLongitudeRef] = cords.longitude_ref    
    src_exif["GPS"][piexif.GPSIFD.GPSLongitude] = [properCords(cords.longitude)]
    
    # дампим эксиф
    exif_bytes = piexif.dump(src_exif)

    # заливаем эксиф в фотку
    image.save(path, "jpeg", exif=exif_bytes)

def deletePhoto(path):
    os.remove(path)