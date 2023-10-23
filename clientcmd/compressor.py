def _exec(inputname, outputname):
    compressionlevel = input('Please select compression level\n' + \
                                    '0 : low\n' + \
                                    '1 : medium\n' + \
                                    '2 : high\n')
    match compressionlevel:
        case '0':
            return f'ffmpeg -i  {inputname} -c:v libx264 {outputname}.mp4'
        case '1':
            return f'ffmpeg -i  {inputname} -c:v libx265 {outputname}.mp4'
        case '2':
            return f'ffmpeg -i  {inputname} -c:v libx265 -b:v 500k {outputname}.mp4'
        case _:
            print('wrong input, read the prompt and try again')