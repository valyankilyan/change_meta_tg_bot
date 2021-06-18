from loggingconfig import getLogger
log = getLogger(__name__)

from exif import Image
import os


path = './images'

files = os.listdir(path)
images = []

latitude = 62.304588
latitude_ref = 'N'
longitude = 34.579684 
longitude_ref = 'E'

log.info('Listing files')
for f in files:
    with open(path + '/' + f, 'rb') as file:
        image = Image(file)
        log.info('----------------------')
        log.info(f'file {f} has read')
        try:
            log.info(f"Latitude: {image.gps_latitude} {image.gps_latitude_ref}")
            log.info(f"Longitude: {image.gps_longitude} {image.gps_longitude_ref}")
        except:
            log.error(f'Image {f} does not have gps exif data')
    # image.gps_latitude = latitude
    # image.gps_latitude_ref = latitude_ref
    # image.gps_longitude = longitude
    # image.gps_longitude_ref = longitude_ref
    # with open(f'{path}/{f}', 'wb') as updated_file:
    #     updated_file.write(image.get_file())
    images.append(image)
    # log.info(f'File {f} has read')


# for index, image in enumerate(images):
#     try:
#         if image.has_exif:
#             status = f"contains EXIF (version {image.exif_version}) information."
#         else:
#             status = "does not contain any EXIF information."
#         print(f"Image {index} {status}")
#     except:
#         pass
        
        
# for image in images:
#     try:
#         image_members = dir(image)
#         print(f"Image contains {len(image_members)} members:")
#         print(f"{image_members}\n")
#         for i in image_members:
#             print(f'{i} = {getattr(image,i) if len(str(getattr(image,i))) < 10000 else "too long"}')
#     except:
#         pass
    
# for index, image in enumerate(images):
#     try:
#         print(f"Coordinates - Image {index}")
#         print("---------------------")
#         print(f"Latitude: {image.gps_latitude} {image.gps_latitude_ref}")
#         print(f"Longitude: {image.gps_longitude} {image.gps_longitude_ref}\n")
#     except:
#         print("media doesn't contain gps data")
        
    

# for index, image in enumerate(images):
#     try:
#         print(f"Device information - Image {index}")
#         print("----------------------------")
#         print(f"Make: {image.make}")
#         print(f"Model: {image.model}\n")
#     except:
#         pass
    
# for index, image in enumerate(images):
#     try:
#         print(f"Lens and OS - Image {index}")
#         print("---------------------")
#         print(f"Lens make: {image.get('lens_make', 'Unknown')}")
#         print(f"Lens model: {image.get('lens_model', 'Unknown')}")
#         print(f"Lens specification: {image.get('lens_specification', 'Unknown')}")
#         print(f"OS version: {image.get('software', 'Unknown')}\n")
#     except:
#         pass
    
# for index, image in enumerate(images):
#     try:
#         print(f"Date/time taken - Image {index}")
#         print("-------------------------")
#         print(f"{image.datetime_original}.{image.subsec_time_original} {image.get('offset_time', '')}\n")
#     except:
#         print('doesnt')
        
        
# def format_dms_coordinates(coordinates):
#     return f"{coordinates[0]}° {coordinates[1]}\' {coordinates[2]}\""

# def dms_coordinates_to_dd_coordinates(coordinates, coordinates_ref):
#     decimal_degrees = coordinates[0] + \
#                       coordinates[1] / 60 + \
#                       coordinates[2] / 3600
    
#     if coordinates_ref == "S" or coordinates_ref == "W":
#         decimal_degrees = -decimal_degrees
    
#     return decimal_degrees

# for index, image in enumerate(images):
#     try:
#         print(f"Coordinates - Image {index}")
#         print("---------------------")
#         print(f"Latitude (DMS): {format_dms_coordinates(image.gps_latitude)} {image.gps_latitude_ref}")
#         print(f"Longitude (DMS): {format_dms_coordinates(image.gps_longitude)} {image.gps_longitude_ref}\n")
#         print(f"Latitude (DD): {dms_coordinates_to_dd_coordinates(image.gps_latitude, image.gps_latitude_ref)}")
#         print(f"Longitude (DD): {dms_coordinates_to_dd_coordinates(image.gps_longitude, image.gps_longitude_ref)}\n")
#     except:
#         print("something went wrong")