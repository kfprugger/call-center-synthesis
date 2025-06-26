# Contoso Call Center Synthetic Transcript and Audio Generator - Detailed PRD

## Executive Summary
A comprehensive Python-based application that generates synthetic medical call center conversations with corresponding high-quality audio files. The system simulates realistic interactions between call center agents and customers/patients for Contoso Medical, supporting multiple medical scenarios with configurable parameters.

## Architecture Overview

### Technology Stack
- **Backend**: FastAPI (Python 3.12+) with Poetry dependency management
- **Frontend**: React 18+ with TypeScript, Vite build system
- **UI Framework**: Tailwind CSS with shadcn/ui component library
- **Audio Processing**: Azure Cognitive Services Speech SDK with pydub
- **Data Generation**: Faker library for synthetic PHI/PII
- **Voice Selection**: gender-guesser library for name-based voice assignment

### System Architecture
```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   React Frontend │────│   FastAPI Backend │────│  Azure Speech   │
│   (Port 5173)   │    │   (Port 8000)    │    │    Services     │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌──────────────────┐
                       │  Local File      │
                       │  Storage         │
                       │  - /generated_   │
                       │    audio/        │
                       │  - /generated_   │
                       │    transcripts/  │
                       └──────────────────┘
```

## Functional Requirements

### Core Features

#### 1. Scenario Generation
**Three Medical Scenarios:**
1. **Healthcare Provider Inquiry**: Provider calling about past patient encounters
2. **Patient Visit Inquiry**: Patient calling about recent hospital/clinic visits  
3. **Caregiver Inquiry**: Caregiver calling with medical questions about patients

**Implementation Details:**
- Each scenario has unique conversation templates
- Realistic medical terminology and procedures
- Appropriate role-based dialogue patterns
- Configurable conversation flow and complexity

#### 2. Synthetic Data Generation
**PHI/PII Generation:**
- Patient names, addresses, phone numbers
- Medical record numbers, insurance IDs
- Diagnosis codes, medication names
- Hospital/clinic names and locations
- Provider names and credentials

**Compliance:**
- All data is synthetic and non-identifiable
- No real PHI/PII included
- Faker library with medical-specific providers
- Disclaimer text in all outputs

#### 3. Audio Generation System
**Azure Speech Integration:**
- **Endpoint**: `https://westus3.api.cognitive.microsoft.com/`
- **Authentication**: API key-based authentication
- **Voice Selection**: Gender-based voice assignment using name analysis

**Voice Configuration:**
```python
voice_settings = {
    'agent': {
        'male': {'voice_name': 'en-US-BrianNeural'},
        'female': {'voice_name': 'en-US-JennyNeural'}
    },
    'caller': {
        'male': {'voice_name': 'en-GB-RyanNeural'},
        'female': {'voice_name': 'en-GB-SoniaNeural'}
    }
}
```

**Audio Specifications:**
- **Format**: WAV (Microsoft PCM)
- **Bit Depth**: 16-bit
- **Sample Rates**: 8kHz, 16kHz, 32kHz, 48kHz (configurable)
- **Channels**: Mono (recommended) or Stereo
- **Bitrate**: 256 kbps (mono), 512 kbps (stereo)
- **Codec**: PCM

#### 4. Configuration Options
**Sentiment Control:**
- Positive: Satisfied, helpful interactions
- Neutral: Professional, matter-of-fact conversations
- Negative: Frustrated, complaint-based calls
- Mixed sentiment support within single conversations

**Duration Settings:**
- Short: 2-3 minutes
- Medium: 4-6 minutes  
- Long: 7-10 minutes

**Audio Settings Panel:**
- Sample rate selection dropdown
- Channel configuration (mono/stereo)
- Audio generation toggle
- Real-time audio preview

## Technical Implementation

### Backend Implementation (FastAPI)

#### Dependencies (pyproject.toml)
```toml
[tool.poetry.dependencies]
python = "^3.12"
fastapi = {extras = ["standard"], version = "^0.115.14"}
faker = "^37.4.0"
pydub = "^0.25.1"
numpy = "^2.3.1"
scipy = "^1.16.0"
azure-cognitiveservices-speech = "^1.41.1"
gender-guesser = "^0.4.0"
python-dotenv = "^1.0.1"
```

#### Core API Endpoints
```python
POST /generate-calls
GET /audio/{audio_id}
GET /transcript/{transcript_id}
GET /scenarios
GET /audio-settings
GET /stats
DELETE /cleanup/{session_id}
```

#### Key Services
1. **TranscriptGenerator**: Creates realistic conversation scripts
2. **AudioGenerator**: Converts text to speech with voice differentiation
3. **SyntheticDataGenerator**: Generates fake medical data
4. **DataModels**: Pydantic models for request/response validation

### Frontend Implementation (React + TypeScript)

#### Key Components
```typescript
// Main application component
App.tsx - Main application layout and state management

// UI Components (shadcn/ui)
- Button, Card, Checkbox, Select, Slider
- Dialog, Progress, Toast notifications
- Form components with validation
```

#### State Management
- React hooks for local state
- Form validation with real-time feedback
- Audio playback controls
- File download management

### File Management System

#### Directory Structure
```
/generated_audio/
├── contoso_call_YYYYMMDD_HHMMSS_call_1.wav
├── contoso_call_YYYYMMDD_HHMMSS_call_2.wav
└── ...

/generated_transcripts/
├── contoso_call_YYYYMMDD_HHMMSS_call_1.txt
├── contoso_call_YYYYMMDD_HHMMSS_call_2.txt
└── ...
```

