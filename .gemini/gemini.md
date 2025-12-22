# Vietnamese Text-to-Speech (TTS) Project

## Project Overview

This project provides a collection of Python scripts and a CLI application to convert Vietnamese text content (Plain Text, Markdown, PDF) into audio files using Microsoft Edge's online text-to-speech service (`edge-tts`).

The primary goal is to assist a visually impaired family member by converting written documents into accessible audio formats. The project strives for simplicity and ease of use.

**Key Technologies:**
*   **Python 3.12+**: Core language.
*   **edge-tts**: Python library for Microsoft Edge's online TTS service (free, high quality).
*   **pypdf**: For extracting text from PDF documents.
*   **pygame**: For audio playback in the interactive demo.
*   **uv**: Fast Python package installer and resolver.

## Building and Running

### Prerequisites
*   Python 3.12 or higher.
*   `uv` package manager (`pip install uv`).

### Installation
Sync the environment dependencies using `uv`:
```bash
uv pip sync --python 3.12 simple-tts/pyproject.toml
```

### Running the Application

**1. Main CLI App (Recommended)**
This is the feature-rich application including an onboarding wizard, configuration management, and file conversion menus.
```bash
python simple-tts/app.py
```

**2. Interactive Demo**
A quick script to type text and hear it immediately.
```bash
python simple-tts/main.py
```

**3. Standalone Scripts**
Legacy scripts for specific file types (requires manual path editing in the file):
*   Markdown: `python simple-tts/md_to_audio.py`
*   PDF: `python simple-tts/pdf_to_audio.py`

## Development Conventions

*   **Structure**: The core logic resides in `simple-tts/`. The `documents/` folder is intended for user content.
*   **Async/Await**: The `edge-tts` library is asynchronous, so core conversion functions are `async` and run via `asyncio`.
*   **Configuration**: User settings (voice, destination folder) are stored in `simple-tts/config.json`.
*   **Input Handling**: `simple-tts/app.py` contains robust text cleaning and extraction logic for supported file formats.
*   **Conventions**:
    *   Follow standard Python PEP 8 guidelines.
    *   Use type hinting where possible.
    *   Ensure file paths are handled robustly (cross-platform compatibility).

## Key Files

*   `simple-tts/app.py`: The main entry point for the full CLI application.
*   `simple-tts/main.py`: Simple interactive text-to-speech script.
*   `simple-tts/pyproject.toml`: Project dependencies and configuration.
*   `project-plan/backlog.md`: User stories and future features.
