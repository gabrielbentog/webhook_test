# client.py
import asyncio
import websockets

async def communicate():
    async with websockets.connect("ws://localhost:8765") as websocket:
        print("Conectado ao servidor")
        await websocket.send("Olá, servidor!")
        response = await websocket.recv()
        print(f"Resposta do servidor: {response}")
        print("Desconectando do servidor")

if __name__ == "__main__":
    asyncio.run(communicate())
