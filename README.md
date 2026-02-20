# CREED

CREED is a locally hosted, modular AI assistant system designed for full-stack personal deployment.  
It is built to operate entirely offline using local inference models, with long-term integration planned for embedded hardware such as the Raspberry Pi 4.

CREED is not a chatbot wrapper.  
It is an evolving AI infrastructure project focused on resilience, modularity, and performance control.

---

## Core Architecture

CREED currently operates using:

- Python 3.10.11
- Ollama (local inference engine)
- phi3 model (local LLM)
- REST API communication via localhost (port 11434)

The system communicates directly with the Ollama daemon and processes structured JSON responses.

---

## Development Phases

### Phase 1 — Core Model Integration (Completed)

- Installed and configured Ollama
- Installed phi3 model
- Verified local inference via terminal
- Implemented Python API client
- Confirmed localhost endpoint stability
- Resolved PATH configuration issues
- Understood daemon vs model lifecycle behavior

Outcome:
CREED successfully communicates with a locally hosted LLM.

---

### Phase 2 — Stability Layer (Completed)

- Implemented request timeout handling
- Added graceful failure responses
- Eliminated hanging behavior when service unavailable
- Improved generation response time
- Verified correct API path resolution
- Cleaned Python environment inconsistencies

Outcome:
CREED fails safely and responds reliably.

---

## Current Capabilities

- Local AI interaction via CLI
- Offline inference
- Service failure detection
- Fast generation under stable daemon state
- Modular Python-based architecture

---

## Current Limitations

- No GUI interface
- No persistent memory layer
- No voice input/output
- No camera integration
- Dependent on Ollama daemon health
- No auto-restart recovery logic

---

## Long-Term Roadmap

Phase 3 — Modular Code Refactor  
Phase 4 — Persistent Memory Layer  
Phase 5 — System Command Modules  
Phase 6 — Local Monitoring & Health Checks  
Phase 7 — Raspberry Pi Deployment Optimization  
Phase 8 — Voice Integration  
Phase 9 — Camera Integration  
Phase 10 — Real-Time Assistant Mode  

---

## Design Philosophy

CREED is built with the following principles:

- Fully local execution
- No cloud dependency
- Fail-safe behavior over silent crashes
- Controlled performance optimization
- Hardware-portable architecture
- Long-term maintainability

---

## Deployment Goal

Final deployment target:
Raspberry Pi 4 with optimized lightweight inference and real-time assistant capabilities.

CREED is intended to become a fully autonomous, always-available local AI assistant.
