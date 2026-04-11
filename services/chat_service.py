from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:1234/v1",
    api_key="lm-studio"
)

def get_chat_response(agent, user_input):
    try:
        agent.history.append({"role": "user", "content": user_input})

        response = client.chat.completions.create(
            model="local-model",
            messages=agent.history
        )

        reply = response.choices[0].message.content

        agent.history.append({"role": "assistant", "content": reply})
        agent.count += 1

        return reply

    except Exception as e:
        return f"Error: {str(e)}"
