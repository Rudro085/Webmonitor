from fastapi import FastAPI, HTTPException, UploadFile, File, Response
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Optional
import csv
import io
import uvicorn

app = FastAPI()

# Simulated bot and database state
bot_running = False
bot_result = None
selected_db = "default_db"
databases = {"default_db": {}}

class DBUpdateRequest(BaseModel):
    key: str
    value: str

class DBSelectRequest(BaseModel):
    db_name: str

@app.post("/bot/start")
def start_bot():
    global bot_running, bot_result
    if bot_running:
        raise HTTPException(status_code=400, detail="Bot already running")
    bot_running = True
    # Simulate bot work
    bot_result = {"status": "Bot started and running"}
    return {"message": "Bot started"}

@app.post("/bot/stop")
def stop_bot():
    global bot_running
    if not bot_running:
        raise HTTPException(status_code=400, detail="Bot is not running")
    bot_running = False
    return {"message": "Bot stopped"}

@app.get("/bot/result")
def get_result():
    if bot_result is None:
        raise HTTPException(status_code=404, detail="No result available")
    return {"result": bot_result}

@app.post("/db/select")
def select_database(request: DBSelectRequest):
    global selected_db
    if request.db_name not in databases:
        databases[request.db_name] = {}
    selected_db = request.db_name
    return {"message": f"Database '{selected_db}' selected"}

@app.post("/db/update")
def update_database(request: DBUpdateRequest):
    if selected_db not in databases:
        raise HTTPException(status_code=404, detail="Selected database not found")
    databases[selected_db][request.key] = request.value
    return {"message": f"Updated {request.key} in {selected_db}"}

@app.post("/db/upload_csv")
async def upload_csv(file: UploadFile = File(...)):
    if selected_db not in databases:
        raise HTTPException(status_code=404, detail="Selected database not found")
    content = await file.read()
    decoded = content.decode("utf-8")
    reader = csv.reader(io.StringIO(decoded))
    db = {}
    for row in reader:
        if len(row) >= 2:
            db[row[0]] = row[1]
    databases[selected_db] = db
    return {"message": f"CSV uploaded to {selected_db}"}

@app.get("/db/download_csv")
def download_csv():
    if selected_db not in databases:
        raise HTTPException(status_code=404, detail="Selected database not found")
    db = databases[selected_db]
    output = io.StringIO()
    writer = csv.writer(output)
    for key, value in db.items():
        writer.writerow([key, value])
    output.seek(0)
    return StreamingResponse(
        output,
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename={selected_db}.csv"}
    )
    
if __name__ == "__main__":
    uvicorn.run("main_api:app", host="127.0.0.1", port=8000, reload=True)