### Python 3.x
from exif import Image
from datetime import datetime
import os
from os.path import getmtime
import sys
import shutil
import re
# unix style
#image_folder = "/home/pina/Bilder/20190906-Toskana/"
#output_folder = "/home/pina/Bilder/20190906-Toskana-by-day/"
#windows style
image_folder = 'd:\\_photopath\\2019-09-15_hikingtour\\'
#store in same folder as a subfolder named "devided" 
divided_folder = 'divided'
output_folder = os.path.join(image_folder, divided_folder)

filename_regex = r"(?P<filename>.*)\.(?P<extension>JPG|jpg|jpeg|PNG|png|tiff|tif|TIF|BMP|bmp)"

# Count the images for the progress bar
image_count = 0

with os.scandir(image_folder) as it:
    for entry in it:
       if entry.is_file():
            #print('File: ' + entry.name)
            filename_matches = re.finditer(filename_regex, entry.name, re.UNICODE)
            filename, extension = None, None
            for match in filename_matches:
               filename, extension = match.groups()
            if not filename or not extension:
               continue
            image_count += 1       
print('image_count:')
print(image_count)
print("\n")

# Do the actual work
progressbar_width = 40
bar_str = "[%s]" % (" " * progressbar_width)
sys.stdout.write(bar_str)
sys.stdout.flush()
sys.stdout.write("\b" * len(bar_str))
copied_image_count = 0
subfolder = ''
with os.scandir(image_folder) as it:
    if entry.is_dir():
        subfolder = entry.name
    else:
        for entry in it:   
          if entry.is_file():
                filename_matches = re.finditer(filename_regex, entry.name, re.UNICODE)
                filename, extension = None, None
                for match in filename_matches:
                    filename, extension = match.groups()
                if not filename or not extension:
                    continue
                with open(os.path.join(image_folder, subfolder, entry.name), 'rb') as file:
                    image_obj = Image(file)
                if image_obj.has_exif:
                    image_time = datetime.strptime(image_obj.datetime, "%Y:%m:%d %H:%M:%S")
                else:
                    print("The file " + os.path.join(image_folder, subfolder, entry.name) + "has no exif data.")
                    #image_time_tmp = os.path.getmtime(os.path.join(image_folder, subfolder, entry.name))
                    datetime.fromtimestamp(getmtime(os.path.join(image_folder, subfolder, entry.name))).strftime('%m/%d/%Y')
                    print("Last modification time since the epoch:", image_time)
                    print('Mv_File: ' + entry.name)
                day_str = image_time.strftime("%Y-%m-%d_%A")
                if not os.path.exists(os.path.join(output_folder, day_str)):
                    os.makedirs(os.path.join(output_folder, day_str))
                shutil.copy2(
                    os.path.join(image_folder, subfolder, entry.name),
                    os.path.join(output_folder, day_str, image_time.strftime("%Y-%m-%d_%H%M%S_") + subfolder + "_" + filename + "." + extension.lower()))
                copied_image_count += 1
                progress = copied_image_count / image_count
                bar_str = "[%s] %d%%" % (
                    "=" * int(progress*progressbar_width) + " " * (progressbar_width - int(progress*progressbar_width)),
                    (progress * 100))
                sys.stdout.write(bar_str)
                sys.stdout.flush()
                sys.stdout.write("\b" * len(bar_str))
        sys.stdout.write("\n")
