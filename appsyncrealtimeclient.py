from base64 import b64encode, decode
from datetime import datetime
from uuid import uuid4

import websocket
import threading

import json

# Constants Copied from AppSync API 'Settings'
API_URL = "https://hpx6nqcpargk5koynpygwtqcly.appsync-api.us-west-2.amazonaws.com/graphql"
API_KEY = "da2-okaasp6snfdtreekaffenvsfla"

# GraphQL subscription Registration object
GQL_SUBSCRIPTION = json.dumps({
        # 'query': 'subscription mysub { addedPost(id:"6") { author title url } }',
        #'query': 'subscription mysub { localresolve { id author title  } }',
        #'query': 'subscription mysub { tickerlocal(ticker:"BTC") { id ticker price  } }',
        'query': 'subscription mysub { tickerlocal { id ticker price  } }',
        'variables': {}
})

# Discovered values from the AppSync endpoint (API_URL)
WSS_URL = API_URL.replace('https','wss').replace('appsync-api','appsync-realtime-api')
HOST = API_URL.replace('https://','').replace('/graphql','')

# Subscription ID (client generated)
SUB_ID = str(uuid4())

# Set up Timeout Globals
timeout_timer = None
timeout_interval = 10

# Calculate UTC time in ISO format (AWS Friendly): YYYY-MM-DDTHH:mm:ssZ
def header_time():
    return datetime.utcnow().isoformat(sep='T',timespec='seconds') + 'Z'

# Encode Using Base 64
def header_encode( header_obj ):
    return b64encode(json.dumps(header_obj).encode('utf-8')).decode('utf-8')

# reset the keep alive timeout daemon thread
def reset_timer( ws ):
    global timeout_timer
    global timeout_interval

    if (timeout_timer):
        timeout_timer.cancel()
    timeout_timer = threading.Timer( timeout_interval, lambda: ws.close() )
    timeout_timer.daemon = True
    timeout_timer.start()

# Create API key authentication header
api_header = {
    'host':HOST,
    'x-api-key':API_KEY
}

# Socket Event Callbacks, used in WebSocketApp Constructor
def on_message(ws, message):
    global timeout_timer
    global timeout_interval

    print('### message ###')
    print('<< ' + message)

    message_object = json.loads(message)
    message_type   = message_object['type']

    if( message_type == 'ka' ):
        reset_timer(ws)

    elif( message_type == 'connection_ack' ):
        timeout_interval = int(json.dumps(message_object['payload']['connectionTimeoutMs']))

        register = {
            'id': SUB_ID,
            'payload': {
                'data': GQL_SUBSCRIPTION,
                'extensions': {
                    'authorization': {
                        'host':HOST,
                        'x-api-key':API_KEY
                    }
                }
            },
            'type': 'start'
        }
        start_sub = json.dumps(register)
        print('>> '+ start_sub )
        ws.send(start_sub)

    elif(message_type == 'data'):
        deregister = {
            'type': 'stop',
            'id': SUB_ID
        }
        end_sub = json.dumps(deregister)
        #暂时关闭，保证一直获取数据
        #print('>> ' + end_sub )
        #ws.send(end_sub)

    elif(message_object['type'] == 'error'):
        print ('Error from AppSync: ' + message_object['payload'])
    
def on_error(ws, error):
    print('### error ###')
    print(error)

def on_close(ws):
    print('### closed ###')

def on_open(ws):
    print('### opened ###')
    init = {
        'type': 'connection_init'
    }
    init_conn = json.dumps(init)
    print('>> '+ init_conn)
    ws.send(init_conn)

if __name__ == '__main__':
    # Uncomment to see socket bytestreams
    #websocket.enableTrace(True)

    # Set up the connection URL, which includes the Authentication Header
    #   and a payload of '{}'.  All info is base 64 encoded
    connection_url = WSS_URL + '?header=' + header_encode(api_header) + '&payload=e30='

    # Create the websocket connection to AppSync's real-time endpoint
    #  also defines callback functions for websocket events
    #  NOTE: The connection requires a subprotocol 'graphql-ws'
    print( 'Connecting to: ' + connection_url )

    ws = websocket.WebSocketApp( connection_url,
                            subprotocols=['graphql-ws'],
                            on_open = on_open,
                            on_message = on_message,
                            on_error = on_error,
                            on_close = on_close,)

    ws.run_forever()