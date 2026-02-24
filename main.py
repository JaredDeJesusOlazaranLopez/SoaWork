import asyncio
import uvicorn
import math
import json

async def mergeSort(A,p,r):
    if p>=r:
        return
    q=math.floor((p+r)/2)
    t1 = asyncio.create_task(mergeSort(A, p, q))
    t2 = asyncio.create_task(mergeSort(A, q+1, r))
    await t1
    await t2
    await merge(A, p, q, r)

async def merge(A, p, q, r):
    L = A[p:q+1]
    R = A[q+1:r+1]
    i = 0
    j = 0
    k = p
    while i < (q - p + 1) and j < (r - q):
        if L[i] <= R[j]:
            A[k] = L[i]
            i += 1
        else:
            A[k] = R[j]
            j += 1
        k += 1
    while i < (q - p + 1):
        A[k] = L[i]
        i += 1
        k += 1
    while j < (r - q):
        A[k] = R[j]
        j += 1
        k += 1

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
        #print(lista)
        #print(numbers)
        n=0
        for _ in lista:
         n += 1
        await mergeSort(lista, 0, n - 1)
        resultado = ", ".join(str(x) for x in lista)

        await send({
          'type': 'http.response.start',
           'status': 200,
            'headers':[
                [b'content-type', b'text/html'],
          ],
        })

        with open("index.html", "r") as f:
            content = f.read()

        content = content.replace("</body>", f"<p>Resultado: {resultado}</p></body>")
        content = content.encode()
        await send({'type': 'http.response.body','body': content})

if __name__ == "__main__":
    uvicorn.run("main:app", port=5000, log_level="info")

    