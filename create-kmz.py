import zipfile
import os
import shutil

def zip_folder(folder_path, zip_name):
    # Create a zip file with the desired name
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(folder_path):
            for file_name in files:
                # Construct the full path to the file
                full_path = os.path.join(root, file_name)
                # Add the file to the zip, preserving the relative path
                relative_path = os.path.relpath(full_path, folder_path)
                zipf.write(full_path, relative_path)

    # Rename the file extension to .kmz
    kmz_name = os.path.splitext(zip_name)[0] + '.kmz'
    shutil.move(zip_name, kmz_name)
    print(f'{folder_path} has been zipped and renamed to {kmz_name}.')

# Example usage
folder_to_zip = 'KMZBasedirectory'
zip_name = 'output.zip'

zip_folder(folder_to_zip, zip_name)
