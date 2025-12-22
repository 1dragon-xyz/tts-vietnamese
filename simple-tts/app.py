import asyncio
import json
import os
import re
import sys
import time
from typing import Optional, List, Dict

import edge_tts
from pypdf import PdfReader

# Constants
CONFIG_FILE = os.path.join(os.path.dirname(__file__), "config.json")
DEFAULT_VOICE = "vi-VN-HoaiMyNeural"
DEFAULT_CONFIG = {
    "voice": DEFAULT_VOICE,
    "destination_folder": "",
    "onboarding_completed": False
}

# --- Configuration Management ---
def load_config() -> Dict:
    if not os.path.exists(CONFIG_FILE):
        save_config(DEFAULT_CONFIG)
        return DEFAULT_CONFIG.copy()
    try:
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return DEFAULT_CONFIG.copy()

def save_config(config: Dict):
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=4)

# --- UI Helpers ---
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header(title: str):
    clear_screen()
    print("=" * 60)
    print(f"  {title}")
    print("=" * 60)
    print()

def get_input(prompt: str, options: Optional[List[str]] = None) -> str:
    while True:
        user_input = input(f"{prompt} ").strip()
        if not options:
            return user_input
        
        # Check if input matches an option (case-insensitive) or an index
        if user_input.lower() in [o.lower() for o in options]:
            return user_input
        
        # Check for numeric selection
        if user_input.isdigit():
            idx = int(user_input) - 1
            if 0 <= idx < len(options):
                return options[idx]
        
        print(f"Invalid input. Please choose from: {', '.join(options)}")

# --- Text Extraction ---
def clean_text(text: str) -> str:
    # Basic cleanup
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def extract_from_md(file_path: str) -> str:
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()
    
    # Remove Headers
    text = re.sub(r'^#+\s+', '', text, flags=re.MULTILINE)
    # Remove Bold/Italic
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)
    text = re.sub(r'\*(.*?)\*', r'\1', text)
    # Remove Links
    text = re.sub(r'\[(.*?)\]\(.*?\)', r'\1', text)
    # Remove horizontal rules
    text = re.sub(r'^-{3,}', '', text, flags=re.MULTILINE)
    # Remove URLs
    text = re.sub(r'http[s]?://\S+', '', text)
    
    return clean_text(text)

def extract_from_pdf(file_path: str) -> str:
    reader = PdfReader(file_path)
    full_text = ""
    for page in reader.pages:
        text = page.extract_text()
        if text:
            full_text += text + "\n"
    
    # Improve PDF text flow
    full_text = full_text.replace('\u200b', '')
    lines = full_text.split('\n')
    cleaned_text = ""
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if line[-1] in ['.', '!', '?', ':', ';']:
            cleaned_text += line + "\n"
        else:
            cleaned_text += line + " "
            
    return clean_text(cleaned_text)

def extract_text(file_path: str) -> str:
    _, ext = os.path.splitext(file_path)
    ext = ext.lower()
    
    if ext == '.md':
        return extract_from_md(file_path)
    elif ext == '.pdf':
        return extract_from_pdf(file_path)
    elif ext == '.txt':
        with open(file_path, 'r', encoding='utf-8') as f:
            return clean_text(f.read())
    else:
        raise ValueError(f"Unsupported file format: {ext}")

# --- TTS Conversion ---
async def convert_file(config: Dict, source_path: str):
    if not os.path.exists(source_path):
        print(f"Error: File not found: {source_path}")
        input("Press Enter to continue...")
        return

    try:
        print(f"Extracting text from {os.path.basename(source_path)}...")
        text = extract_text(source_path)
        if not text:
            print("Error: No text extracted.")
            input("Press Enter to continue...")
            return
            
        # Determine output path
        dest_folder = config.get("destination_folder")
        if not dest_folder or not os.path.exists(dest_folder):
            dest_folder = os.path.dirname(source_path)
            
        filename = os.path.basename(source_path)
        base_name = os.path.splitext(filename)[0]
        output_path = os.path.join(dest_folder, f"{base_name}.mp3")
        
        print(f"Converting to audio (Voice: {config['voice']})...")
        print(f"Output: {output_path}")
        print("Progress: ", end="", flush=True)

        communicate = edge_tts.Communicate(text, config['voice'])
        
        with open(output_path, "wb") as f:
            async for chunk in communicate.stream():
                if chunk["type"] == "audio":
                    f.write(chunk["data"])
                    print(".", end="", flush=True)
                elif chunk["type"] == "WordBoundary":
                    pass # Can be used for subtitles/timing

        print("\n\nSuccess! Conversion complete.")
        
        choice = get_input("Convert another file? (y/n)", ["y", "n"])
        if choice.lower() == 'n':
            return "exit"
            
    except Exception as e:
        print(f"\nError during conversion: {e}")
        input("Press Enter to continue...")

