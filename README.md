# Vietnamese Text-to-Speech (TTS) Utility

A lightweight native desktop application to convert Vietnamese text content from various formats into high-quality audio files using Microsoft Edge's online TTS services.

## Features

- **Lightweight UI:** Built with Python's native `tkinter`, ensuring a small footprint and fast startup.
- **Format Support:** Converts plain text, Markdown (.md), and PDF files.
- **Native Playback:** Opens generated audio files in your default system media player.
- **High Quality:** Uses `edge-tts` for natural-sounding Vietnamese voices.

## Setup & Installation

This project uses `uv` for package management.

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/anhdhnguyen/tts-vietnamese.git
    cd tts-vietnamese
    ```

2.  **Install dependencies:**
    ```bash
    uv pip sync desktop-app/pyproject.toml
    ```

## How to Use

Run the desktop application:

```bash
python desktop-app/main.py
```

### Usage Steps:
1.  **Select a Voice:** Choose between Female (Hoai My) and Male (Nam Minh) voices.
2.  **Input Text:** Either type directly in the "Text Input" tab or upload a file in the "File Upload" tab.
3.  **Convert:** Click "Convert to Audio". The file will be saved to your `Documents/VietnameseTTS` folder.
4.  **Play Audio:** Click "Play Audio" to open the result in your default media player.

## Directory Structure

```
.
├── desktop-app/        # Native Desktop Application (Tkinter)
├── simple-tts/         # Legacy CLI scripts
├── documents/          # Suggested folder for input files
└── README.md
```

## Contributing

Contributions are welcome! If you have ideas for improvements, feel free to open an issue or submit a pull request.
