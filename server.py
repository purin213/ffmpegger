import os
import socket
from pathlib import Path
import subprocess
import json

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
addr = socket.gethostbyname(socket.gethostname())
port = 8080

sock.bind((addr, port))
sock.listen(1)

while True:
    connection, _ = sock.accept()
    try:
        # contains inputname and outputname
        json_data = json.loads(connection.recv(1024).decode())
        input_basename = json_data['input_basename']
        input_size = json_data['input_size']
        STREAM_RATE = 1400
        data = connection.recv(input_size if input_size <= STREAM_RATE else STREAM_RATE)
        # open file sent from client
        with open(Path(input_basename).name, 'wb+') as f:
            while data:
                f.write(data)
                data = connection.recv(input_size if input_size <= STREAM_RATE else STREAM_RATE)
        cmd_list = connection.recv(1024).decode().split(' ')
        subprocess.run(cmd_list)
        os.remove(f)

        # write file to send to client
        with open(Path(cmd_list[-1]).name, 'rb') as output:
            output.seek(0, os.SEEK_END)
            output_size = output.tell()
            output.seek(0, 0)

            _, output_extension = os.path.splitext(output.name)

            json_data = {
                'output_basename': cmd_list[-1],
                'output_size': output_size
            }

            sock.send(json.dumps(json_data).encode())
            # send to client
            data = output.read(1400)
            while data:
                sock.send(data)
                data = f.read(1400)

    except Exception as e:
        print(f'Errorr: {str(e)}')
    finally:
        connection.close()
