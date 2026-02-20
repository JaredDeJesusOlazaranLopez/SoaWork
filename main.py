import asgiref
import uvicorn
import math

def merge(A,p,r):
    if p>=r:
        return
    q=math.floor((p+r)/2)


async def app(scope, receive, send):
    await send({
        'type': 'http.response.start',
        'status': 200,
        'headers':[
            [b'content-type', b'text/html'],
        ],
    })

    with open("index.html", "rb") as f:
        content = f.read()

    await send({
        'type': 'http.response.body',
        'body': content
    })

if __name__ == "__main__":
    uvicorn.run("main:app", port=5000, log_level="info")

    