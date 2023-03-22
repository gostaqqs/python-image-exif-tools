# Author: @gostaqqs
# Version: 1.0006

import os
import pytz
from datetime import datetime
from dateutil import parser
import piexif

def get_timezone(prompt):
    while True:
        try:
            tz_str = input(prompt)
            return pytz.timezone(tz_str)
        except pytz.UnknownTimeZoneError:
            print("Invalid timezone. Please try again.")

def main():
    folder_path = input("Enter the folder path: ")
    original_tz = pytz.timezone("Asia/Tokyo")
    new_tz = get_timezone("Enter the corrected timezone (e.g. 'America/New_York'): ")

    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith((".jpg", ".jpeg")):
                file_path = os.path.join(root, file)

                try:
                    exif_dict = piexif.load(file_path)

                    if piexif.ExifIFD.DateTimeOriginal in exif_dict["Exif"]:
                        original_datetime_str = exif_dict["Exif"][piexif.ExifIFD.DateTimeOriginal].decode("utf-8")
                        print(f"Original datetime string: {original_datetime_str}")
                        
                        original_datetime = parser.parse(original_datetime_str, yearfirst=True)
                        print(f"Original datetime: {original_datetime}")
                        
                        original_datetime = original_tz.localize(original_datetime)
                        print(f"Original datetime localized: {original_datetime}")
                        
                        new_datetime = original_datetime.astimezone(new_tz)
                        print(f"New datetime: {new_datetime}")
                        
                        exif_dict["Exif"][piexif.ExifIFD.DateTimeOriginal] = new_datetime.strftime("%Y:%m:%d %H:%M:%S").encode("utf-8")

                        exif_bytes = piexif.dump(exif_dict)

                        with open(file_path, "rb") as image_file:
                            img = image_file.read()

                        piexif.insert(exif_bytes, img, file_path)

                    print(f"Updated 'Date taken' for {file}.")
                except Exception as e:
                    print(f"Unexpected error processing '{file}': {e}. Skipping file.")

    print("Finished processing files.")

if __name__ == "__main__":
    main()
