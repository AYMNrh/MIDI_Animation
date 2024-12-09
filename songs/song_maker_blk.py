# song_maker.py
import os
import json
import zipfile
import argparse
from typing import Optional

# Define the list of directories to process
DIRECTORIES = [
    "badpig",
    "bloodystreamjojo",
    "chainsaw",
    "dejavu",
    "feelmyhart",
    "fosterhome",
    "freebird",
    "furelise",
    "gravitystyle",
    "jojoop1",
    "killerqueen",
    "riptide",
    "runaway",
    "rushE",
    "skyfall",
    "strongeryou",
    "teentitans",
    "timmy",
    "vivalavida",
    "wellerman"
]

def song_maker(directory: str) -> Optional[str]:
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

def process_directories() -> list[str]:
    """Process the predefined directories and create song packages."""
    successful_zips = []
    
    for directory in DIRECTORIES:
        if result := song_maker(directory):
            successful_zips.append(result)
            print(f"Created song package: {result}")
        else:
            print(f"Skipping {directory}: Missing required files or invalid directory")
            
    return successful_zips

def main():
    results = process_directories()
    if results:
        print(f"\nSuccessfully created {len(results)} song package(s)")
        for zip_path in results:
            print(f"- {zip_path}")
    else:
        print("\nError: No song packages were created")

if __name__ == '__main__':
    main()

