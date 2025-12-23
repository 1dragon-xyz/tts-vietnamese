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

    // 2. State for chunking
    let audioBlobs = [];
    let currentChunkIndex = 0;
    const downloadBtn = document.createElement('button');
    downloadBtn.textContent = "Download Full Audio";
    downloadBtn.style.marginTop = "10px";
    downloadBtn.style.backgroundColor = "#10b981"; // Emerald green
    downloadBtn.style.display = "none";
    
    // Add download button to action group
    document.querySelector('.action-group').appendChild(downloadBtn);

    function splitIntoChunks(text, maxChars = 800) {
        // Split by sentence boundaries while keeping the delimiter
        const sentences = text.match(/[^.!?]+[.!?]+(?:\s+|$)|[^.!?]+$/g) || [text];
        const chunks = [];
        let currentChunk = "";

        for (let sentence of sentences) {
            if ((currentChunk + sentence).length > maxChars && currentChunk !== "") {
                chunks.push(currentChunk.trim());
                currentChunk = sentence;
            } else {
                currentChunk += (currentChunk === "" ? "" : " ") + sentence;
            }
        }
        if (currentChunk) chunks.push(currentChunk.trim());
        return chunks;
    }

    async function fetchAudioChunk(text, voice) {
        const response = await fetch('/api/tts', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text, voice }),
        });

        if (!response.ok) throw new Error('Failed to fetch audio chunk');
        return await response.blob();
    }

    // 3. Handle Conversion
    convertBtn.addEventListener('click', async () => {
        const text = textInput.value.trim();
        const voice = voiceSelect.value;

        if (!text) {
            statusDiv.textContent = "Please enter some text.";
            statusDiv.style.color = "#f87171";
            return;
        }

        // Reset state
        audioBlobs = [];
        currentChunkIndex = 0;
        downloadBtn.style.display = "none";
        
        // Clean up old URLs
        if (audioPlayer.src) URL.revokeObjectURL(audioPlayer.src);
        
        const textChunks = splitIntoChunks(text);
        
        // UI Loading State
        convertBtn.disabled = true;
        convertBtn.textContent = "Processing...";
        statusDiv.textContent = textChunks.length > 1 ? `Preparing ${textChunks.length} parts...` : "Processing...";
        statusDiv.style.color = "#94a3b8";
        audioPlayer.hidden = true;

        try {
            // Fetch and play the first chunk immediately
            const firstBlob = await fetchAudioChunk(textChunks[0], voice);
            audioBlobs[0] = firstBlob;
            
            const firstUrl = URL.createObjectURL(firstBlob);
            audioPlayer.src = firstUrl;
            audioPlayer.hidden = false;
            audioPlayer.play();
            
            statusDiv.textContent = textChunks.length > 1 ? `Playing part 1 of ${textChunks.length}...` : "Done! Audio ready.";
            statusDiv.style.color = "#4ade80";

            // Setup sequential playback first (so it works even if background fetch is slow)
            audioPlayer.onended = () => {
                currentChunkIndex++;
                if (currentChunkIndex < textChunks.length) {
                    playNextChunk();
                } else {
                    statusDiv.textContent = "Playback complete.";
                    // Re-enable convert button only when fully done or if user wants to restart
                    convertBtn.disabled = false; 
                    convertBtn.textContent = "Convert & Play";
                }
            };

            const playNextChunk = () => {
                 if (audioBlobs[currentChunkIndex]) {
                    const url = URL.createObjectURL(audioBlobs[currentChunkIndex]);
                    audioPlayer.src = url;
                    audioPlayer.play();
                    statusDiv.textContent = `Playing part ${currentChunkIndex + 1} of ${textChunks.length}...`;
                } else {
                    statusDiv.textContent = "Buffering next part...";
                    setTimeout(playNextChunk, 200);
                }
            };

            // Background fetch remaining chunks
            const fetchPromises = [];
            for (let i = 1; i < textChunks.length; i++) {
                const p = fetchAudioChunk(textChunks[i], voice)
                    .then(blob => { audioBlobs[i] = blob; })
                    .catch(err => console.error(`Error chunk ${i}:`, err));
                fetchPromises.push(p);
            }

            // Wait for ALL chunks to be ready to enable Download
            await Promise.all(fetchPromises);
            
            // Merge Blobs for Download
            const fullAudioBlob = new Blob(audioBlobs, { type: 'audio/mpeg' });
            const fullAudioUrl = URL.createObjectURL(fullAudioBlob);
            
            downloadBtn.onclick = () => {
                const a = document.createElement('a');
                a.href = fullAudioUrl;
                a.download = "lito_audio.mp3";
                document.body.appendChild(a);
                a.click();
                document.body.removeChild(a);
            };
            downloadBtn.style.display = "block";
            
            // If only 1 chunk, update status to done now
            if (textChunks.length === 1) {
                convertBtn.disabled = false;
                convertBtn.textContent = "Convert & Play";
            }

        } catch (error) {
            console.error(error);
            statusDiv.textContent = "Error converting text.";
            statusDiv.style.color = "#f87171";
            convertBtn.disabled = false;
            convertBtn.textContent = "Convert & Play";
        }
    });
});

