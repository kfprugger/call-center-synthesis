#!/usr/bin/env python3

import sys
import os
sys.path.append('/home/ubuntu/cc-proj/contoso-call-center-backend')

from app.services.audio_generator import AudioGenerator
from pydub import AudioSegment

def test_windows_audio_combination():
    """Debug Windows audio combination issue step by step."""
    print("=== Debugging Windows Audio Combination Issue ===\n")
    
    os.environ['SPEECH_KEY'] = 'BHNTpO3MwvVchOW7T1qmMA9MKhO2uzkJKya52wVU6IQ9uXwf6jzIJQQJ99BFACMsfrFXJ3w3AAAYACOGJ1BP'
    
    generator = AudioGenerator()
    
    transcript = """Agent Sarah: Thank you for calling Contoso Medical, this is Sarah. How can I help you today?
Dr. Baker: Hi Sarah, this is Dr. Baker from City General Hospital. I'm calling about a patient encounter we had last week.
Agent Sarah: Of course, Dr. Baker. I'd be happy to help you with that information."""
    
    audio_settings = {
        'sampling_rate': 16000,
        'channels': 1
    }
    
    print("Testing full audio generation with enhanced debugging...")
    result = generator.generate_audio(transcript, audio_settings, "debug_windows_combination_20250627")
    
    if result:
        print(f"✅ Audio generation successful: {result}")
        if os.path.exists(result):
            file_size = os.path.getsize(result)
            print(f"File size: {file_size} bytes")
            return file_size > 0
        else:
            print("❌ File not found")
            return False
    else:
        print("❌ Audio generation failed")
        return False

if __name__ == "__main__":
    success = test_windows_audio_combination()
    print(f"\n=== Test Result ===")
    if success:
        print("🎉 Windows audio combination fix is working!")
    else:
        print("⚠️  Windows audio combination still has issues")
