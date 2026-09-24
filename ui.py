import os
import gradio as gr
from dotenv import load_dotenv
from livekit import api

load_dotenv(".env")

LIVEKIT_URL = os.getenv("LIVEKIT_URL")
LIVEKIT_API_KEY = os.getenv("LIVEKIT_API_KEY")
LIVEKIT_API_SECRET = os.getenv("LIVEKIT_API_SECRET")

AGENT_NAME = "my-agent"


def generate_token(
    room_name: str,
    participant_name: str = "gradio-user",
) -> str:

    if not LIVEKIT_API_KEY or not LIVEKIT_API_SECRET:
        raise RuntimeError(
            "LiveKit API credentials are missing from .env"
        )

    token = (
        api.AccessToken(
            LIVEKIT_API_KEY,
            LIVEKIT_API_SECRET,
        )
        .with_identity(participant_name)
        .with_name(participant_name)
        .with_grants(
            api.VideoGrants(
                room_join=True,
                room=room_name,
                can_publish=True,
                can_subscribe=True,
            )
        )
    )

    return token.to_jwt()


async def create_session(room_name: str):

    room_name = room_name.strip()

    if not room_name:
        return "", "", "Please enter a room name."

    if not LIVEKIT_URL:
        return "", "", "LIVEKIT_URL is missing from .env"

    if not LIVEKIT_API_KEY or not LIVEKIT_API_SECRET:
        return "", "", "LiveKit API credentials are missing from .env"

    try:
        print(f">>> DISPATCHING {AGENT_NAME} TO ROOM: {room_name}")

        # Explicitly dispatch the named agent to this room.
        async with api.LiveKitAPI(
            url=LIVEKIT_URL,
            api_key=LIVEKIT_API_KEY,
            api_secret=LIVEKIT_API_SECRET,
        ) as lkapi:

            dispatch = await lkapi.agent_dispatch.create_dispatch(
                api.CreateAgentDispatchRequest(
                    agent_name=AGENT_NAME,
                    room=room_name,
                )
            )

        print(
            f">>> DISPATCH CREATED: {AGENT_NAME} -> {room_name}"
        )
        print(f">>> DISPATCH ID: {dispatch.id}")

        # Create the browser participant token.
        token = generate_token(room_name)

        return (
            token,
            LIVEKIT_URL,
            f"Ready to join: {room_name}",
        )

    except Exception as e:
        print(f">>> DISPATCH ERROR: {e}")
        return "", "", f"Error: {e}"


def clear_session():
    return "", "", "Disconnected"


CUSTOM_HTML = """
<div class="voice-card">

    <div class="orb">
        <div class="orb-inner"></div>
    </div>

    <h2>AI Voice Assistant</h2>

    <p class="subtitle">
        Connect to your LiveKit voice agent and start talking.
    </p>

    <div class="status-pill">
        <span class="status-dot"></span>
        <span id="lk-status">Ready</span>
    </div>

    <div id="lk-audio"></div>

</div>

<style>

.voice-card {
    padding: 35px 25px;
    text-align: center;
    border-radius: 24px;
    border: 1px solid rgba(128,128,128,.25);
    min-height: 330px;
}

.orb {
    width: 110px;
    height: 110px;
    margin: 10px auto 25px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    background: radial-gradient(circle, #8b5cf6, #4f46e5);
    box-shadow: 0 0 45px rgba(99,102,241,.35);
}

.orb-inner {
    width: 65px;
    height: 65px;
    border-radius: 50%;
    background: rgba(255,255,255,.18);
    backdrop-filter: blur(8px);
}

.voice-card h2 {
    margin-bottom: 8px;
}

.subtitle {
    opacity: .7;
    margin-bottom: 20px;
}

.status-pill {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 8px 14px;
    border-radius: 999px;
    background: rgba(128,128,128,.12);
}

.status-dot {
    width: 9px;
    height: 9px;
    border-radius: 50%;
    background: #22c55e;
}

</style>
"""


