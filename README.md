# ACA KEDA Scaling Test

This repository demonstrates Azure Container Apps (ACA) scaling behavior using KEDA, focusing on how containers handle message processing and scale-down events.

## Purpose
The goal is to observe whether ACA waits for a message to finish processing before scaling down, or if it terminates the container after the cooldown period, even if processing is still ongoing.

## Files
- `app.py`: Main application logic for receiving and processing Service Bus messages.
- `Dockerfile`: Container image definition for deployment.
- `requirements.txt`: Python dependencies.

## Scenario 1: Main Thread Processing (No Background Worker, 3 min Cooldown)
- **Setup:**
  - A single message is sent to an Azure Service Bus queue.
  - The container app receives and processes the message on the main thread (no background worker).
  - Processing simulates a long-running task (6 minutes).
  - KEDA is configured with a cooldown period of 3 minutes.

- **Test:**
  - Observe if the container app scales down after 3 minutes (cooldown) or waits for the 6-minute processing to complete.

- **Observations:**
  - ![alt text](image.png)

  - Container scales down after 3 minutes and doesn't wait for the processing to finish. KEDA scales down the container after the cooldown period.
  - Whenever container app was scaled using KEDA, no console logs were visible in log analytics. If manually scaled (hence 0 message workflow), logs were visible. It is possible that if container doesn't complete successfully (because KEDA scales it down after 3 minutes), no console logs are stored.

## Scenario 2: Long Processing (6 min) with Extended Cooldown (8 min)
- **Setup:**
  - A single message is sent to the queue.
  - The container app processes the message for 6 minutes on the main thread.
  - KEDA is configured with a cooldown period of 8 minutes (longer than the processing time).

- **Test:**
  - Observe if the container app remains active for the full 6 minutes, allowing processing and log output to complete before scale-down.
  - This scenario helps determine if missing console logs in log analytics are due to premature scale-down (before processing/logging finishes) or another issue.

- **Observations:**
  - ![alt text](image-2.png)
  - If replica is running and the container has completed its processing. Container will keep restarting and again execute till the replica stops (cooldown period). This is why we see multiple container start system messages while a replica is running.
  - If the cooldown period is longer than the processing time (8 min cooldown, 6 min processing), the container finishes processing and logs console output before scale-down. This helps confirm log loss is due to premature termination.
