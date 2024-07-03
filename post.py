from fastapi import FastAPI, WebSocket
import asyncio

app = FastAPI()

async def send_pdf(websocket: WebSocket):
    try:
        # Open the PDF file and read its content
        with open('lumen 2.pdf', 'rb') as pdf_file:
            # Send the PDF content in chunks
            while True:
                chunk = pdf_file.read(1024)
                if not chunk:
                    break  # Exit the loop when EOF is reached
                await websocket.send_bytes(chunk)

    except Exception as e:
        # Handle any exceptions
        print(f"Error: {e}")


@app.websocket("/pdf")
async def pdf_endpoint(websocket: WebSocket):
    await websocket.accept()
    await send_pdf(websocket)

