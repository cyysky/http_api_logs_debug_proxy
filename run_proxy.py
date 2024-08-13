import uvicorn
from debug_proxy import app, config

if __name__ == "__main__":
    uvicorn.run(app, host=config["host"], port=config["port"])