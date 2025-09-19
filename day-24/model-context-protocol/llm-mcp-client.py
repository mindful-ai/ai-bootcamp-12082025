import asyncio

async def send_message(session_id: str, message: str):
    reader, writer = await asyncio.open_connection("127.0.0.1", 8888)
    
    # Send data
    writer.write(f"{session_id}:{message}\n".encode())
    await writer.drain()

    # Read response
    response = await reader.readline()
    print(f"Assistant: {response.decode().strip()}")
    
    writer.close()
    await writer.wait_closed()

async def main():
    session_id = "session1"
    while True:
        message = input("You: ")
        await send_message(session_id, message)

if __name__ == "__main__":
    asyncio.run(main())
