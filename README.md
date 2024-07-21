# SimpliVisor: Hypervisor for MLOps

Note: This is still WORK IN PROGRESS

## Architecture 
1. Sever:
    - Server.py contains all the logic for serving APP server written in Flask 

2. Scheduler:
    - Scheduler.py is continous loop, to read deployment queue and schedule deployment

- When deployment is schduled following flow is followed
    1. PSQL table for deployment entry
    2. Same Deployment entry is added to scheduling queue in redis respective organization and cluster combination 
    3. scheduler reads from redis queue and tries to schedule deployment based on priority based scheduler logic


## Scheduler Logic
- Initializes high and low priority Redis queue keys based on the organization and cluster IDs.
- Continues processing as long as there are items in either the high or low priority queues.
- High Priority Processing:
    - If the high priority queue has items, it pops the highest priority deployment.
- Low Priority Processing:
    - If the high priority queue is empty, it processes items from the low priority queue.
- Deployment Validation:
    - Checks if the deployment's requested resources (memory and CPU) can be satisfied with the available resources.
    - If resources are sufficient, the deployment is updated to a running status, and available resources are adjusted accordingly.
- Aging and Priority Adjustment:
    - If resources are insufficient, the deployment's priority is adjusted for aging:
    - If the priority is greater than 1, it is decreased.   
    - If the priority is 1 or lower, the wait time is increased, and if it exceeds the threshold, the priority is increased.
    - The deployment is re-added to the appropriate queue based on the adjusted priority. 