import matplotlib.pyplot as plot
import matplotlib.animation as ani
from matplotlib.animation import PillowWriter as PW
from matplotlib.animation import FFMpegWriter as FW
from os.path import exists
class AnimWriter:
    def Visualize(file : str) ->None:
        makeMp4 : bool = False
        ffmpeg_path : str = 'C:path\\to\\ffmpeg.exe'
        if(exists(ffmpeg_path)):
            plot.rcParams['animation.ffmpeg_path'] = ffmpeg_path
            makeMp4 = True
        txt = open(f'{file}', 'r')

        data = txt.readlines()
        size = len(data[0].split('.')[0].split(' '))
        fig = plot.figure()

        frame, =plot.plot([],[],'ko')
        plot.xlim(-.5, size + 0.5)
        plot.ylim(-.5, size + 0.5)

        metadata = dict(title='LITTLE GUYS')
        if(makeMp4):  
            writer = FW(fps=30, metadata=metadata )
        else:
            writer = PW(fps=30, metadata=metadata )
        with writer.saving(fig,f'{file.replace(".dat", "")}.mp4' if makeMp4 else f'{file.replace(".dat", "")}.gif' ,100):
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