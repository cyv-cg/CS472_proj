import matplotlib.pyplot as plot
import matplotlib.animation as ani
from matplotlib.animation import PillowWriter as PW
from matplotlib.animation import FFMpegWriter as FW
from os.path import exists
class AnimWriter:
    def Visualize(file : str) ->None:
        if(exists('D:\\FFMPEG\\ffmpeg-2022-11-03-git-5ccd4d3060-full_build\\bin\\ffmpeg.exe')):
            plot.rcParams['animation.ffmpeg_path'] = 'D:\\FFMPEG\\ffmpeg-2022-11-03-git-5ccd4d3060-full_build\\bin\\ffmpeg.exe'
            makeMp4 = True
        txt = open(f'{file}', 'r')

        data = txt.readlines()
        size = len(data[0].split('.')[0].split(' '))
        fig = plot.figure()

        frame, =plot.plot([],[],'ko')
        plot.xlim(-.5, size + 0.5)
        plot.ylim(-.5, size + 0.5)

        metadata = dict(title='LITTLE GUYS')
        writer = FW(fps=30, metadata=metadata )
        with writer.saving(fig,f'{file}.mp4' if makeMp4 else f'{file}.gif' ,100):
            for row in range(len(data)):
                plot.title(f'gen {row}')
                for g in range(len(data[row].split('.'))):
                    ts1 = data[row].split('.')[g].split(' ')
                
                    xlist = []
                    ylist = []
                    for j in range(len(ts1)):
                        for r in range(len(ts1[j].strip())):
                            if(ts1[r][j] == '1'):
                                xlist.append(j)
                                ylist.append(size-r)
                    frame.set_data(xlist,ylist)
                    writer.grab_frame()