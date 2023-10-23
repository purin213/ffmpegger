def _exec(inputname, outputname):
    height = input('Please enter the height (ex. 1280) : ')
    width = input('Please enter the width (ex. 720) : ')
    return f'ffmpeg -i {inputname} -filter:v scale={height}:{width} -c:a copy {outputname}.mp4'