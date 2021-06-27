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

def makeExif(image, cords):
    # берем размеры
    w, h = image.size
    
    zeroth_ifd = {piexif.ImageIFD.Make: "Iphone",  # ASCII, count any
                piexif.ImageIFD.XResolution: (w, 1),  # RATIONAL, count 1
                piexif.ImageIFD.YResolution: (h, 1),  # RATIONAL, count 1
                piexif.ImageIFD.Orientation: 1,
                piexif.ImageIFD.Software: "ChangeMetaDataBot"  # ASCII, count any
                }
    exif_ifd = {piexif.ExifIFD.ExifVersion: b"\x00\x02\x03\x01",  # UNDEFINED, count 4
                piexif.ExifIFD.LensMake: "Lens",  # ASCII, count any
                piexif.ExifIFD.Sharpness: 65535,  # SHORT, count 1 ... also be accepted '(65535,)'
                piexif.ExifIFD.LensSpecification: ((1, 1), (1, 1), (1, 1), (1, 1)),  # Rational, count 4
                }
    
    lat_cord, lat_st = properCords(cords.latitude)
    long_cord, long_st = properCords(cords.longitude)
    gps_ifd = { piexif.GPSIFD.GPSVersionID: (2, 0, 0, 0),  # BYTE, count 4
                piexif.GPSIFD.GPSAltitudeRef: 1,  # BYTE, count 1 ... also be accepted '(1,)'
                piexif.GPSIFD.GPSLatitudeRef: cords.latitude_ref,
                piexif.GPSIFD.GPSLatitude: [lat_cord, lat_st],
                piexif.GPSIFD.GPSLongitudeRef: cords.longitude_ref,
                piexif.GPSIFD.GPSLongitude: [long_cord, long_st]            
                }
    exif_dict = {"0th":zeroth_ifd, "Exif":exif_ifd, "GPS":gps_ifd}
    exif_bytes = piexif.dump(exif_dict)    

    return exif_bytes

def changeGPS(path, cords):
    # открываем фотку
    image = Image.open(path)
    
    exif_bytes = makeExif(image, cords)

    # заливаем эксиф в фотку
    image.save(path, "jpeg", exif=exif_bytes, quality=100)

def deletePhoto(path):
    os.remove(path)