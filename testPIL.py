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
    
    

    zeroth_ifd = {piexif.ImageIFD.Make: "Iphone",  # ASCII, count any
                piexif.ImageIFD.XResolution: (w, 1),  # RATIONAL, count 1
                piexif.ImageIFD.YResolution: (h, 1),  # RATIONAL, count 1
                piexif.ImageIFD.Orientation: 1,
                piexif.ImageIFD.Software: "piexif"  # ASCII, count any
                }
    exif_ifd = {piexif.ExifIFD.ExifVersion: b"\x00\x02\x03\x01",  # UNDEFINED, count 4
                piexif.ExifIFD.LensMake: "Lens",  # ASCII, count any
                piexif.ExifIFD.Sharpness: 65535,  # SHORT, count 1 ... also be accepted '(65535,)'
                piexif.ExifIFD.LensSpecification: ((1, 1), (1, 1), (1, 1), (1, 1)),  # Rational, count 4
                }
    lat_cord, lat_st = properCords(latitude)
    long_cord, long_st = properCords(longitude)
    gps_ifd = { piexif.GPSIFD.GPSVersionID: (2, 0, 0, 0),  # BYTE, count 4
                piexif.GPSIFD.GPSAltitudeRef: 1,  # BYTE, count 1 ... also be accepted '(1,)'
                piexif.GPSIFD.GPSLatitudeRef: latitude_ref,
                piexif.GPSIFD.GPSLatitude: [lat_cord, lat_st],
                piexif.GPSIFD.GPSLongitudeRef: longitude_ref,
                piexif.GPSIFD.GPSLongitude: [long_cord, long_st]            
                }
    exif_dict = {"0th":zeroth_ifd, "Exif":exif_ifd, "GPS":gps_ifd}
    exif_bytes = piexif.dump(exif_dict)

    # round trip
    # piexif.insert(exif_bytes, "foo.jpg")
    # exif_dict_tripped = piexif.load("foo.jpg")


    
    # # берем готовый эксиф
    # src_exif = piexif.load(src_photo.info['exif'])
    # # b'0231'
    
    # # меняем у него размеры
    # src_exif["0th"][piexif.ImageIFD.XResolution] = (w, 1)
    # src_exif["0th"][piexif.ImageIFD.YResolution] = (h, 1)
    # src_exif["0th"][piexif.ImageIFD.Orientation] = 1
    
    # # меняем жпс
    # src_exif["GPS"][piexif.GPSIFD.GPSLatitudeRef] = latitude_ref
    # cord, st = properCords(latitude)
    # print(cord, st)
    # src_exif["GPS"][piexif.GPSIFD.GPSLatitude] = [cord, st]
    # src_exif["GPS"][piexif.GPSIFD.GPSLongitudeRef] = longitude_ref
    # cord, st = properCords(longitude)
    # print(cord, st)
    # src_exif["GPS"][piexif.GPSIFD.GPSLongitude] = [cord, st]
    
    # # дампим эксиф
    # exif_bytes = piexif.dump(src_exif)
    
    # заливаем эксив в фотку
    im.save('.' + ph.split('.')[1] + '_CHANGED_.' + ph.split('.')[2], "jpeg", exif=exif_bytes)
