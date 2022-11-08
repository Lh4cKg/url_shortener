import uvicorn

if __name__ == '__main__':
    uvicorn.run("url_shortener.asgi:application", reload=True)
