def main(log, json, websocket, create_connection, threading):

    websocket.enableTrace(False)

    try:
        ws = create_connection('ws://localhost:5000/ws/chat/BrainAPI/')
        ws.send(json.dumps({
            'message': "Hello Brain API"
        }))

        recieve_thread = threading.Thread(target=receive(ws, json, log))
        recieve_thread.start()


    except:
        log.info("Websocket Failed")


def receive(ws, json, log):
    while True:
        result = ws.recv()
        if result is not None:
            result = json.loads(result)
            log.info(result['message'])
