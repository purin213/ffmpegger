def _exec(inputname, outputname):
    return f'ffmpeg -i {inputname} -vn {outputname}.mp3'