from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
import os

app = FastAPI()

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>WebSocket PDF Transfer</title>
    </head>
    <body>
        <h1>WebSocket PDF Transfer</h1>
        <button onclick="connect()">Connect</button>
        <button onclick="downloadFile()">Download PDF</button>
        <button onclick="disconnect()">Disconnect</button>
        <script>
            var ws;

            function connect() {
                ws = new WebSocket("ws://localhost:8000/ws");
                ws.binaryType = "arraybuffer"; // Set binary type to arraybuffer
                ws.onmessage = function(event) {
                    const blob = new Blob([event.data], { type: 'application/pdf' });
                    const url = window.URL.createObjectURL(blob);
                    const link = document.createElement('a');
                    link.href = url;
                    link.setAttribute('download', 'file.pdf'); // Change to your file name
                    document.body.appendChild(link);
                    link.click();
                    link.parentNode.removeChild(link);
                };
                ws.onclose = function(event) {
                    console.log("WebSocket closed:", event);
                };
            }

            function downloadFile() {
                if (ws) {
                    ws.send("send file"); // Trigger file sending
                }
            }

            function disconnect() {
                if (ws) {
                    ws.close();
                }
            }
        </script>
    </body>
</html>
"""

@app.get("/")
async def get():
    return HTMLResponse(html)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    file_sent = False
    try:
        while True:
            data = await websocket.receive_text()
            if data == "send file" and not file_sent:
                pdf_path = "dhoni.pdf"  # Change to your PDF file path
                with open(pdf_path, "rb") as pdf_file:
                    while chunk := pdf_file.read(1024):  # Read in chunks
                        await websocket.send_bytes(chunk)
                file_sent = True  # Mark the file as sent
    except WebSocketDisconnect:
        print("Client disconnected")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        await websocket.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
