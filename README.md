# 🎙️ LiveKit AI Voice Assistant

A real-time AI voice assistant built with **Python, LiveKit, Gradio, Deepgram, Google Gemma, Inworld TTS, and ai-coustics**.

The project provides a browser-based voice interface where users can join a LiveKit room, speak naturally through their microphone, and receive spoken responses from an AI agent.

---

## ✨ Features

- 🎙️ Real-time browser-based voice interaction
- ⚡ LiveKit real-time audio communication
- 🧠 Google Gemma language model
- 🎧 Deepgram Nova-3 speech-to-text
- 🔊 Inworld TTS with the **Ashley** voice
- 🎚️ ai-coustics audio enhancement/noise cancellation
- 🌐 Gradio web interface
- 🔐 Environment-based API credential management
- 🤖 Explicit LiveKit agent dispatch
- 🗣️ Automatic microphone activation after connection
- 🔄 Connect/disconnect session controls
- 👋 Automatic greeting when an agent session starts
- 🧩 Modular Python agent architecture

---

## 🏗️ Architecture

```text
┌──────────────────────────────┐
│        Browser / User        │
│      Gradio Web Interface    │
└──────────────┬───────────────┘
               │
               │ LiveKit WebRTC
               ▼
┌──────────────────────────────┐
│        LiveKit Cloud         │
│        Voice Room            │
└──────────────┬───────────────┘
               │
               │ Agent Dispatch
               ▼
┌──────────────────────────────┐
│       Python Voice Agent     │
│          my-agent            │
└──────────────┬───────────────┘
               │
       ┌───────┼────────┐
       ▼       ▼        ▼
   Deepgram  Gemma   Inworld
    STT       LLM      TTS
       │       │        │
       └───────┼────────┘
               ▼
        ai-coustics Audio
          Enhancement
               │
               ▼
        Spoken AI Response
```

---

## 🔄 How It Works

1. The user opens the Gradio web interface.
2. A LiveKit room name is entered.
3. The application creates a LiveKit participant token.
4. The application explicitly dispatches the `my-agent` agent to the selected room.
5. The browser connects to LiveKit using the generated token.
6. Microphone access is enabled.
7. User speech is transmitted through LiveKit.
8. ai-coustics provides audio enhancement/noise cancellation.
9. Deepgram Nova-3 converts speech to text.
10. Google Gemma generates the AI response.
11. Inworld TTS converts the response into speech.
12. The browser receives and plays the generated audio through LiveKit.

---

## 🧰 Technology Stack

| Technology | Purpose |
|---|---|
| Python 3.13+ | Application and agent runtime |
| LiveKit | Real-time voice communication and agent infrastructure |
| LiveKit Agents | Voice-agent session management |
| Gradio | Browser-based user interface |
| Deepgram Nova-3 | Speech-to-text |
| Google Gemma | Large language model |
| Inworld TTS | Text-to-speech |
| ai-coustics | Audio enhancement / noise cancellation |
| python-dotenv | Environment variable management |
| uv | Python environment and dependency management |

---

## 📁 Project Structure

```text
voiceagent/
│
├── ui.py
│   └── Gradio web interface and LiveKit browser connection
│
├── voiceagent.py
│   └── LiveKit AI voice-agent implementation
│
├── pyproject.toml
│   └── Project metadata and Python dependencies
│
├── uv.lock
│   └── Locked dependency versions
│
├── .python-version
│   └── Python version configuration
│
├── src/
│   └── voiceagent/
│       └── __init__.py
│
├── .env
│   └── Local API credentials (DO NOT COMMIT)
│
└── README.md
    └── Project documentation
```

---

## ⚙️ Requirements

Before running the project, install:

- Python **3.13 or newer**
- `uv`
- A LiveKit Cloud project
- LiveKit API credentials
- Access to the configured AI inference providers/models

The project currently requires:

```toml
gradio>=6.28.0
livekit-agents>=1.8.2
livekit-plugins-ai-coustics>=0.3.2
python-dotenv>=1.2.3
```

---

## 🚀 Installation

### 1. Clone the repository

```bash
git clone https://github.com/NoorUlHudaQureshi/livekit-ai-voice-agent.git
cd livekit-ai-voice-agent
```

### 2. Create the environment

If you use `uv`, the project can be prepared with:

```bash
uv sync
```

Activate the virtual environment if needed:

**Windows CMD:**

```cmd
.venv\Scripts\activate
```

---

## 🔐 Environment Variables

Create a local `.env` file in the project root.

```env
LIVEKIT_URL=your_livekit_url
LIVEKIT_API_KEY=your_livekit_api_key
LIVEKIT_API_SECRET=your_livekit_api_secret
```

### Security

**Never commit `.env` to GitHub.**

API keys and secrets should remain local or be stored using your deployment platform's secret-management system.

A safe repository can contain a `.env.example` file with placeholder values, but never real credentials.

---

## ▶️ Running the Project

The project uses two processes:

- **Terminal 1:** Gradio web interface
- **Terminal 2:** LiveKit voice agent

### Terminal 1 — Start the Web UI

```bash
uv run python ui.py
```

The Gradio interface will normally be available at:

```text
http://127.0.0.1:7860
```

Open that address in your browser.

### Terminal 2 — Start the Voice Agent

Open a second terminal in the project directory:

```bash
uv run python voiceagent.py dev
```

The LiveKit agent will register and wait for a session.

> Depending on your installed LiveKit CLI version, you may see a notice that `dev` is deprecated in favor of `lk agent dev`. This is a CLI notice and does not change the application architecture.

---

