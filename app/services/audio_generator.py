import io
import wave
import numpy as np
import azure.cognitiveservices.speech as speechsdk
from pydub import AudioSegment
from pydub.generators import Sine
import tempfile
import os
from typing import Dict, Optional, Tuple, Union
import base64
import gender_guesser.detector as gender

class AudioGenerator:
    def __init__(self):
        self.voice_settings = {
            'agent': {
                'male': {'voice_name': 'en-US-BrianNeural'},    # US English, professional male voice
                'female': {'voice_name': 'en-US-JennyNeural'}   # US English, professional female voice
            },
            'caller': {
                'male': {'voice_name': 'en-GB-RyanNeural'},     # UK English, professional male voice  
                'female': {'voice_name': 'en-GB-SoniaNeural'}   # UK English, professional female voice
            }
        }
    
    def _detect_gender_from_name(self, name: str) -> str:
        """Detect gender from a given name. Returns 'male' or 'female'."""
        d = gender.Detector()
        
        first_name = name.split()[0] if ' ' in name else name
        
        first_name = first_name.replace('Dr.', '').replace('Mr.', '').replace('Ms.', '').replace('Mrs.', '').strip()
        
        gender_result = d.get_gender(first_name)
        
        if gender_result in ['male', 'mostly_male']:
            return 'male'
        elif gender_result in ['female', 'mostly_female']:
            return 'female'
        else:
            return 'female'
    
    def generate_audio(self, transcript: str, audio_settings: Dict, audio_id: Optional[str] = None) -> Optional[Union[str, bytes]]:
        """Generate audio file from transcript. Returns file path if audio_id provided, otherwise bytes."""
        try:
            segments = self._parse_transcript(transcript)
            
            audio_segments = []
            
            for i, (speaker, text) in enumerate(segments):
                speaker_name = self._extract_name_from_speaker(speaker, transcript)
                voice_config = self._get_voice_config(speaker, speaker_name)
                
                
                segment_audio = self._text_to_speech(text, voice_config)
                
                if segment_audio:
                    segment_audio = self._apply_voice_characteristics(segment_audio, speaker)
                    audio_segments.append(segment_audio)
                    
                    if i < len(segments) - 1:
                        pause = AudioSegment.silent(duration=500)  # 0.5 second pause
                        audio_segments.append(pause)
            
            if not audio_segments:
                return None
            
            combined_audio = sum(audio_segments)
            
            final_audio = self._apply_audio_settings(combined_audio, audio_settings)
            
            if audio_id:
                return self._save_to_file(final_audio, audio_settings, audio_id)
            else:
                return self._to_wav_bytes(final_audio, audio_settings)
            
        except Exception as e:
            print(f"Error generating audio: {e}")
            return None
    
    def _parse_transcript(self, transcript: str) -> list:
        """Parse transcript into speaker segments."""
        segments = []
        lines = transcript.split('\n')
        
        for line in lines:
            line = line.strip()
            if ':' in line and line:
                parts = line.split(':', 1)
                if len(parts) == 2:
                    speaker = parts[0].strip()
                    text = parts[1].strip()
                    if text:  # Only add non-empty text
                        segments.append((speaker, text))
        
        return segments
    
    def _get_voice_config(self, speaker: str, speaker_name: Optional[str] = None) -> Dict:
        """Get voice configuration based on speaker type and name gender."""
        speaker_type = 'agent' if 'agent' in speaker.lower() else 'caller'
        
        if speaker_name:
            gender = self._detect_gender_from_name(speaker_name)
            return self.voice_settings[speaker_type][gender]
        else:
            return self.voice_settings[speaker_type]['female']
    
    def _extract_name_from_speaker(self, speaker: str, transcript_text: Optional[str] = None) -> str:
        """Extract the actual name from speaker label or transcript context."""
        if 'Agent' in speaker and transcript_text:
            import re
            agent_intro_pattern = r'this is (\w+)'
            match = re.search(agent_intro_pattern, transcript_text, re.IGNORECASE)
            if match:
                return match.group(1)
        
        if 'Agent' in speaker:
            parts = speaker.split()
            if len(parts) > 1:
                return ' '.join(parts[1:])  # Return everything after "Agent"
            else:
                return speaker  # Fallback to full speaker label
        else:
            name = speaker.replace('Dr.', '').replace('Mr.', '').replace('Ms.', '').replace('Mrs.', '').strip()
            return name if name else speaker
    
    def _apply_voice_characteristics(self, audio: AudioSegment, speaker: str) -> AudioSegment:
        """Apply voice characteristics to differentiate speakers."""
        if 'agent' in speaker.lower():
            audio = audio + 2  # Slightly increase volume
            audio = audio.speedup(playback_speed=1.05)  # Slightly faster, professional pace
        else:
            audio = audio - 1  # Slightly decrease volume
        
        return audio
    
    def _text_to_speech(self, text: str, voice_config: Dict) -> Optional[AudioSegment]:
        """Convert text to speech using Azure Speech SDK."""
        try:
            speech_config = speechsdk.SpeechConfig(
                subscription=os.environ.get('SPEECH_KEY'),
                region="westus3"
            )
            speech_config.speech_synthesis_voice_name = voice_config['voice_name']
            
            with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_file:
                temp_filename = temp_file.name
            
            audio_config = speechsdk.audio.AudioOutputConfig(filename=temp_filename)
            
            speech_synthesizer = speechsdk.SpeechSynthesizer(
                speech_config=speech_config, 
                audio_config=audio_config
            )
            
            speech_synthesis_result = speech_synthesizer.speak_text_async(text).get()
            
            if speech_synthesis_result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
                audio = AudioSegment.from_wav(temp_filename)
                os.unlink(temp_filename)
                return audio
            else:
                print(f"Speech synthesis failed: {speech_synthesis_result.reason}")
                if speech_synthesis_result.reason == speechsdk.ResultReason.Canceled:
                    cancellation_details = speech_synthesis_result.cancellation_details
                    print(f"Error details: {cancellation_details.error_details}")
                os.unlink(temp_filename)
                return None
                
        except Exception as e:
            print(f"Error in Azure text-to-speech: {e}")
            return None
    
    def _apply_audio_settings(self, audio: AudioSegment, settings: Dict) -> AudioSegment:
        """Apply audio settings to the combined audio."""
        
        target_sample_rate = settings.get('sampling_rate', 16000)
        audio = audio.set_frame_rate(target_sample_rate)
        
        target_channels = settings.get('channels', 1)
        if target_channels == 1:
            audio = audio.set_channels(1)  # Convert to mono
        else:
            audio = audio.set_channels(2)  # Convert to stereo
        
        audio = audio.normalize()
        
        return audio
    
    def _to_wav_bytes(self, audio: AudioSegment, settings: Dict) -> bytes:
        """Convert AudioSegment to WAV bytes."""
        
        wav_buffer = io.BytesIO()
        
        audio.export(
            wav_buffer,
            format="wav",
            parameters=[
                "-acodec", "pcm_s16le",  # 16-bit PCM
                "-ar", str(settings.get('sampling_rate', 16000)),  # Sample rate
                "-ac", str(settings.get('channels', 1))  # Channels
            ]
        )
        
        wav_buffer.seek(0)
        return wav_buffer.getvalue()
    
    def _save_to_file(self, audio: AudioSegment, settings: Dict, audio_id: str) -> str:
        """Save AudioSegment to WAV file and return file path."""
        import os
        
        audio_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'generated_audio')
        os.makedirs(audio_dir, exist_ok=True)
        
        file_path = os.path.join(audio_dir, f"{audio_id}.wav")
        
        audio.export(
            file_path,
            format="wav",
            parameters=[
                "-acodec", "pcm_s16le",  # 16-bit PCM
                "-ar", str(settings.get('sampling_rate', 16000)),  # Sample rate
                "-ac", str(settings.get('channels', 1))  # Channels
            ]
        )
        
        return file_path

    def simulate_phone_quality(self, audio: AudioSegment) -> AudioSegment:
        """Apply phone-like audio filtering."""
        
        
        audio = audio.low_pass_filter(3400)
        
        audio = audio.high_pass_filter(300)
        
        audio = audio.compress_dynamic_range()
        
        return audio
