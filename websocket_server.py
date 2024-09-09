import asyncio
import websockets
import json

# Estados possíveis e suas transições (adjacências)
graph = {
    'Q0': ['Q1', 'Q2'],
    'Q1': ['Q0', 'Q3'],
    'Q2': ['Q0'],
    'Q3': ['Q1']
}

# Estado inicial
current_state = 'Q0'

async def handler(websocket, path):
    global current_state
    
    while True:
        state_info = {
            'type': 'state',
            'current_state': current_state,
            'possible_transitions': graph[current_state]
        }
        await websocket.send(json.dumps(state_info))

        message = await websocket.recv()
        print(f"Recebido: {message}")

        try:
            data = json.loads(message)
            if data['type'] == 'state_transition':
                chosen_state = data['chosen_state']

                # Verificar se a transição é válida
                if chosen_state in graph[current_state]:
                    current_state = chosen_state
                    print(f"Transição válida! Novo estado: {current_state}")
                else:
                    print(f"Transição inválida de {current_state} para {chosen_state}")

                state_info = {
                    'type': 'state',
                    'current_state': current_state,
                    'possible_transitions': graph[current_state]
                }
                await websocket.send(json.dumps(state_info))
            else:
                print("Tipo de mensagem desconhecido")
        except json.JSONDecodeError as e:
            print(f"Erro ao decodificar JSON: {e}")

async def main():
    async with websockets.serve(handler, "localhost", 8765):
        print("Servidor WebSocket em execução...")
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())
