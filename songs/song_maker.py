# song_maker.py
import os
import json
import zipfile
import argparse
from typing import Optional


def song_maker(directory: str):
    # Check if directory exists
    if not os.path.isdir(directory):
        return None
        
    # Find midi and mp3 files
    midi_file = None
    mp3_file = None
    
    for file in os.listdir(directory):
        if file.endswith('.mid'):
            midi_file = file
        elif file.endswith('.mp3'):
            mp3_file = file
            
    if not (midi_file and mp3_file):
        return None
        
    # Create metadata
    song_name = os.path.splitext(midi_file)[0]  # Use midi filename without extension
    metadata = {
        "name": song_name,
        "author": "etuvip",
        "mapper": "etuvip", 
        "version": 1,
        "song_file": midi_file,
        "audio_file": mp3_file
    }
    
    # Write metadata to file
    metadata_path = os.path.join(directory, 'metadata.json')
    with open(metadata_path, 'w') as f:
        json.dump(metadata, f, indent=4)
        
    # Create zip file in songs directory
    songs_dir = os.path.dirname(os.path.abspath(__file__))  # Get the songs directory path
    zip_path = os.path.join(songs_dir, f"{song_name}.zip")
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        zipf.write(os.path.join(directory, midi_file), midi_file)
        zipf.write(os.path.join(directory, mp3_file), mp3_file)
        zipf.write(metadata_path, 'metadata.json')
        
    return zip_path


def main():
    parser = argparse.ArgumentParser(description='Create a song package from MIDI and MP3 files')
    parser.add_argument('directory', type=str, help='Directory containing the MIDI and MP3 files')
    
    args = parser.parse_args()
    
    result = song_maker(args.directory)
    if result:
        print(f"Successfully created song package at: {result}")
    else:
        print("Error: Could not create song package. Make sure the directory exists and contains both MIDI and MP3 files.")


if __name__ == '__main__':
    main()

