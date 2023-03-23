# Author: @gostaqqs
# Version: 1.0014

import os
import exifread
from datetime import datetime
import pytz
import pyexiv2
from tkinter import Tk, Label, Entry, Button, StringVar, filedialog, messagebox, simpledialog

def get_exif_data(file_path):
    exif_data = {}
    try:
        with open(file_path, 'rb') as f:
            exif_tags = exifread.process_file(f)
            for tag in exif_tags.keys():
                if tag not in ('JPEGThumbnail', 'TIFFThumbnail'):
                    exif_data[tag] = exif_tags[tag].printable
    except (AttributeError, KeyError, IndexError):
        pass
    return exif_data

def convert_to_new_timezone(dt, from_tz, to_tz):
    from_tz = pytz.timezone(from_tz)
    to_tz = pytz.timezone(to_tz)

    dt = from_tz.localize(dt)
    dt_new = dt.astimezone(to_tz)

    return dt_new

def update_exif_data(file_path, date_time_new):
    with pyexiv2.Image(file_path) as img:
        date_time_new_str = date_time_new.strftime('%Y:%m:%d %H:%M:%S')
        
        img.modify_exif({'Exif.Photo.DateTimeOriginal': date_time_new_str})
        img.modify_exif({'Exif.Photo.DateTimeDigitized': date_time_new_str})

def browse_folder():
    folder_path.set(filedialog.askdirectory())

def process_images():
    folder = folder_path.get()
    to_tz = new_timezone.get()

    for file_name in os.listdir(folder):
        file_ext = os.path.splitext(file_name)[1]
        if file_ext.lower() in ('.jpg', '.jpeg', '.cr2', '.arw'):
            file_path = os.path.join(folder, file_name)
            exif_data = get_exif_data(file_path)
            date_time_original_str = exif_data.get('EXIF DateTimeOriginal', 'N/A')

            if date_time_original_str != 'N/A':
                date_time_original = datetime.strptime(date_time_original_str, '%Y:%m:%d %H:%M:%S')

                # Set timezone to Asia/Tokyo
                from_tz = 'Asia/Tokyo'

                date_time_new = convert_to_new_timezone(date_time_original, from_tz, to_tz)

                # Update the DateTimeOriginal and DateTimeDigitized attributes in the image file
                update_exif_data(file_path, date_time_new)

                print(f'File Name: {file_name}, DateTimeOriginal: {date_time_original}, New DateTime: {date_time_new}')
            else:
                print(f'File Name: {file_name}, DateTimeOriginal: N/A')

    # Show message box after all images have been processed
    messagebox.showinfo(title='Success', message='Date and time of all images have been updated')
      
# GUI implementation
root = Tk()
root.title("EXIF TimeZone Repair Tool")

folder_path = StringVar()
new_timezone = StringVar()

Label(root, text="Folder Path:").grid(row=0, column=0, padx=10, pady=10, sticky="W")
Entry(root, textvariable=folder_path, width=40).grid(row=0, column=1, padx=10, pady=10)
Button(root, text="Browse", command=browse_folder).grid(row=0, column=2, padx=10, pady=10)

Label(root, text="New Timezone:").grid(row=1, column=0, padx=10, pady=10, sticky="W")
Entry(root, textvariable=new_timezone, width=40).grid(row=1, column=1, padx=10, pady=10)

Button(root, text="Process Images", command=process_images).grid(row=2, column=1, padx=10, pady=10)

root.mainloop()
