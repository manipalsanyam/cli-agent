# Issues Faced During Development



## 1. ModuleNotFoundError (openai not found)

**Problem:**  
Python could not find the `openai` module even after installation.

**Cause:**  
The package was installed in a different Python environment than the one being used to run the script.

**Fix:**  
Used:
python -m pip install openai

**Learning:**  
Always ensure that `pip` and `python` refer to the same environment.



## 2. PowerShell Execution Policy Error

**Problem:**  
Virtual environment activation failed with a script execution error.

**Cause:**  
PowerShell restricts execution of local scripts by default.

**Fix:**  
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser

**Learning:**  
System-level security settings can affect development tools.



## 3. File Naming Issue (main.py not detected)

**Problem:**  
Python could not run the script even though the file existed.

**Cause:**  
File was saved as `main.py.txt` due to Windows default settings.

**Fix:**  
Renamed the file correctly to `main.py`.

**Learning:**  
Always verify file extensions, especially on Windows systems.



## 4. Git Remote Repository Error

**Problem:**  
`git push` failed with "repository not found".

**Cause:**  
Incorrect remote URL and repository not properly configured.

**Fix:**  
Removed incorrect remote and added the correct GitHub repository URL.

**Learning:**  
Always verify repository URL and existence before pushing.



## 5. LM Studio Integration Issues

**Problem:**  
Initial confusion while integrating LM Studio with the CLI agent.

**Cause:**  
Difference between OpenAI API usage and local LLM setup was not clearly understood.

**Fix:**  
- Configured base URL: http://localhost:1234/v1  
- Used a dummy API key ("lm-studio")  
- Ensured model was loaded and server was running  

**Learning:**  
Local LLMs require proper server setup and endpoint configuration.



## 6. Overuse of Class-Based Structure

**Problem:**  
Initially implemented services using classes, increasing complexity.

**Cause:**  
Misunderstanding of microservice-style architecture as requiring OOP design.

**Fix:**  
Refactored services into simple functional modules.

**Learning:**  
Separation of concerns is more important than abstraction at early stages.



## 7. Difficulty in Modularizing the CLI Agent

**Problem:**  
The original CLI agent had all logic in one file, making it hard to split into services.

**Cause:**  
Lack of clarity on how to separate responsibilities.

**Fix:**  
Divided the system into:
- chat_service (LLM interaction)  
- intent_service (classification)  
- action_service (decision making)  

**Learning:**  
Breaking systems into smaller modules improves clarity and scalability.



## 8. Intent Classification Inconsistency

**Problem:**  
The model returned inconsistent outputs for similar queries.

**Cause:**  
Prompt was not strict enough, leading to responses like full sentences instead of labels.

**Fix:**  
- Added strict instructions (return only label)  
- Included examples in the prompt  
- Cleaned output using string processing  

**Learning:**  
Prompt design directly affects system reliability.



## 9. Chatbot vs Agent Confusion

**Problem:**  
Initially treated the system as a chatbot that only responds to queries.

**Cause:**  
Lack of distinction between response generation and decision-making.

**Fix:**  
Introduced:
- intent classification  
- action layer  

**Learning:**  
An agent must:
- understand the query  
- decide what to do  
- take action  



## 10. Static vs Data-Driven Actions

**Problem:**  
Actions were initially hardcoded and not connected to any system.

**Cause:**  
No backend or structured data was used.

**Fix:**  
Introduced structured data (`orders.json`, `payments.json`) to simulate backend systems.

**Learning:**  
Real-world systems rely on data, not static responses.



## 11. Maintaining Clean Flow in main.py

**Problem:**  
As features were added, `main.py` started becoming cluttered.

**Cause:**  
Mixing multiple responsibilities in a single file.

**Fix:**  
Moved logic to service files and kept `main.py` as an orchestrator.

**Learning:**  
Entry point should only coordinate flow, not contain business logic.



## Summary

The development process involved challenges across:
- Environment setup  
- Git configuration  
- System design  
- Prompt engineering  
- Modular architecture  

Each issue helped improve understanding of building reliable and scalable agent systems.
