import asyncio
from typing import Dict
import openai

# Load API key from file
with open(r"C:\mindful-ai\sapient-ds\2024\presentation\week-06\openai-api-key-purushotham.txt") as f:
    openai.api_key = f.read().strip()


class ModelSession:
    def __init__(self, session_id: str):
        self.session_id = session_id
        self.history = []

    async def stream_response(self, user_input: str):
        self.history.append({"role": "user", "content": user_input})

        # Stream response using OpenAI 0.28.0
        stream = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=self.history,
            max_tokens=200,
            stream=True
        )

        response_text = ""
        for event in stream:
            delta_content = event['choices'][0]['delta'].get("content")
            if delta_content:
                response_text += delta_content
                yield delta_content  # yield each token immediately

        # Append full assistant response to history
        self.history.append({"role": "assistant", "content": response_text})


sessions: Dict[str, ModelSession] = {}


async def handle_client(reader, writer):
    data = await reader.readline()
    if not data:
        writer.close()
        return

    try:
        session_id, user_input = data.decode().strip().split(":", 1)
    except ValueError:
        writer.write(b"Invalid input format. Use session_id:message\n")
        await writer.drain()
        writer.close()
        return

    if session_id not in sessions:
        sessions[session_id] = ModelSession(session_id)

    # STREAM TOKENS using async for
    async for token in sessions[session_id].stream_response(user_input):
        writer.write(token.encode())
        await writer.drain()

    writer.write(b"\n")  # end of message
    await writer.drain()
    writer.close()


async def main():
    server = await asyncio.start_server(handle_client, "127.0.0.1", 8888)
    print("Streaming MCP server running on 127.0.0.1:8888")
    async with server:
        await server.serve_forever()


if __name__ == "__main__":
    asyncio.run(main())
