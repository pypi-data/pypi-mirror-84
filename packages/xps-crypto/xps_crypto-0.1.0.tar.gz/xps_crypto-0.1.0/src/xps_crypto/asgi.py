import uvicorn

if __name__ == "__main__":
    host = '127.0.0.1'
    port = 9010
    uvicorn.run("xps_crypto.api:app", host=host, port=port, reload=True)