#### File Naming Convention
- **Pattern**: `contoso_call_YYYYMMDD_HHMMSS_call_N.{wav|txt}`
- **Example**: `contoso_call_20250626_143022_call_1.wav`
- **Timestamp**: Current date/time when generation starts
- **Sequential**: Call number increments for batch generations

## User Interface Specifications

### Main Application Layout
```
┌─────────────────────────────────────────────────────────┐
│ Contoso Call Center Synthetic Transcript & Audio Gen   │
├─────────────────────────────────────────────────────────┤
│ ┌─────────────────┐ ┌─────────────────┐ ┌─────────────┐ │
│ │ Scenario        │ │ Sentiment       │ │ Duration    │ │
│ │ Selection       │ │ Configuration   │ │ Settings    │ │
│ │ ☑ Provider      │ │ ○ Positive      │ │ ○ Short     │ │
│ │ ☑ Patient       │ │ ○ Neutral       │ │ ● Medium    │ │
│ │ ☑ Caregiver     │ │ ● Negative      │ │ ○ Long      │ │
│ └─────────────────┘ └─────────────────┘ └─────────────┘ │
├─────────────────────────────────────────────────────────┤
│ ┌─────────────────────────────────────────────────────┐ │
│ │ Audio Settings                                      │ │
│ │ ☑ Generate Audio Files                             │ │
│ │ Sample Rate: [16kHz ▼] Channels: [Mono ▼]         │ │
│ └─────────────────────────────────────────────────────┘ │
├─────────────────────────────────────────────────────────┤
│ Number of Calls: [5] [Generate Calls]                  │
├─────────────────────────────────────────────────────────┤
│ ┌─────────────────────────────────────────────────────┐ │
│ │ Generated Results                                   │ │
│ │ Call 1: [📄 Transcript] [🔊 Audio] [⬇ Download]    │ │
│ │ Call 2: [📄 Transcript] [🔊 Audio] [⬇ Download]    │ │
│ └─────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────┘
```

### UI Component Requirements
- **Responsive Design**: Mobile and desktop compatibility
- **Accessibility**: WCAG 2.1 AA compliance
- **Loading States**: Progress indicators during generation
- **Error Handling**: User-friendly error messages
- **File Management**: Bulk download and individual file access

## Data Models and Validation

### Request Models
```python
class CallGenerationRequest(BaseModel):
    scenarios: List[ScenarioType]
    sentiment: SentimentType
    duration: DurationType
    num_calls: int = Field(ge=1, le=50)
    audio_settings: AudioSettings

class AudioSettings(BaseModel):
    generate_audio: bool = True
    sampling_rate: int = Field(default=16000)
    channels: int = Field(default=1, ge=1, le=2)
```

### Response Models
```python
class GeneratedCall(BaseModel):
    id: int
    scenario: str
    transcript_data: TranscriptData
    audio_file_url: Optional[str]
    transcript_file_url: str

class TranscriptData(BaseModel):
    scenario: str
    sentiment: str
    duration: str
    transcript: str
    participants: List[str]
    estimated_duration_minutes: int
```

## Environment Configuration

### Required Environment Variables
```bash
# Azure Speech Services
SPEECH_KEY=your_azure_speech_api_key
ENDPOINT=https://westus3.api.cognitive.microsoft.com/

# Optional Configuration
DEBUG=false
MAX_CALLS_PER_REQUEST=50
AUDIO_STORAGE_PATH=./generated_audio
TRANSCRIPT_STORAGE_PATH=./generated_transcripts
```

### Development Setup
```bash
# Backend Setup
cd contoso-call-center-backend
poetry install
poetry run uvicorn app.main:app --reload --port 8000

# Frontend Setup  
cd contoso-call-center-frontend
npm install
npm run dev
```

## Quality Assurance & Testing

### Testing Criteria
1. **Functional Testing**
   - All three scenarios generate appropriate content
   - Audio files match transcript content
   - Gender-based voice selection works correctly
   - File downloads function properly

2. **Audio Quality Testing**
   - Clear speech synthesis
   - Appropriate voice differentiation
   - Correct audio format specifications
   - No audio artifacts or distortion

3. **Data Validation Testing**
   - All generated data is synthetic
   - No real PHI/PII included
   - Realistic medical terminology usage
   - Proper conversation flow and context

4. **Performance Testing**
   - Generation time under 30 seconds for 5 calls
   - Concurrent request handling
   - File storage efficiency
   - Memory usage optimization

## Deployment Considerations

### Production Requirements
- **Server**: Linux-based environment with Python 3.12+
- **Storage**: Sufficient disk space for audio file generation
- **Network**: Reliable internet for Azure Speech API calls
- **Security**: API key management and secure file serving

### Scalability Considerations
- **Horizontal Scaling**: Multiple backend instances
- **File Storage**: Cloud storage integration (S3, Azure Blob)
- **Caching**: Redis for session management
- **Load Balancing**: Nginx or similar for request distribution

## Security & Compliance

### Data Protection
- No real PHI/PII storage or processing
- Synthetic data generation only
- Secure API key management
- File access controls

### Privacy Considerations
- Clear disclaimers about synthetic data
- No user data collection
- Temporary file cleanup options
- Audit logging for compliance

## Future Enhancements

### Potential Features
1. **Additional Scenarios**: Insurance claims, appointment scheduling
2. **Voice Customization**: Custom voice training options
3. **Multi-language Support**: Spanish, French language options
4. **Advanced Analytics**: Call quality metrics and reporting
5. **Integration APIs**: EMR system integration capabilities
6. **Batch Processing**: Large-scale generation workflows

This PRD provides comprehensive specifications for recreating the Contoso Call Center Synthetic Generator application with full feature parity and technical accuracy.
