import os

def rename_audio_file(old_filepath, new_filename):
    # Get the directory path of the old file
    directory = os.path.dirname(old_filepath)
    # Get the file extension of the old file
    extension = os.path.splitext(old_filepath)[1]
    # Create the new file path
    new_filepath = os.path.join(directory, new_filename + extension)
    # Rename the file
    os.rename(old_filepath, new_filepath)


