# AGENTS.md — VoiceClaw (openclaw-voice-control)

Browser-based voice interface for OpenClaw agents. Self-hosted, open-source.

## Architecture

```
Browser (mic/speaker) ←→ WebSocket ←→ Voice Server
                                        ├── Whisper STT (local)
                                        ├── AI Backend (OpenClaw gateway or OpenAI)
                                        ├── ElevenLabs TTS (cloud) / Chatterbox (local)
                                        └── Silero VAD
```

## Key Files

| File | Purpose |
|------|---------|
| `src/server/main.py` | FastAPI server, WebSocket handler, lifespan |
| `src/server/stt.py` | Speech-to-Text (faster-whisper or openai-whisper) |
| `src/server/tts.py` | Text-to-Speech (ElevenLabs → Chatterbox → XTTS → mock) |
| `src/server/backend.py` | AI backend (OpenClaw gateway or direct OpenAI) |
| `src/server/vad.py` | Voice Activity Detection (Silero) |
| `src/server/audio_processing.py` | Audio preprocessing (HPF, noise reduction, normalize) |
| `src/server/text_utils.py` | Clean AI text for TTS (strip markdown, URLs, etc.) |
| `src/server/auth.py` | API key management and rate limiting |
| `src/client/index.html` | Browser UI (AudioWorklet, WebSocket client) |
| `src/client/audio-processor.js` | AudioWorklet processor for mic capture |

## Deployment Modes

1. **OpenClaw Gateway** (recommended): Set `OPENCLAW_GATEWAY_URL` + `OPENCLAW_GATEWAY_TOKEN` in `.env`. Voice sessions route through the full agent with memory, tools, persona.
2. **Direct OpenAI**: Set `OPENAI_API_KEY`. Standalone, no agent features.
3. **Docker**: `docker-compose up` for GPU-accelerated deployment.

## Platform Notes

- **Linux/CUDA**: `OPENCLAW_STT_DEVICE=cuda` for GPU-accelerated Whisper
- **Mac Studio (Apple Silicon)**: `OPENCLAW_STT_DEVICE=cpu` — faster-whisper doesn't support MPS. VAD and local TTS still use MPS via torch.
- **HTTPS required for mobile mic**: Use Tailscale Serve or nginx + Let's Encrypt

## Running

```bash
cp .env.example .env   # configure keys
uv sync                # or pip install -r requirements.txt
PYTHONPATH=. python -m src.server.main
# → http://localhost:8765
```

## Tests

```bash
pytest tests/
```