with gr.Blocks(
    title="LiveKit AI Voice Assistant",
    theme=gr.themes.Soft(),
) as demo:

    gr.Markdown(
        """
        # 🎙️ LiveKit AI Voice Assistant
        ### Talk naturally with your AI voice agent
        """
    )

    with gr.Row():

        with gr.Column(scale=2):

            voice_ui = gr.HTML(CUSTOM_HTML)

            with gr.Row():

                room_name = gr.Textbox(
                    label="Room Name",
                    value="voice-agent-room",
                    placeholder="Enter a LiveKit room name",
                )

            with gr.Row():

                join_button = gr.Button(
                    "🎙️ Connect & Start Talking",
                    variant="primary",
                )

                leave_button = gr.Button(
                    "Disconnect",
                    variant="secondary",
                )

            status = gr.Textbox(
                label="Session Status",
                value="Disconnected",
                interactive=False,
            )

        with gr.Column(scale=1):

            gr.Markdown("### Session")

            gr.Markdown(
                """
                **Agent:** `my-agent`

                **Speech recognition:** Deepgram Nova-3

                **AI model:** Google Gemma

                **Voice:** Ashley

                **Audio enhancement:** ai-coustics
                """
            )

            gr.Markdown(
                """
                ### How it works

                1. Connect to a LiveKit room.
                2. Allow microphone access.
                3. Your voice is sent to the AI agent.
                4. The agent responds using speech.
                """
            )

    token_box = gr.Textbox(visible=False)
    url_box = gr.Textbox(visible=False)

    # CONNECT
    join_button.click(
        fn=create_session,
        inputs=room_name,
        outputs=[
            token_box,
            url_box,
            status,
        ],
    ).then(
        fn=None,
        inputs=[
            token_box,
            url_box,
        ],
        outputs=[],
        js="""
        (token, url) => {

            window.postMessage(
                {
                    type: "livekit-connect",
                    token: token,
                    url: url
                },
                "*"
            );

        }
        """,
    )

    # DISCONNECT
    leave_button.click(
        fn=clear_session,
        outputs=[
            token_box,
            url_box,
            status,
        ],
    ).then(
        fn=None,
        js="""
        () => {

            window.postMessage(
                {
                    type: "livekit-disconnect"
                },
                "*"
            );

        }
        """,
    )


if __name__ == "__main__":

    demo.launch(
        js="""

        () => {

            let livekitRoom = null;


            function setLiveKitStatus(message) {

                const status =
                    document.getElementById("lk-status");

                if (status) {
                    status.textContent = message;
                }

            }


            async function loadLiveKit() {

                if (window.LivekitClient) {
                    return;
                }

                await new Promise((resolve, reject) => {

                    const script =
                        document.createElement("script");

                    script.src =
                        "https://cdn.jsdelivr.net/npm/livekit-client@2.15.3/dist/livekit-client.umd.min.js";

                    script.onload = resolve;
                    script.onerror = reject;

                    document.head.appendChild(script);

                });

            }


            async function connectLiveKit(url, token) {

                try {

                    setLiveKitStatus(
                        "Loading LiveKit..."
                    );

                    await loadLiveKit();

                    setLiveKitStatus(
                        "Connecting..."
                    );


                    livekitRoom =
                        new LivekitClient.Room();


                    livekitRoom.on(
                        LivekitClient.RoomEvent.TrackSubscribed,
                        (track) => {

                            if (track.kind === "audio") {

                                const element =
                                    track.attach();

                                element.autoplay = true;

                                const audioContainer =
                                    document.getElementById(
                                        "lk-audio"
                                    );

                                if (audioContainer) {

                                    audioContainer.appendChild(
                                        element
                                    );

                                }

                            }

                        }
                    );


                    livekitRoom.on(
                        LivekitClient.RoomEvent.Disconnected,
                        () => {

                            setLiveKitStatus(
                                "Disconnected"
                            );

                        }
                    );


                    await livekitRoom.connect(
                        url,
                        token
                    );


                    await livekitRoom
                        .localParticipant
                        .setMicrophoneEnabled(true);


                    setLiveKitStatus(
                        "Connected — listening"
                    );

                    console.log(
                        "LiveKit connected successfully"
                    );

                    console.log(
                        "Microphone enabled"
                    );

                } catch (error) {

                    console.error(
                        "LiveKit connection error:",
                        error
                    );

                    setLiveKitStatus(
                        "Connection failed"
                    );

                }

            }


            async function disconnectLiveKit() {

                if (livekitRoom) {

                    await livekitRoom.disconnect();

                    livekitRoom = null;

                }

                setLiveKitStatus(
                    "Disconnected"
                );

            }


            window.addEventListener(
                "message",
                (event) => {

                    if (
                        !event.data ||
                        typeof event.data !== "object"
                    ) {
                        return;
                    }


                    if (
                        event.data.type ===
                        "livekit-connect"
                    ) {

                        connectLiveKit(
                            event.data.url,
                            event.data.token
                        );

                    }


                    if (
                        event.data.type ===
                        "livekit-disconnect"
                    ) {

                        disconnectLiveKit();

                    }

                }
            );

        }

        """
    )