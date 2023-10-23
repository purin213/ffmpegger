def _exec(inputname, outputname):
    height = input('Please enter the height (ex. 16) : ')
    width = input('Please enter the width (ex. 9) : ')
    return f'ffmpeg -i {inputname} -pix_fmt yuv420p -aspect {height}:{width} {outputname}.mp4'