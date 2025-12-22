# Desktop App Implementation Plan (Tkinter)

This document tracks the creation of the lightweight native Python desktop application.

## Phase 1: Setup & Core Logic

- [x] **1.1 Initialization**
    - [x] Create `desktop-app` directory.
    - [x] Create `pyproject.toml` with `edge-tts`, `pypdf` (No GUI lib needed).
    - [x] Install dependencies.

- [x] **1.2 Logic Migration**
    - [x] Extract text processing logic (PDF/MD/TXT) into `desktop-app/logic.py`.
    - [x] Create a `TTSManager` class to handle `edge-tts` and file saving.

## Phase 2: GUI Implementation (Tkinter)

- [x] **2.1 Main Window Layout**
    - [x] Setup `tk.Tk` window with a native `vista` theme.
    - [x] Create a clean, padded layout using `ttk.Frame` and `pack`.

- [x] **2.2 Components**
    - [x] **Voice Selector:** `ttk.Combobox` populated with Vietnamese voices.
    - [x] **Input Area:** A `ttk.Notebook` switching between "Text" and "File".
    - [x] **Controls:** "Convert" button and "Play Audio" button.

- [x] **2.3 Asynchronous Integration**
    - [x] Implement `threading` to run `edge-tts` without freezing the UI.
    - [x] Use `root.after` to safely update the UI from the background thread.
    - [x] Use `os.startfile` for zero-cost audio playback.

## Phase 3: Cleanup & Packaging

- [x] **3.1 Clean Legacy Code**
    - [x] Archive/Delete the `web-app` directory.

- [x] **3.2 Packaging**
    - [x] Create PyInstaller spec file.
    - [x] Build the single-file executable (`.exe`).
    - [x] Achievement Unlocked: Final build size is ~12MB.
