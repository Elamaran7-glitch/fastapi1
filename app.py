from fastapi import FastAPI, WebSocket
from starlette.websockets import WebSocketDisconnect

app = FastAPI()
async def save_pdf(websocket: WebSocket, filename: str):
    try:
        await websocket.accept()  # Accept the WebSocket connection
        with open(filename, "wb") as f:
            while True:
                try:
                    data = await websocket.receive_bytes()
                    f.write(data)
                except WebSocketDisconnect:
                    print(f"WebSocket connection closed: {filename}")
                    break
    except Exception as e:
        print(f"Error saving PDF: {e}")

@app.websocket("/pdf")
async def pdf_endpoint(websocket: WebSocket):
    filename = "sample1_received.pdf"  # You can customize this as needed
    await save_pdf(websocket, filename)








