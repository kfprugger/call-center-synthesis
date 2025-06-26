#!/usr/bin/env python3

import sys
import os
sys.path.append('/home/ubuntu/contoso-call-center-backend')

from app.services.audio_generator import AudioGenerator

def test_gender_detection():
    ag = AudioGenerator()
    
    print("Testing gender detection:")
    test_names = ["Nicholas", "Dr. Baker", "Baker", "Sarah", "Michael", "Jennifer", "David", "Emily"]
    
    for name in test_names:
        gender = ag._detect_gender_from_name(name)
        print(f"  {name}: {gender}")
    
    print("\nTesting name extraction:")
    test_speakers = ["Agent", "Dr. Baker", "Nicholas", "Agent Sarah", "Dr. Michael Smith"]
    
    for speaker in test_speakers:
        extracted = ag._extract_name_from_speaker(speaker)
        print(f"  '{speaker}' -> '{extracted}'")
    
    print("\nTesting voice configuration:")
    for speaker in ["Agent", "Dr. Baker"]:
        extracted_name = ag._extract_name_from_speaker(speaker)
        voice_config = ag._get_voice_config(speaker, extracted_name)
        print(f"  Speaker: '{speaker}', Name: '{extracted_name}', Voice: {voice_config['voice_name']}")

if __name__ == "__main__":
    test_gender_detection()
