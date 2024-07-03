from fastapi import FastAPI,File,UploadFile
from secrets import token_hex


app=FastAPI(title="upload file using FastAPI")


@app.get("/")
async def read_root():
    return {"hello":"FastAPI"}


@app.post("/upload")
async def upload_file(file:UploadFile=File(...)):
    file_ext=file.filename.split(".").pop()
    file_name= token_hex(10)
    file_path=f"{file_name}.{file_ext}"
    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)
    return {"sucess":True, "file_path":file_path,"message":"file uploaded successfully"}    



if __name__ == "__main__":
    uvicorn.run("test:app",host="127.0.0.1",reload=True)







