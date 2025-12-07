import os
import json
import time
from azure.servicebus import ServiceBusClient

SERVICE_BUS_CONNECTION_STRING = os.getenv("SERVICE_BUS_CONNECTION_STRING")
QUEUE_NAME = os.getenv("SERVICE_BUS_QUEUE_NAME")


def process_message(queue_name: str, payload: dict):
    print(f"[PROCESSOR] Processing message from queue '{queue_name}'")
    print(f"[PROCESSOR] Payload: {payload}")

    # Simulate some processing work
    # print("[PROCESSOR] Simulating 2 minutes of processing...")
    # time.sleep(120)

    print("[PROCESSOR] Done!")
    return {
        "status": 200,
        "response": "success"
    }


def main():
    client = ServiceBusClient.from_connection_string(SERVICE_BUS_CONNECTION_STRING)
    receiver = client.get_queue_receiver(queue_name=QUEUE_NAME)

    print(f"Waiting for a message on: {QUEUE_NAME}")
    print(f"[MAIN] Using Service Bus connection string: {SERVICE_BUS_CONNECTION_STRING}")

    with receiver:
        messages = receiver.receive_messages(max_message_count=1, max_wait_time=10)
        print(f"[MAIN] Received {len(messages)} messages.")

        if not messages:
            print("No messages received.")
            time.sleep(60)
            print("Waited 60 seconds. Exiting now.")
            return

        msg = messages[0]

        # Decode message body exactly like your real app
        try:
            raw = b"".join(msg.body) if hasattr(msg, "body") else str(msg)
        except Exception:
            raw = str(msg)

        print("[MAIN] Simulating 3 minute of pre-processing...")
        time.sleep(180)
        print("[MAIN] Preprocessing completed...")
        receiver.complete_message(msg)
        print("[MAIN] Message completed (deleted) from Service Bus.")

        raw_text = raw.decode("utf-8") if isinstance(raw, (bytes, bytearray)) else raw

        print(f"[MAIN] Raw message body: {raw_text}")

        try:
            payload = json.loads(raw_text)
        except Exception:
            print("[MAIN] Failed to parse JSON payload")
            payload = {}
        result = process_message(QUEUE_NAME, payload)

    print(f"[MAIN] Processing result: {result}")
    print("Container exiting now (1 message processed).")


if __name__ == "__main__":
    main()
