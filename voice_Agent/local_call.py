import time
import os
import threading
from dotenv import load_dotenv
from deepgram import (
    DeepgramClient,
    DeepgramClientOptions,
    AgentWebSocketEvents,
    AgentKeepAlive,
)
from deepgram.clients.agent.v1.websocket.options import SettingsOptions

load_dotenv()

def main():
    try:
        # 1. Get API key from environment
        api_key = os.getenv("DEEPGRAM_API_KEY")
        if not api_key:
            raise ValueError("DEEPGRAM_API_KEY environment variable is not set")
        print("API Key found.")

        # 2. Initialize Deepgram client
        config = DeepgramClientOptions(options={"keepalive": "true"})
        deepgram = DeepgramClient(api_key, config)
        connection = deepgram.agent.websocket.v("1")
        print("Created WebSocket connection...")

        # 3. Configure the Agent
        options = SettingsOptions()
        options.audio.input.encoding = "linear16"
        options.audio.input.sample_rate = 24000
        options.audio.output.encoding = "linear16"
        options.audio.output.sample_rate = 24000
        options.audio.output.container = "wav"
        options.agent.language = "en"
        options.agent.listen.provider.type = "deepgram"
        options.agent.listen.provider.model = "nova-3"
        options.agent.think.provider.type = "open_ai"
        options.agent.think.provider.model = "gpt-4o-mini"
        options.agent.think.prompt = "You are a friendly AI assistant."
        options.agent.speak.provider.type = "deepgram"
        options.agent.speak.provider.model = "aura-2-thalia-en"
        options.agent.greeting = "Hello! How can I help you today?"

        # 4. Send keep-alive messages in a separate thread
        def send_keep_alive():
            while True:
                time.sleep(5)
                print("Keep alive!")
                connection.send(str(AgentKeepAlive()))

        keep_alive_thread = threading.Thread(target=send_keep_alive, daemon=True)
        keep_alive_thread.start()

        # 5. Set up event handlers
        def on_audio_data(self, data, **kwargs):
            print(f"Received audio data: {len(data)} bytes")

        def on_agent_audio_done(self, agent_audio_done, **kwargs):
            print("Agent audio done.")

        def on_conversation_text(self, conversation_text, **kwargs):
            print(f"Conversation Text: {conversation_text}")

        connection.on(AgentWebSocketEvents.AudioData, on_audio_data)
        connection.on(AgentWebSocketEvents.AgentAudioDone, on_agent_audio_done)
        connection.on(AgentWebSocketEvents.ConversationText, on_conversation_text)

        # 6. Start the agent
        connection.start(options)

        # 7. Keep the main thread alive
        input("Press Enter to exit...\n")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()