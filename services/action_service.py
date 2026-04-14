def take_action(intent):
    actions = {
        "refund": "Refund initiated (simulated)",
        "late_delivery": "Checked delivery: delayed (simulated)",
        "wrong_item": "Replacement request created",
        "complaint": "Complaint escalated to support team",
        "general": "No action required"
    }

   return actions.get(intent, "Unable to process request at the moment")
