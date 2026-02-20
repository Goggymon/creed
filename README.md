# CREED

CREED is a modular, fully local AI assistant backend built on Python and Ollama.

It is designed as a resilient, extensible AI infrastructure capable of powering a GUI kiosk system on embedded hardware such as the Raspberry Pi 4.

CREED operates entirely offline and exposes a REST API for interface integration.

---

## Architecture

CREED consists of:

- **Engine Layer** – Core orchestration logic
- **Dynamic Module System** – Auto-loaded capability modules
- **AI Module** – Local LLM integration via Ollama
- **FastAPI Backend** – REST interface for external clients
- **Versioned Development System** – Structured changelog + semantic tagging

---

## Technology Stack

- Python 3.10.11
- Ollama (local inference engine)
- phi3 model
- FastAPI
- Uvicorn
- Requests

CREED communicates with Ollama via JSON over `localhost:11434` and exposes its own API on `localhost:8000`.

---

## Development Milestones

### v0.1.0 – Core Model Integration
- Local Ollama setup
- Model integration
- Python API client
- Terminal-based interaction

### v0.2.0 – Stability Layer
- Timeout handling
- Graceful failure responses
- Contained network exceptions
- Safe module loader initialization

### v0.3.0 – Backend Foundation
- FastAPI integration
- `/chat` REST endpoint
- Automatic module loading on engine initialization
- Swagger API documentation
- Backend verified under service failure conditions

---

## Current Capabilities

- CLI interaction (debug mode)
- REST API backend
- Offline local inference
- Graceful Ollama failure handling
- Modular extension system
- Structured version control workflow

---

## Current Limitations

- No GUI frontend (backend-only)
- No persistent memory system
- No voice or camera integration
- No AI health monitoring endpoint
- Engine still partially CLI-oriented

---

## Next Phase

- Refactor engine to be API-first (return-based responses)
- Add structured request validation (Pydantic models)
- Implement AI health-check endpoint
- Prepare GUI frontend layer
- Optimize for Raspberry Pi deployment

---

CREED is under active development.
