from pylab import *
import pandas as pd
import Common as common

import plotly.plotly as py
import plotly.graph_objs as go
from plotly.offline import init_notebook_mode, plot, iplot
import Common as common


class EventDisplay():
    def __init__(self):
        pass


    def show(self,df,eventIds):
        geom     = self._figureHGCalGeometry()
        genparts = self._figureGentLines(df,eventIds)
        rechits  = self._figureRechits(df,eventIds)

        fig = go.Figure(data   = geom+genparts+rechits,
                        layout = go.Layout(scene = dict(xaxis=dict(title='x (cm)'),
                                                        yaxis=dict(title='z (cm)'),
                                                        zaxis=dict(title='y (cm)')),
                                            margin = dict(l=0,r=0,b=0,t=0)
                                            ))
        iplot(fig, filename=common.getBaseDir()+'plots/test')



    def _figureGentLines(self,df,eventIds):
        genLinesList = []
        
        for idx in eventIds:
            event = df.loc[idx]
            n = len(event.gen_e)

            x = np.zeros(n*2)
            y = np.zeros(n*2)
            z = np.zeros(n*2)
            
            mode = common.getTauDecayMode(event.gen_id)
            genLinesColor = ["red","blue","gray"][mode]

            for i in range(n):
                if (event.gen_e[i]>10) & ((event.gen_vx[i]**2 + event.gen_vy[i]**2) < 200**2):
                    x[2*i]=event.gen_vx[i]
                    y[2*i]=event.gen_vy[i]
                    z[2*i]=event.gen_vz[i]
            
            genLines = go.Scatter3d(x=x, y=z, z=y, mode='lines',marker=dict(size=0,color=genLinesColor,opacity=1,line = dict(width =0))) 
            genLinesList.append(genLines)
            
        return genLinesList

    def _figureRechits(self,df,eventIds):
        rechitsList = []
        for idx in eventIds:
            event = df.loc[idx]
            
            slt = event.e>0.02
            e = event.e[slt]
            x = event.x[slt]
            y = event.y[slt]
            z = event.z[slt]
        
            rechits = go.Scatter3d(x=x,y=z,z=y,mode='markers',
                                marker=dict(size = 10*e**0.5,
                                            line = dict(width = 0))) 
            rechitsList.append(rechits)
        return rechitsList

    def _figureHGCalGeometry(self):
        x,y,z = common.truncatedCone(1.48,3.0,320,352)
        geomEE = go.Surface(x=x, y=z, z=y, surfacecolor=0.5*np.ones_like(y),cmin=0,cmax=1,opacity=0.3,showscale=False)

        x,y,z = common.truncatedCone(1.48,3.0,357,410)
        geomFH = go.Surface(x=x, y=z, z=y, surfacecolor=0.5*np.ones_like(y),cmin=0,cmax=1,opacity=0.3,showscale=False)

        x,y,z = common.truncatedCone(1.4,3.0,415,500)
        geomBH = go.Surface(x=x, y=z, z=y, surfacecolor=0.5*np.ones_like(y),cmin=0,cmax=1,opacity=0.3,showscale=False)

        return [geomEE,geomFH,geomBH]