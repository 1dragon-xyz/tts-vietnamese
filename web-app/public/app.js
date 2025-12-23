document.addEventListener('DOMContentLoaded', () => {
    const voiceSelect = document.getElementById('voice-select');
    const textInput = document.getElementById('text-input');
    const convertBtn = document.getElementById('convert-btn');
    const statusDiv = document.getElementById('status');
    const audioPlayer = document.getElementById('audio-player');

    // 1. Load Voices
    async function loadVoices() {
        try {
            const response = await fetch('/api/voices');
            const voices = await response.json();
            
            voiceSelect.innerHTML = '';
            voices.forEach(voice => {
                const option = document.createElement('option');
                option.value = voice.ShortName;
                option.textContent = voice.FriendlyName;
                voiceSelect.appendChild(option);
            });
        } catch (error) {
            statusDiv.textContent = "Error loading voices.";
            statusDiv.style.color = "red";
        }
    }

    loadVoices();

    // 2. Handle Conversion
    convertBtn.addEventListener('click', async () => {
        const text = textInput.value.trim();
        const voice = voiceSelect.value;

        if (!text) {
            statusDiv.textContent = "Please enter some text.";
            statusDiv.style.color = "#f87171"; // Red
            return;
        }

        // UI Loading State
        convertBtn.disabled = true;
        convertBtn.textContent = "Converting...";
        statusDiv.textContent = "Processing...";
        statusDiv.style.color = "#94a3b8"; // Default
        audioPlayer.hidden = true;

        try {
            const response = await fetch('/api/tts', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ text, voice }),
            });

            if (!response.ok) {
                throw new Error('Conversion failed');
            }

            // Create audio blob URL
            const blob = await response.blob();
            const url = URL.createObjectURL(blob);
            
            audioPlayer.src = url;
            audioPlayer.hidden = false;
            audioPlayer.play();

            statusDiv.textContent = "Done! Audio ready.";
            statusDiv.style.color = "#4ade80"; // Green
        } catch (error) {
            console.error(error);
            statusDiv.textContent = "Error converting text.";
            statusDiv.style.color = "#f87171";
        } finally {
            convertBtn.disabled = false;
            convertBtn.textContent = "Convert & Play";
        }
    });
});
