def _exec(inputname, outputname):
    start = input('Input starting position (ex. 00:00:20) : ')
    end = input('Input ending position (ex. 10) : ')
    framerate = input('Input frame rate (ex. 10) : ')
    size = input('Input size (ex. 300) : ')
    return f'ffmpeg -ss {start} -i {inputname} -to {end} -r {framerate} -vf scale={size}:-1 {outputname}.gif'