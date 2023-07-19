import os
from dotenv import load_dotenv
from slack_sdk.rtm_v2 import RTMClient

load_dotenv()

bot_token = os.getenv("BOT_TOKEN")

rtm = RTMClient(token=bot_token)


@rtm.on("message")
def handle(client: RTMClient, event: dict):
    if "Hello" in event["text"]:
        channel_id = event["channel"]
        thread_ts = event["ts"]
        user = event[
            "user"
        ]  # This is not username but user ID (the format is either U*** or W***)

        client.web_client.chat_postMessage(
            channel=channel_id, text=f"Hi <@{user}>!", thread_ts=thread_ts
        )


# rtm.connect()
rtm.start()
