import asyncio

async def send_message(session_id: str, message: str):
    reader, writer = await asyncio.open_connection("127.0.0.1", 8888)

    writer.write(f"{session_id}:{message}\n".encode())
    await writer.drain()

    print("Assistant: ", end="", flush=True)

    while True:
        token = await reader.read(1)  # read byte-by-byte for streaming
        if not token or token == b"\n":  # end of response
            break
        print(token.decode(), end="", flush=True)

    print("\n")
    writer.close()
    await writer.wait_closed()


async def main():
    session_id = "session1"
    while True:
        message = input("You: ")
        if message.lower() in ["exit", "quit"]:
            break
        await send_message(session_id, message)


if __name__ == "__main__":
    asyncio.run(main())
