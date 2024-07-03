from fastapi import FastAPI, WebSocket
from starlette.websockets import WebSocketDisconnect

app = FastAPI()

async def save_pdf(websocket: WebSocket):
    try:
        await websocket.accept()  # Accept the WebSocket connection
        while True:
            data = await websocket.receive_bytes()
            with open("received_file.pdf", "wb") as f:
                f.write(data)
    except WebSocketDisconnect:
        pass

@app.websocket("/pdf")
async def pdf_endpoint(websocket: WebSocket):
    await save_pdf(websocket)
 



