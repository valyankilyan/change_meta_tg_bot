import os
import io
from PIL import Image
import piexif

path = './images'

# лоадим эксив срс 
src_path = 'exif_src.JPG'
src_photo = Image.open(src_path)

latitude = 62.304588
latitude_ref = 'N'
longitude = 34.579684 
longitude_ref = 'E'

# находим все файлы в папке
files = os.listdir(path)

def properCords(cord):
    ans = len(str(cord).split('.')[1])
    m = 10 ** ans
    return int(cord * m), m

for f in files:
    
    # exif_dict = piexif.load(im.info["exif"])
    # process im and exif_dict...
    
    
    # exif_bytes = piexif.dump(exif_dict)
    # im.save(new_file, "jpeg", exif=exif_bytes)
    # piexif.transplant(src, ph)
    
    # берем данные размера фотографии (и ориентации возможно)
    ph = path + '/' + f
    im = Image.open(ph)
    w, h = im.size
    
    # берем готовый эксиф
    src_exif = piexif.load(src_photo.info['exif'])
    
    # меняем у него размеры
    src_exif["0th"][piexif.ImageIFD.XResolution] = (w, 1)
    src_exif["0th"][piexif.ImageIFD.YResolution] = (h, 1)
    src_exif["0th"][piexif.ImageIFD.Orientation] = 1
    
    # меняем жпс
    src_exif["GPS"][piexif.GPSIFD.GPSLatitudeRef] = latitude_ref
    cord, st = properCords(latitude)
    print(cord, st)
    src_exif["GPS"][piexif.GPSIFD.GPSLatitude] = [cord, st]
    src_exif["GPS"][piexif.GPSIFD.GPSLongitudeRef] = longitude_ref
    cord, st = properCords(longitude)
    print(cord, st)
    src_exif["GPS"][piexif.GPSIFD.GPSLongitude] = [cord, st]
    
    # дампим эксиф
    exif_bytes = piexif.dump(src_exif)
    
    # заливаем эксив в фотку
    im.save(ph, "jpeg", exif=exif_bytes)
