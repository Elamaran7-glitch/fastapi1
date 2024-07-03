import asyncio
import websockets

async def send_pdf(uri, file_path):
    async with websockets.connect(uri) as websocket:
        with open(file_path, "rb") as f:
            while chunk := f.read(1024):  # Read the file in chunks
                await websocket.send(chunk)
        await websocket.close()

file_path = "lumen 2.pdf"  # Replace with your PDF file path
uri = "ws://localhost:8000/pdf"  # Replace with your server's WebSocket URI

asyncio.get_event_loop().run_until_complete(send_pdf(uri, file_path))









