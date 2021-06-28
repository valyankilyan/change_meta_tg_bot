from loggingconfig import getLogger
log = getLogger(__name__)

import os
import PIL
# from PIL import Image
import piexif 

def getImageQuality(original_img):    
    quantization = getattr(original_img, 'quantization', None)
    subsampling = PIL.JpegImagePlugin.get_sampling(original_img)
    quality = 95 if quantization is None else -1
    return quality, quantization, subsampling

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
    image = PIL.Image.open(path)
    
    quality, quantization, subsampling = getImageQuality(image)
    
    exif_bytes = makeExif(image, cords)

    # заливаем эксиф в фотку
    image.save(path, "jpeg", exif=exif_bytes, quality=quality,
               subsampling=subsampling, qtables=quantization)

def changeFormat(path, fmt):
    log.debug('Format changing...')
    new_path = ''
    if fmt == 'png':
        new_path = replace_last(path, '.png', '.jpg')
        image = PIL.Image.open(path)
        log.debug(f"Saving photo in {new_path}")
        rgb_im = image.convert('RGB')
        rgb_im.save(new_path, quality=95)
    log.debug('Image successfully saved in JPG format')
    deletePhoto(path)
    return new_path

def replace_last(source_string, replace_what, replace_with):
    head, _sep, tail = source_string.rpartition(replace_what)
    return head + replace_with + tail     

def deletePhoto(path):
    os.remove(path)
    