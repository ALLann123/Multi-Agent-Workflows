#!/usr/bin/python3
import asyncio
import base64
import json
import websockets
import os
from dotenv import load_dotenv

# get our environment variables
load_dotenv()

# --- This function handles our connection to deepgram
def sts_connect():
    api_key = os.getenv("DEEPGRAM_API_KEY")
    # check if there is an API key in the .env file
    if not api_key:
        raise Exception("Missing DEEPGRAM_API_KEY")
    
    # we use websockets to connect to deepgram - Listen for a phone call
    sts_ws = websockets.connect(
        "wss://agent.deepgram.com/v1/agent/converse",
        # pass our token
        subprotocols=["token", api_key]
    )
    return sts_ws


# ---- Specify the voice we are using, and all the configurations our agent is using
def load_config():
    # we load our config.json file as a python dictionary
    with open("config.json", "r") as f:
        return json.load(f)
    

# allows user to interrupt the model when speaking
async def handle_barge_in(decoded, twilio_ws, streamsid):
    if decoded["type"] == "UserStartedSpeaking":
        clear_message = {
            "event": "clear",
            "streamSid": streamsid
        }
        await twilio_ws.send(json.dumps(clear_message))


# function calling
async def handle_text_message(decoded, twilio_ws, sts_ws, streamsid):
    await handle_barge_in(decoded, twilio_ws, streamsid)


# sending audio from our server via the web socket
async def sts_sender(sts_ws, audio_queue):
    print("sts_sender started")
    while True:
        # as soon as we have audio we send it to deepgram
        chunk = await audio_queue.get()
        await sts_ws.send(chunk)


# receiving from Deepgram message and send to twilio
async def sts_receiver(sts_ws, twilio_ws, streamsid_queue):
    print("sts_receiver started")
    streamsid = await streamsid_queue.get()

    # load the data from deepgram - Response can contain the response for twilio or function call
    async for message in sts_ws:
        if isinstance(message, str):
            decoded = json.loads(message)
            await handle_text_message(decoded, twilio_ws, sts_ws, streamsid)
            continue

        raw_mulaw = message
        
        # we want to take the voice input to send to Twilio as output
        media_message = {
            "event": "media",
            "streamSid": streamsid,
            "media": {"payload": base64.b64encode(raw_mulaw).decode("ascii")}
        }
        await twilio_ws.send(json.dumps(media_message))


# ----- function receives audio from Twilio
async def twilio_receiver(twilio_ws, audio_queue, streamsid_queue):
    # load in all the voice input from Twilio - Dealing with bytes
    BUFFER_SIZE = 20 * 160
    inbuffer = bytearray(b"")

    # connect to the web socket and loop through all the audio chunks being received
    async for message in twilio_ws:
        try:
            data = json.loads(message)
            event = data["event"]

            if event == "start":
                print("get our streamSid")
                start = data["start"]
                streamsid = start["streamSid"]
                streamsid_queue.put_nowait(streamsid)

            elif event == "connected":
                continue
            
            # we are getting the audio media which is in base64 and we try and decode it
            elif event == "media":
                media = data["media"]
                chunk = base64.b64decode(media["payload"])

                # did the user say this? if so add it to buffer
                if media.get("track") == "inbound":
                    inbuffer.extend(chunk)

            elif event == "stop":
                break

            while len(inbuffer) >= BUFFER_SIZE:
                chunk = inbuffer[:BUFFER_SIZE]
                audio_queue.put_nowait(chunk)
                inbuffer = inbuffer[BUFFER_SIZE:]

        except Exception as e:
            print("Error in twilio_receiver:", e)
            break


async def twilio_handler(twilio_ws):
    # we need to process the messages in a stream. Store all the audio we want to store
    audio_queue = asyncio.Queue()

    # we can have multiple people calling us on Twilio
    streamsid_queue = asyncio.Queue()

    # connect to deepgram
    async with sts_connect() as sts_ws:
        # configure
        config_message = load_config()
        
        # send the configurations loaded to deepgram
        await sts_ws.send(json.dumps(config_message))

        # three things we want to always be running: 1. Sender, 2. Receiver, 3. Twilio Receiver
        await asyncio.wait(
            [
                asyncio.ensure_future(sts_sender(sts_ws, audio_queue)),
                asyncio.ensure_future(sts_receiver(sts_ws, twilio_ws, streamsid_queue)),
                asyncio.ensure_future(twilio_receiver(twilio_ws, audio_queue, streamsid_queue)),
            ]
        )

        # we close the connection
        await twilio_ws.close()


# trigger everything - Ensure server is running constantly
async def main():
    async with websockets.serve(twilio_handler, host="localhost", port=5000):
        print("Started Server")
        await asyncio.Future()  # run forever


# call the main
if __name__ == "__main__":
    asyncio.run(main())
