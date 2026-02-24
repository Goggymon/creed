# CREED

CREED is a modular AI assistant backend built in Python with hybrid cloud reasoning and local neural voice synthesis.

It is designed as a scalable AI infrastructure capable of powering a GUI-based desktop or kiosk application.

CREED combines low-latency cloud intelligence with fully local speech generation for a responsive, production-grade assistant experience.

---

## Architecture

CREED consists of:

- **Engine Layer** – Core orchestration and streaming logic  
- **Cloud Reasoning Module** – Groq-powered LLM with token streaming  
- **Local Neural TTS Layer** – Piper-based real-time speech synthesis  
- **Modular Tool System** – Extensible capability modules (memory, system tools, etc.)  
- **FastAPI Backend** – REST API for GUI or external integration  
- **Versioned Development Workflow** – Semantic versioning + structured changelog  

---

## Technology Stack

- Python 3.10.11  
- Groq API (cloud LLM streaming)  
- Piper (local neural TTS)  
- FastAPI  
- Uvicorn  
- SoundDevice  
- NumPy  

CREED streams responses from the cloud LLM while synthesizing speech locally for minimal latency and improved responsiveness.

---

## Development Milestones

### v0.1.0 – Local Model Integration
- Ollama setup  
- Local model integration  
- CLI interaction  

### v0.2.0 – Stability Layer
- Timeout handling  
- Graceful failure logic  
- Safe module initialization  

### v0.3.0 – Backend Foundation
- FastAPI integration  
- `/chat` endpoint  
- Streaming response support  
- API documentation  

### v0.4.0 – Hybrid Intelligence + Neural Voice
- Migrated from Ollama to Groq cloud streaming  
- Implemented token-by-token streaming engine  
- Integrated local Piper neural TTS  
- Real-time speech interruption support  
- Clean streaming + speech synchronization  
- Secured environment configuration (`.env` isolation)  

---

## Current Capabilities

- Streaming cloud reasoning  
- Local neural speech synthesis  
- Interruptible voice output  
- CLI debug interface  
- REST API backend  
- Modular tool framework  
- Secure environment variable management  

---

## Current Limitations

- No GUI frontend (backend-first architecture)  
- No persistent memory database  
- No wake-word integration  
- No advanced tool execution layer  
- No speech-to-text input  

---

## Roadmap

- GUI shell with voice toggle + stop control  
- Persistent memory layer  
- Tool execution framework (system control, automation)  
- Wake word integration  
- Full API-first refactor for UI separation  

---

CREED is under active development and evolving toward a hybrid AI assistant platform.
