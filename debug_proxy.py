from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import requests
import json
import os
import datetime
import traceback
import time
import sys
from pyfiglet import Figlet

# Create a Figlet font object
figlet = Figlet(font='slant')

# Define the text to print
text = "FMCV Debug Proxy"

# Generate and print the ASCII art
ascii_art = figlet.renderText(text)
print(ascii_art)

print("version 20240813\n\n")
print("by chong@fmcv.my www.fmcv.my\n\n")

app = FastAPI()

config = {
    "TARGET_URL": "http://Target:1234",
	"REQEST_CONNECTION_TIMEOUT": 2,
	"REQEST_READ_TIMEOUT": 5,
    "host": "0.0.0.0",
    "port": 8888
}

# Read configuration from file
CONFIG_FILE = "config.txt"
if os.path.isfile(CONFIG_FILE):
    try:
        with open(CONFIG_FILE, "r") as file:
            config = json.load(file)
    except:
        print("read config.txt json format error, please delete it and let program regenerate it.")
        sys.exit()
else:
    with open(CONFIG_FILE, "w") as file:
        file.write(json.dumps(config,indent=2))
    print("Please edit config.txt")
    sys.exit()
    
# Target URL for the REST API
TARGET_URL = config["TARGET_URL"]

# Directory to save debug logs
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

# Get current date for log file names
current_date = datetime.datetime.now().strftime("%Y%m%d")

# Log file names
LOG_FILE = os.path.join(LOG_DIR, f"{current_date}_logs.txt")
ERROR_FILE = os.path.join(LOG_DIR, f"{current_date}_error.txt")

@app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def proxy(path: str, request: Request):
    try:
        # Record start time
        start_time = time.time()

        # Construct the full URL for the target API
        target_url = f"{TARGET_URL}/{path}"
        
        # Extract method, headers, and body
        method = request.method
        headers = dict(request.headers)
        body = await request.body()
        
        # Forward the request to the target API
        response = requests.request(
            method=method,
            url=target_url,
            headers=headers,
            data=body,
            params=request.query_params,
            timeout=(config["REQEST_CONNECTION_TIMEOUT"],config["REQEST_READ_TIMEOUT"])
        )
        # Record end time
        end_time = time.time()

        # Calculate elapsed time
        duration = end_time - start_time

        print(f"Elapsed time: {duration} seconds")
        # Log request and response for debugging
        log_request_and_response(path, method, headers, body, response, duration)
        

        # Parse the response content as JSON
        try:
            response_content = response.json()
        except json.JSONDecodeError:
            response_content = {"raw_content": response.content.decode(response.encoding or "utf-8")}
        
        # Merge the status code and headers into the response content
        merged_response = {
            "status_code": response.status_code,
            "headers": dict(response.headers),
            **response_content,
        }
        
        # Relay the merged response back to the client
        return JSONResponse(content=merged_response)
        
    except Exception as e:
        # Log any exceptions that occur
        log_error(e, target_url, method, headers, body)
        return {"result":False, "message": "An debug proxy recorded an error occurred. Please check the logs."}

def log_request_and_response(path, method, headers, body, response, duration):
    log_entry = {
        "path": path,
        "method": method,
        "headers": headers,
        "body": body.decode('utf-8') if body else None,
        "response_status": response.status_code,
        "response_headers": dict(response.headers),
        "response_body": response.content.decode(response.encoding or "utf-8"),
        "response_duration": duration
    }
    
    with open(LOG_FILE, "a") as log_file:
        log_file.write(json.dumps(log_entry, indent=2) + "\n\n")
        
def log_error(exception, target_url, method, headers, body):
    error_message = "".join(traceback.format_exception(None, exception, exception.__traceback__))
 
    error_log_entry = {
        "error_message": error_message,
        "target_url": target_url,
        "method": method,
        "headers": headers,
        "body": body.decode('utf-8') if body else None,
    }
    
    with open(ERROR_FILE, "a") as error_file:
        error_file.write(f"{datetime.datetime.now()}:\n{json.dumps(error_log_entry, indent=2)}\n\n")
        
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, config["host"], port=config["port"])