##  Research & Understanding – CLI Agent to Customer Support Agent

## 1. Objective

The goal is to evolve the existing CLI agent into an agentic system capable of:
1. Understanding customer queries
2. Classifying intent
3. Taking actions based on the intent

This moves the system from a passive chatbot to an action-oriented agent.



## 2. Understanding the Existing CLI Agent

The original CLI agent follows this flow:

User Input → LLM → Response → Output

Key observations:
The agent maintains conversation history
Uses LM Studio as a local LLM backend
Handles multi-turn conversations
All logic was initially present in a single file

Limitations:
No intent understanding
No decision-making layer
No action execution
Purely conversational



## 3. Transition to Agentic Architecture

To make the system agentic, the following layers are required:

### 1. Intent Layer
Responsible for understanding *what the user wants*

Example:
"my order is late" - late_delivery



### 2. Action Layer
Responsible for deciding "what to do"

Example:
late_delivery - check delivery status



### 3. Execution Layer
Responsible for performing the action

(Currently simulated using predefined responses)


### 4. Response Layer
Communicates results back to the user


## 4. Microservice-style Refactoring

The system was restructured into modules:

`chat_service.py` → handles LLM interaction  
`intent_service.py` → classifies user queries  
`action_service.py` → determines system actions  
`model_service.py` → handles model fetching  
`ui_service.py` → CLI formatting  
`main.py` → orchestrates the flow  

Key understanding:
Each service has a single responsibility  
`main.py` acts as the coordinator  
Logic is decoupled and reusable  


## 5. Key Learnings

### 1. Separation of Concerns
Breaking a system into smaller modules improves clarity and maintainability.

### 2. Agent vs Chatbot
Chatbot → responds  
Agent → understands, decides, and acts  

### 3. Local LLM Integration
LM Studio exposes an OpenAI-compatible API which allows local inference.

### 4. Prompt Sensitivity
Intent classification depends heavily on prompt clarity and constraints.


## 6. Challenges Faced

Understanding how to split logic into services  
Handling inconsistent intent classification  
Avoiding over-engineering (unnecessary classes)  
Transitioning from linear script to modular architecture  


## 7. Current Capability

At this stage, the system can:
Accept user queries  
Classify intent  
Simulate actions  
Generate responses using LLM  


## 8. Next Steps

Improve intent classification reliability  
Replace simulated actions with real integrations (APIs)  
Introduce memory/state for tracking user issues  
Move towards tool-based agent execution  


## 9. Conclusion

The system has been successfully transitioned from a simple CLI chatbot into a modular agentic system with:
Understanding (intent)
Decision-making (action)
Execution (simulated)

Further work will focus on improving reliability and real-world integration.