from ffmpy import FFmpeg as ffmpeg

ff = ffmpeg(
    inputs={'20171113030312.wav': None},
    outputs={'20171113030312-n.wav': ["-ar", "16000"]}
)
print(ff.cmd)
ff.run()