# --- Menus & Wizard ---

async def list_voices() -> List[Dict]:
    try:
        voices = await edge_tts.list_voices()
        return [v for v in voices if "Viet" in v["FriendlyName"]]
    except Exception:
        return []

def show_tutorial():
    print_header("Tutorial")
    print("Welcome to Simple TTS!")
    print("\nHow to use:")
    print("1. Select 'Convert File' from the main menu.")
    print("2. Enter the full path to your .txt, .md, or .pdf file.")
    print("3. Wait for the conversion to complete.")
    print("4. Your audio file will be saved in the configured destination folder")
    print("   (or the same folder as the source file if not configured).")
    print("\nSupported formats:")
    print("- Text files (.txt)")
    print("- Markdown files (.md)")
    print("- PDF documents (.pdf)")
    print()
    input("Press Enter to return...")

async def configure_settings(config: Dict):
    while True:
        print_header("Settings")
        print(f"1. Voice (Current: {config['voice']})")
        print(f"2. Destination Folder (Current: {config['destination_folder'] or 'Same as source'})")
        print("3. Back")
        
        choice = get_input("Select an option:", ["1", "2", "3"])
        
        if choice == "1":
            print("\nFetching voices...")
            voices = await list_voices()
            print("\nAvailable Vietnamese Voices:")
            for i, v in enumerate(voices):
                print(f"{i+1}. {v['ShortName']} ({v['Gender']})")
            
            sel = get_input("Select voice number:", [str(i+1) for i in range(len(voices))])
            config['voice'] = voices[int(sel)-1]['ShortName']
            save_config(config)
            print("Voice updated.")
            time.sleep(1)
            
        elif choice == "2":
            path = get_input("Enter new destination folder path (leave empty for source folder):")
            if path and not os.path.exists(path):
                print("Warning: Folder does not exist.")
                if get_input("Create it? (y/n)", ["y", "n"]) == 'y':
                    try:
                        os.makedirs(path)
                        config['destination_folder'] = path
                    except Exception as e:
                        print(f"Could not create folder: {e}")
                else:
                    print("Setting not changed.")
            else:
                config['destination_folder'] = path
            save_config(config)
            
        elif choice == "3":
            break

async def onboarding_wizard(config: Dict):
    print_header("Welcome to Simple TTS")
    print("This tool helps you convert your documents into speech.")
    print("\nWhat would you like to do?")
    print("1. See Tutorial")
    print("2. Configure Settings")
    print("3. Set Destination Folder")
    print("4. Skip Setup")
    
    choice = get_input("Select an option:", ["1", "2", "3", "4"])
    
    if choice == "1":
        show_tutorial()
    elif choice == "2":
        await configure_settings(config)
    elif choice == "3":
        path = get_input("Enter destination folder path:")
        if path:
            if not os.path.exists(path):
                os.makedirs(path, exist_ok=True)
            config['destination_folder'] = path
            save_config(config)
            print("Destination folder saved.")
            time.sleep(1)
            
    config['onboarding_completed'] = True
    save_config(config)

async def main_menu():
    config = load_config()
    
    if not config['onboarding_completed']:
        await onboarding_wizard(config)
        # Reload config in case it changed
        config = load_config()
        
    while True:
        print_header("Simple TTS - Main Menu")
        print("1. Convert File")
        print("2. Settings")
        print("3. Tutorial")
        print("4. Exit")
        
        choice = get_input("Select an option:", ["1", "2", "3", "4"])
        
        if choice == "1":
            path = get_input("Enter path to source file:")
            # Remove quotes if user copied path as "path/to/file"
            path = path.strip('"').strip("'")
            
            print(f"\nSource: {path}")
            if get_input("Confirm conversion? (y/n)", ["y", "n"]) == 'y':
                res = await convert_file(config, path)
                if res == "exit":
                    break
        elif choice == "2":
            await configure_settings(config)
        elif choice == "3":
            show_tutorial()
        elif choice == "4":
            print("Goodbye!")
            break

if __name__ == "__main__":
    try:
        asyncio.run(main_menu())
    except KeyboardInterrupt:
        print("\nGoodbye!")
