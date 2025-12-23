import os
import re
import asyncio
from typing import List, Dict
import edge_tts
from pypdf import PdfReader

class TextProcessor:
    @staticmethod
    def clean_text(text: str) -> str:
        text = re.sub(r'\s+', ' ', text)
        return text.strip()

    @staticmethod
    def extract_from_md(content: str) -> str:
        text = content
        text = re.sub(r'^#+\s+', '', text, flags=re.MULTILINE)
        text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)
        text = re.sub(r'\*(.*?)\*', r'\1', text)
        text = re.sub(r'\[(.*?)\]\(.*?\)', r'\1', text)
        text = re.sub(r'^-{3,}', '', text, flags=re.MULTILINE)
        text = re.sub(r'http[s]?://\S+', '', text)
        return TextProcessor.clean_text(text)

    @staticmethod
    def extract_from_pdf(file_path: str) -> str:
        reader = PdfReader(file_path)
        full_text = ""
        for page in reader.pages:
            text = page.extract_text()
            if text:
                full_text += text + "\n"
        
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
        return TextProcessor.clean_text(cleaned_text)

    @classmethod
    def process_file(cls, file_path: str) -> str:
        _, ext = os.path.splitext(file_path)
        ext = ext.lower()
        
        if ext == '.pdf':
            return cls.extract_from_pdf(file_path)
        elif ext in ['.md', '.txt']:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                return cls.extract_from_md(content) if ext == '.md' else cls.clean_text(content)
        return ""

class TTSManager:
    def __init__(self):
        self.output_dir = os.path.join(os.path.expanduser("~"), "Documents", "VietnameseTTS")
        os.makedirs(self.output_dir, exist_ok=True)

    async def get_voices(self) -> List[Dict]:
        voices = await edge_tts.list_voices()
        
        # Define the specific high-quality voices we want to support
        target_voices = {
            "vi-VN-HoaiMyNeural": "Vietnamese (Female)",
            "vi-VN-NamMinhNeural": "Vietnamese (Male)",
            "en-US-AvaNeural": "English (Female)",
            "en-US-AndrewNeural": "English (Male)",
            "zh-CN-XiaoxiaoNeural": "Chinese (Female)",
            "zh-CN-YunxiNeural": "Chinese (Male)"
        }
        
        filtered_voices = []
        for v in voices:
            short_name = v.get("ShortName", "")
            if short_name in target_voices:
                 filtered_voices.append({
                    "ShortName": v["ShortName"],
                    "FriendlyName": target_voices[short_name], # Use our simplified name
                    "Gender": v["Gender"],
                    "Locale": v.get("Locale", "Unknown") 
                })
        
        # Sort so it's consistent: VI, EN, ZH
        order = ["vi-VN", "en-US", "zh-CN"]
        filtered_voices.sort(key=lambda x: (order.index(x['Locale']) if x['Locale'] in order else 99, x['Gender']))
        
        return filtered_voices

    async def convert(self, text: str, voice: str, output_path: str, cancel_event=None) -> str:
        """
        Returns: 'success', 'cancelled', or 'error'
        """
        try:
            communicate = edge_tts.Communicate(text, voice)
            with open(output_path, "wb") as f:
                async for chunk in communicate.stream():
                    if cancel_event and cancel_event.is_set():
                        f.close()
                        if os.path.exists(output_path):
                            os.remove(output_path)
                        return "cancelled"

                    if chunk["type"] == "audio":
                        f.write(chunk["data"])
                            
            return "success"
        except Exception as e:
            print(f"TTS Error: {e}")
            if os.path.exists(output_path):
                os.remove(output_path)
            return "error"