import os
import socket
from pathlib import Path
import sys
import json

from clientcmd import aspect_ratio_changer
from clientcmd import compressor
from clientcmd import gif_maker
from clientcmd import mp3ifyer
from clientcmd import res_changer

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
addr = socket.gethostbyname(socket.gethostname())
port = 8080

try:
    sock.connect((addr, port))
except socket.error as err:
    print(err)
    sys.exit(1)

try:
    input_basename = input('Input filename to upload: ')
    with open(input_basename, 'rb') as file:
        # get file size with seek manipulation
        file.seek(0, os.SEEK_END)
        input_size = file.tell()
        file.seek(0, 0)

        _, input_extension = os.path.splitext(file.name)

        if input_extension != '.mp4':
            raise Exception(f'This program only supports mp4 files, got {input_extension}')

        output_basename = input('Input filename to output to: ')
        output_root, output_extension = os.path.splitext(output_basename)

        json_data = {
            'input_basename': input_basename,
            'input_size': input_size,
            'output_basename': output_basename
        }

        sock.send(json.dumps(json_data).encode())

        data = file.read(1400)
        while data:
            sock.send(data)
            data = file.read(1400)

        input_mode = input('Select desired service\n1: compress file\n2: change resolution\n3: change aspect ratio\n4: convert extension to mp3\n5: make gif from timestamp\n')
        match input_mode:
            # input is expected to be a .mp4 extension,
            # output extension can vary depending on the command so only the rootname is passed
            case '1':
                cmd = compressor(input_basename, output_root)
            case '2':
                cmd = res_changer(input_basename, output_root)
            case '3':
                cmd = aspect_ratio_changer(input_basename, output_root)
            case '4':
                cmd = mp3ifyer(input_basename, output_root)
            case '5':
                cmd = gif_maker(input_basename, output_root)
            case _:
                raise Exception('Unexpected input')
        sock.send(cmd.encode())

    json_data = json.loads(sock.recv(1024).decode())
    output_basename = json_data['output_basename']
    output_size = json_data['output_size']
    STREAM_RATE = 1400
    data = sock.recv(output_size if output_size <= STREAM_RATE else STREAM_RATE)
    # open file sent from client
    with open(Path(output_basename), 'wb+') as f:
        while data:
            f.write(data)
            data = sock.recv(output_size if output_size <= STREAM_RATE else STREAM_RATE)
    print(f'Data successfully written to {output_basename}')
except Exception as e:
    print(f'Error: {str(e)}')
finally:
    sock.close()
