import asyncio
from typing import Dict
from openai import OpenAI

# Load API keys
with open(r"C:\mindful-ai\sapient-ds\2024\presentation\week-06\openai-api-key-purushotham.txt") as f:
    openai_api_key = f.read().strip()

client = OpenAI(api_key=openai_api_key)

class ModelSession:
    def __init__(self, session_id: str):
        self.session_id = session_id
        self.history = []

    async def handle_input(self, user_input: str):
        # Store user input
        self.history.append({"role": "user", "content": user_input})
        
        # Call LLM
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=self.history,
            max_tokens=200
        )
        
        # Store assistant response
        assistant_msg = response.choices[0].message
        self.history.append({"role": "assistant", "content": assistant_msg.content})
        return assistant_msg.content

sessions: Dict[str, ModelSession] = {}

async def handle_client(reader, writer):
    data = await reader.readline()
    session_id, user_input = data.decode().strip().split(":", 1)

    if session_id not in sessions:
        sessions[session_id] = ModelSession(session_id)

    response = await sessions[session_id].handle_input(user_input)
    writer.write(response.encode() + b"\n")
    await writer.drain()
    writer.close()

async def main():
    server = await asyncio.start_server(handle_client, "127.0.0.1", 8888)
    print("Server running on 127.0.0.1:8888")
    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    asyncio.run(main())