## 🎙️ Using the Assistant

1. Start the Gradio UI.
2. Start the LiveKit agent.
3. Open the Gradio URL in your browser.
4. Enter a LiveKit room name, or use the default:
   `voice-agent-room`
5. Click **Connect & Start Talking**.
6. Allow microphone access.
7. Wait for the status to show:
   `Connected — listening`
8. Speak naturally.
9. Listen to the AI-generated response.
10. Click **Disconnect** when finished.

---

## 🤖 Agent Configuration

The LiveKit agent is registered with the name:

```text
my-agent
```

The assistant uses the following voice pipeline:

```text
Deepgram Nova-3
        ↓
   Google Gemma
        ↓
   Inworld TTS
```

The configured models are:

```text
STT: deepgram/nova-3
Language: multi

LLM: google/gemma-4-31b-it

TTS: inworld/inworld-tts-2
Voice: Ashley
```

The agent also uses LiveKit turn detection to determine when the user has finished speaking.

---

## 🔊 Audio Enhancement

The project integrates ai-coustics audio enhancement through LiveKit's audio input configuration.

The configured enhancer is:

```text
EnhancerModel.QUAIL_VF_S
```

This processing is applied to incoming audio before it enters the voice-agent pipeline.

---

## 🌐 Browser / LiveKit Integration

The Gradio interface dynamically loads the LiveKit JavaScript client:

```text
livekit-client@2.15.3
```

The browser:

- Creates a LiveKit room
- Connects using the server-generated token
- Enables the local microphone
- Listens for subscribed audio tracks
- Attaches remote audio to the page
- Updates the UI connection status
- Disconnects the room when requested

The application keeps LiveKit credentials on the server side. The browser receives a short-lived participant token generated by the Python application.

---

## 🔐 Authentication and Agent Dispatch

When a user starts a session, `ui.py`:

1. Validates the LiveKit configuration.
2. Creates a LiveKit agent dispatch for `my-agent`.
3. Creates a browser participant token with room-specific permissions.
4. Returns the LiveKit URL and token to the Gradio frontend.
5. The browser connects to the assigned room.

This explicit dispatch mechanism ensures that the named LiveKit agent is assigned to the requested room.

---

## 🧪 Development

For development, run the two components separately:

```bash
# Terminal 1
uv run python ui.py
```

```bash
# Terminal 2
uv run python voiceagent.py dev
```

Useful agent logs include:

```text
>>> AGENT SESSION STARTED
>>> ROOM: ...
>>> STARTING AGENT SESSION
>>> AGENT SESSION CONNECTED
```

The UI also reports connection states such as:

```text
Ready
Loading LiveKit...
Connecting...
Connected — listening
Disconnected
Connection failed
```

---

## 🛠️ Troubleshooting

### Agent connects but does not respond

Check that:

- `voiceagent.py` is running.
- The agent is registered as `my-agent`.
- The Gradio UI successfully dispatches `my-agent`.
- `LIVEKIT_URL`, `LIVEKIT_API_KEY`, and `LIVEKIT_API_SECRET` are configured.
- Your browser has microphone permission.
- The selected LiveKit room is correct.

### Microphone does not work

Check:

- Browser microphone permissions.
- Operating-system microphone permissions.
- Browser console errors.
- Whether another application is using the microphone.

### LiveKit connection fails

Verify:

```text
LIVEKIT_URL
LIVEKIT_API_KEY
LIVEKIT_API_SECRET
```

Also confirm that the LiveKit project is active and that the credentials belong to the same LiveKit environment.

### AI response is not generated

Check the agent terminal for errors and verify that the configured inference models and provider access are available.

---

## 🔒 Security Best Practices

Never commit:

```text
.env
API keys
API secrets
Access tokens
Private credentials
Provider secrets
```

Use environment variables for credentials:

```python
load_dotenv(".env")
```

and:

```python
os.getenv("LIVEKIT_API_KEY")
os.getenv("LIVEKIT_API_SECRET")
```

For production deployments, use your hosting provider's secret-management system instead of storing credentials in source code.

---

## 🚧 Future Improvements

Potential improvements include:

- Persistent conversation history
- Custom system prompts through the UI
- Multiple voice choices
- User authentication
- Conversation transcripts
- Usage and latency monitoring
- Production deployment
- Better error reporting
- Session analytics
- Configurable AI models
- Voice activity visualization
- Mobile-friendly interface
- Automated testing and CI/CD

---

## 📌 Project Status

This project is a working real-time AI voice assistant prototype using LiveKit and a browser-based Gradio interface.

It is suitable as a foundation for experimenting with:

- Real-time conversational AI
- Voice agents
- WebRTC audio
- AI inference pipelines
- Speech-to-text and text-to-speech systems
- LiveKit agent workflows

---

## 👤 Author

**Noor Ul Huda Qureshi**

GitHub:

https://github.com/NoorUlHudaQureshi

Project:

https://github.com/NoorUlHudaQureshi/livekit-ai-voice-agent

---

## 📄 License

Add your preferred open-source license to the repository, such as MIT, before publishing the project for reuse.

---

## ⭐ Contributing

Contributions, ideas, and improvements are welcome.

A typical contribution workflow:

```bash
git checkout -b feature/your-feature
git add .
git commit -m "Add your feature"
git push origin feature/your-feature
```

Then open a pull request on GitHub.

---

## ❤️ Acknowledgements

Built using the LiveKit real-time communications and agent ecosystem, with Deepgram speech recognition, Google Gemma language modeling, Inworld speech synthesis, ai-coustics audio enhancement, and Gradio for the web interface.
