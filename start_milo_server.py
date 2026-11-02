"""Start Milo locally for same-network testing. For worldwide play, deploy server.py to a cloud host."""
import socket
import threading
import uvicorn
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

if __name__ == '__main__':
    try:
        probe = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        probe.connect(('192.0.2.1', 80))
        address = probe.getsockname()[0]
        probe.close()
    except Exception:
        address = 'YOUR-COMPUTER-IP'
    print('\nMILO CO-OP SERVER\n')
    print('Local network test address: http://' + address + ':8765')
    print('For internet play, deploy this folder using the included render.yaml.')
    print('Keep this window open while hosting locally.\n')
    uvicorn.run('server:app', host='0.0.0.0', port=8765, log_level='info')
