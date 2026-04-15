import json

def load_orders():
    with open("data/orders.json", "r") as f:
        return json.load(f)

def extract_order_id(user_input):
    words = user_input.split()
    for w in words:
        if w.isdigit():
            return w
    return None

def check_delivery(user_input):
    orders = load_orders()
    order_id = extract_order_id(user_input)

    for order in orders:
        if order["order_id"] == order_id:
            return f"Order {order_id} is currently {order['status']}."

    return "Order not found."

def take_action(intent, user_input):
    if intent == "late_delivery":
        return check_delivery(user_input)
    elif intent == "refund":
        return "Refund request has been created."
    elif intent == "wrong_item":
        return "Replacement request has been created."
    elif intent == "complaint":
        return "Complaint has been escalated."
    else:
        return "No action required."
