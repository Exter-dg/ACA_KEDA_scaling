# ACA KEDA Scaling Test

This repository demonstrates Azure Container Apps (ACA) scaling behavior using KEDA, focusing on how containers handle message processing and scale-down events.

## Purpose
The goal is to observe whether ACA waits for a message to finish processing before scaling down, or if it terminates the container after the cooldown period, even if processing is still ongoing.

## Files
- `app.py`: Main application logic for receiving and processing Service Bus messages.
- `Dockerfile`: Container image definition for deployment.
- `requirements.txt`: Python dependencies.

## Scenario: Main Thread Processing (No Background Worker)
- **Setup:**
  - A single message is sent to an Azure Service Bus queue.
  - The container app receives and processes the message on the main thread (no background worker).
  - Processing simulates a long-running task (6 minutes).
  - KEDA is configured with a cooldown period of 3 minutes.

- **Test:**
  - Observe if the container app scales down after 3 minutes (cooldown) or waits for the 6-minute processing to complete.


## Observations

