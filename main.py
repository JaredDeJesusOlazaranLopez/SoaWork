import asgiref
import uvicorn
import math
import json

async def merge(A,p,r):
    if p>=r:
        return
    q=math.floor((p+r)/2)


async def app(scope, receive, send):
    if scope["type"] != "http":
        return
    method = scope["method"]

    #Parte del GET, aqui solo agarro el index y es lo que le muestro al cliente
    if method == "GET":
        await send({
        'type': 'http.response.start',
        'status': 200,
        'headers': [[b'content-type', b'text/html']],
        })
        with open("index.html", "rb") as f:
            content = f.read()
        await send({
        'type': 'http.response.body',
        'body': content
        })
        
    #Parte del POST, aqui es donde procesare los datos y los acomodare con merge sort y los enviare
    elif method == "POST":
        body = b""
        while True:
            event = await receive()
            body += event.get("body", b"")
            if not event.get("more_body", False):
                break
        #print("body recibido:", body)
        data = json.loads(body.decode())
        numbers = data.get("numbers")
        #quita espacios y separa por comas 
        lista = [float("".join(x.split())) for x in numbers.split(",")]
        print(lista)
        #print(numbers)

        await send({
          'type': 'http.response.start',
           'status': 200,
            'headers':[
                [b'content-type', b'text/html'],
          ],
        })

        with open("index.html", "rb") as f:
            content = f.read()

        await send({'type': 'http.response.body','body': content})

if __name__ == "__main__":
    uvicorn.run("main:app", port=5000, log_level="info")

    