# Web Migration Implementation Plan

This document tracks the progress of converting the `simple-tts` CLI tool into a modern Web Application using React (Material UI) and FastAPI.

## Phase 1: Backend (FastAPI)

- [x] **1.1 Project Initialization**
    - [x] Create `web-app/backend` directory structure.
    - [x] Create `pyproject.toml` for backend dependencies (fastapi, uvicorn, python-multipart, etc.).
    - [x] Install dependencies.

- [x] **1.2 Core Logic Refactoring**
    - [x] Adapt text extraction logic (from `simple-tts/app.py`) for API usage.
    - [x] Adapt TTS generation logic (using `edge_tts`) for API usage.

- [x] **1.3 API Development**
    - [x] Create `GET /voices` endpoint to list available Vietnamese voices.
    - [x] Create `POST /convert` endpoint to handle text/file input and return audio.
    - [x] Create static file serving for generated audio files.
    - [x] Enable CORS to allow frontend communication.

## Phase 2: Frontend (React + Material UI)

- [x] **2.1 Project Initialization**
    - [x] Scaffold React app using Vite in `web-app/frontend`.
    - [x] Install dependencies: `@mui/material`, `@emotion/react`, `@emotion/styled`, `@mui/icons-material`, `axios`.

- [x] **2.2 Basic UI Layout**
    - [x] Create a responsive App Bar/Header.
    - [x] Set up the main layout container using Material UI `Grid` or `Container`.

- [x] **2.3 Functional Components**
    - [x] **VoiceSelector**: Dropdown to fetch and display available voices.
    - [x] **InputSection**: Tabs for switching between "Text Input" and "File Upload".

- [x] **2.4 Integration**
    - [x] Connect `VoiceSelector` to `GET /voices`.
    - [x] Connect `InputSection` form submission to `POST /convert`.
    - [x] Handle direct file download upon successful conversion.
    - [x] Handle loading states and error messages (Toast/Snackbar).

## Phase 3: Final Polish

- [ ] **3.1 Testing**
    - [ ] Verify text-to-speech works for short texts.
    - [ ] Verify file upload (MD, PDF) conversion works.
    - [ ] Check responsive design on mobile view.

- [x] **3.2 Documentation**
    - [x] Update `README.md` with instructions on how to start both servers.
