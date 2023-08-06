# -*- coding: utf-8 -*-
"""
Created on Sun Aug 25 00:12:16 2019

@author: jazzn
"""


import pandas as pd
import numpy as np
from prettytable import PrettyTable
from pyzik.pandly import scatter2D,scatter3D,draw_vectors,histogram,scatterPolar
from time import sleep

class Fplot:
    __G2D = 'scatter2D'
    __G3D = 'scatter3D'
    __GV2 = 'vector2D'
    __GV3 = 'vector3D'
    __H = 'histogram'
    __P = 'polar'
    #rajouter la methode fill sur __G2D
    __expectDaxis={__G2D:['titre','ortho', 'unsur', 'style_tracer', 
              'shape', 'quadril_x', 'quadril_y','subplots', 'xlabel', 'ylabel','xorder'],
            __G3D:['titre', 'unsur','style_tracer','xlabel','ylabel','zlabel'],
            __GV2:['unsur','scalvect','titre','quadril_x','quadril_y','xlabel','ylabel','style_tracer'],
                 __GV3:['unsur','scalvect','titre','quadril_x','quadril_y','quadril_z','xlabel','ylabel','zlabel'
                        ,'style_tracer'],
                  __H:['titre','orientation','histnorm'],
                  __P:['titre','unsur', 'style_tracer','quadril_r', 'quadril_theta']}
    __expectD={__G2D:['color'],__G3D:['color'],__GV2:[],__GV3:[],__H:[],__P:[]}


    def __check_assert(self,typ='axis',**d):
        for kd in d:
            if typ == 'axis':
                assert kd in Fplot.__expectDaxis[self.__kind],f"bad argument {kd} ...\n use :\n{Fplot.__expectDaxis[self.__kind]}"
            else:
                assert kd in Fplot.__expectD[self.__kind],f"bad argument {kd} ...\n use :\n{Fplot.__expectD[self.__kind]}"
                
    def __init__(self,kind='scatter2D',**d):
        styps = [Fplot.__G2D,Fplot.__G3D,Fplot.__GV2,Fplot.__GV3,Fplot.__H,Fplot.__P]
        assert kind in styps,f"kind must be in {styps}"
        self.__kind = kind
        self.__check_assert(typ='axis',**d)
        self.__df=[]
        self.__d = {}
        self.__d.update(self.__clean_axis_dict(d))
        self.__init = True

    
    def __clean_axis_dict(self,d):
        return {k:v for k,v in d.items() if k in Fplot.__expectDaxis[self.__kind]}  
    
    def hist(self,x,label='',**d):
        """
        set histogram data for plotting
        > gfx = Fplot(kind='histogram')
        > gfx.hist(x,label='values of ...').orientation('vertical').show()
        x is numpy 1D array
        sub methods availables :
            * orientation
        """
        try:
            g = self.__init
        except:
            self.__init__(kind=Fplot.__H)
        assert self.__kind == Fplot.__H,f"use hist only if u want draw histogram, change ur kind type to: {Fplot.__H}"
        self.__check_assert(typ='xyz',**d)
        datf = pd.DataFrame({'x':x})
        coltxt = '' if label == '' else ' |' + label
        if isinstance(self.__df,list):
            self.__df = datf
            self.__df.columns = ['x0'+coltxt]
        else:
            i = len(list(self.__df.columns))
            datf.columns = [f"x{i}"+coltxt]
            self.__df = pd.concat([self.__df,datf],axis=1)
        self.__d.update(self.__clean_dict(d))
        return self
    
    def draw_vector2D(self,point=tuple(),vector=tuple(),**d):
        """
        set vector 2D data for plotting
        > gfx = Fplot(kind='vector2D')
        > gfx.draw_vector2D(point=(x,y),vector=(vx,vy)).show()
        x,y,vx,vy are numpy 1D arrays
        """
        try:
            g = self.__init
        except:
            self.__init__(kind=Fplot.__GV2)
        assert self.__kind == Fplot.__GV2,f"use draw_vector2D only if u want draw 2D gfx with vectors, change ur kind type to: {Fplot.__GV2}"
        assert len(point)==2,'point must have 2 coordinates'
        assert len(vector)==2,'vector must have 2 coordinates'
        #assert len(set([len(i) for i in point+vector]))==1,'arrays must have same lenght'
        self.__check_assert(typ='xyz',**d)
        datf = pd.DataFrame({'x':point[0],'y':point[1],'ux':vector[0],'uy':vector[1]})
        datf.info = ''
        self.__df = [datf]
        self.__d.update(self.__clean_dict(d))
        return self
    
    def draw_vector3D(self,point=tuple(),vector=tuple(),**d):
        """
        set vector 3D data for plotting
        > gfx = Fplot(kind='vector3D')
        > gfx.draw_vector3D(point=(x,y,z),vector=(vx,vy,vz)).show()
        x,y,z,vx,vy,vz are numpy 1D arrays
        """
        try:
            g = self.__init
        except:
            self.__init__(kind=Fplot.__GV3)
        assert self.__kind == Fplot.__GV3,f"use draw_vector2D only if u want draw 2D gfx with vectors, change ur kind type to: {Fplot.__GV2}"
        assert len(point)==3,'point must have 2 coordinates'
        assert len(vector)==3,'vector must have 2 coordinates'
        assert len(set([len(i) for i in point+vector]))==1,'arrays must all be same length'
        self.__check_assert(typ='xyz',**d)
        datf = pd.DataFrame({'x':point[0],'y':point[1],'z':point[2],'ux':vector[0],'uy':vector[1],'uz':vector[2]})
        datf.info = ''
        self.__df = [datf]
        self.__d.update(self.__clean_dict(d))
        return self
        
    def plot(self,x,y,label='',**d):
        """
        set data for plotting
        > gfx = Fplot(kind='scatter2D')
        > gfx.plot(x,y,label='y=f(x)').show()
        x,y are numpy 1D arrays same size
        """
        try:
            g = self.__init
        except:
            self.__init__(kind=Fplot.__G2D)
        assert self.__kind == Fplot.__G2D,f"use plot only if u want draw 2D gfx, change ur kind type to: {Fplot.__G2D}"
        assert isinstance(x,(np.ndarray,list)),"x must be numpy array or list"
        assert isinstance(y,(np.ndarray,list)),"y must be numpy array or list"
        #assert len(x)==len(y),"arrays must have same lenght"
        if len(x)>len(y):
            x = x[:len(y)]
        if len(y)>len(x):
            y = y[:len(x)]
        self.__check_assert(typ='xyz',**d)
        datf = pd.DataFrame({'x':x,'y':y})
        datf.info = label
        self.__df.append(datf)
        self.__d.update(self.__clean_dict(d))
        return self

    def polar(self,theta,r,label='',**d):
        """
        set data for polar plotting
        > gfx = Fplot(kind='polar')
        > gfx.dplot(r,theta,label='r=f(theta)').show()
        r,theta are numpy 1D arrays
        theta in radian
        """
        try:
            g = self.__init
        except:
            self.__init__(kind=Fplot.__P)
        assert self.__kind == Fplot.__P,f"use polar only if u want draw 2D gfx, change ur kind type to: {Fplot.__G2D}"
        assert isinstance(r,(np.ndarray,list)),"x must be numpy array or list"
        assert isinstance(theta,(np.ndarray,list)),"x must be numpy array or list"
        assert len(r)==len(theta),"arrays must have same lenght"
        self.__check_assert(typ='xyz',**d)
        datf = pd.DataFrame({'theta':theta,'r':r})
        datf.info = label
        self.__df.append(datf)
        self.__d.update(self.__clean_dict(d))
        return self
    
    def title(self,title):
        """Ex : title('title of graphics')"""
        self.__d.update({'titre':title})
        return self
    
    def xlabel(self,xlabel):
        """Ex : xlabel("name of x axis")"""
        self.__d.update(self.__clean_axis_dict({'xlabel':xlabel}))
        return self
    
    def ylabel(self,ylabel):
        """Ex : ylabel("name of y axis")"""
        self.__d.update(self.__clean_axis_dict({'ylabel':ylabel}))
        return self
    
    def zlabel(self,zlabel):
        """Ex : zlabel("name of z axis")"""
        self.__d.update(self.__clean_axis_dict({'zlabel':zlabel}))
        return self
    
    def xgrid(self,xgrid):
        """Ex: xgrid(50) for have 50 (max) line in x-axis"""
        self.__d.update(self.__clean_axis_dict({'quadril_x':xgrid}))
        return self
    
    def ygrid(self,ygrid):
        """Ex: ygrid(50) for have 50 (max) line in y-axis"""
        self.__d.update(self.__clean_axis_dict({'quadril_y':ygrid}))
        return self
    
    def zgrid(self,zgrid):
        """Ex: zgrid(50) for have 50 (max) line in z-axis
        u can use 20 or 10 or ..."""
        self.__d.update(self.__clean_axis_dict({'quadril_z':zgrid}))
        return self
    
    def marker(self,marker):
        """Ex: marker('o') for have only points in graph
        anothers : only marker  'o' '*' '+' 'x' '[' ']' '<' '>' '/' 
        '\' '%' or with line '-o','-*',':',';' etc
        """
        self.__d.update(self.__clean_axis_dict({'style_tracer':marker}))
        return self
    
    def subplots(self,subplots):
        """Ex: subplots(True) for have multiple gfx"""
        self.__d.update(self.__clean_axis_dict({'subplots':subplots}))
        return self
    
    def xorder(self,xorder):
        """Ex: xorder('reversed') for reverse x-axis order
        xorder('normal') is default value"""
        self.__d.update(self.__clean_axis_dict({'xorder':xorder}))
        return self
        
    def scalvect(self,scalvect):
        """Ex: scalvect(0.5) for decrease lenght of vectors
        scalvect(1.5) for increase
        or anothers floatings values of course !!!"""
        self.__d.update(self.__clean_axis_dict({'scalvect':scalvect}))
        return self

    def unsur(self,unsur):
        """Ex: unsur(3) for plot only 1 point over 3
        reduce number of points to plot"""
        self.__d.update(self.__clean_axis_dict({'unsur':unsur}))
        return self
   
    def orientation(self,orientation):
        """Ex: orientation('vertical') or orientation('horizontal') up2u"""
        self.__d.update(self.__clean_axis_dict({'orientation':orientation}))
        return self
    
    def shape(self,shape):
        """Ex: shape() too dificult ..."""
        self.__d.update(self.__clean_axis_dict({'shape':shape}))
        return self
    
    def histnorm(self,histnorm):
        """Ex: histnorm('percent') for have percent y-axis
        histnorm('') for normal y-axis
        """
        self.__d.update(self.__clean_axis_dict({'histnorm':histnorm}))
        return self
    
    def ortho(self,ortho):
        """Ex: ortho('ortho') for have orthonormal axes, ideal for draw trajectory"""
        self.__d.update(self.__clean_axis_dict({'ortho':ortho}))
        return self

    def thetagrid(self,thetagrid):
        """set the angular grid value
        Ex: thetagrid(36)"""
        self.__d.update(self.__clean_axis_dict({'quadril_theta':thetagrid}))
        return self
    
    def rgrid(self,rgrid):
        """set the radius r grid value
        Ex: rgrid(25)"""
        self.__d.update(self.__clean_axis_dict({'quadril_r':rgrid}))
        return self
    
    def get_methods(self):
        __methods ={'titre':self.title,'ortho':self.ortho,'unsur':self.unsur,'shape':self.shape,
                  'quadril_x':self.xgrid,'quadril_y':self.ygrid,
           'quadril_z':self.zgrid,'subplots':self.subplots,'xlabel':self.xlabel,'ylabel':self.ylabel,
                  'zlabel':self.zlabel,
           'xorder':self.xorder,'scalvect':self.scalvect,'orientation':self.orientation,'histnorm':self.histnorm,
            'style_tracer':self.marker,'quadril_theta':self.thetagrid,'quadril_r':self.rgrid}
        print(f"methods availables for ur kind={self.__kind}:\n")
        t = PrettyTable()
        methods = [__methods[eld].__name__ for eld in Fplot.__expectDaxis[self.__kind]]
        desc = [__methods[eld].__doc__ for eld in Fplot.__expectDaxis[self.__kind]]
        t.add_column("Method",methods)
        t.add_column("Description",desc)
        t.align["Description"]="l"
        print(t,"\n")
        t = PrettyTable()
        
        maxl = max(len(Fplot.__expectDaxis[self.__kind]),len(Fplot.__expectD[self.__kind]))
        laxis = Fplot.__append_nones(maxl,Fplot.__expectDaxis[self.__kind])
        ldata = Fplot.__append_nones(maxl,Fplot.__expectD[self.__kind])
        t.add_column("Argument Axis",laxis)
        t.add_column("Argument Data",ldata)
        
        print(t)
            
    
    def __append_nones(length, list_):
        """
        Appends Nones to list to get length of list equal to `length`.
        If list is too long raise AttributeError
        """
        if len(list_) < length:
            nones = length - len(list_)
            return list_ + [''] * nones
        elif len(list_) > length:
            raise AttributeError('Length error list is too long.')
        else:
            return list_
    
    def add_regression(self,degre=1,label='model',xlabel=None,ylabel=None):
        assert self.__kind == Fplot.__G2D,f"if u want use add_regression, change ur kind type to: {Fplot.__G2D}"
        assert len(self.__df)>0,"no data to fit ... use plot(x,y) before add_regression method"
        x = self.__df[-1]['x'].values
        y = self.__df[-1]['y'].values
        degre = min(max(degre,0),3)
        idx = np.isfinite(x) & np.isfinite(y)
        resultat = np.polyfit(x[idx],y[idx],degre)
        dd = self.__clean_axis_dict(self.__d)
        if xlabel is None:
            try:
                xlabel = dd['xlabel']
            except:
                xlabel = 'x'
        if ylabel is None:
            try:
                ylabel = dd['ylabel']
            except:
                ylabel = 'y'
        p=np.poly1d(resultat,variable=xlabel)
        y_mod = np.poly1d(resultat)(x)
        datf = pd.DataFrame({'x':x,'y':y_mod})
        datf.info = f"{label} degre={degre}"
        print(f'best polynomial of degree={degre} between {xlabel} and {ylabel} is :')
        print(ylabel+'=')
        print(p)
        self.__df.append(datf)
        return self
        
    def plot3D(self,x,y,z,label,**d):        
        try:
            g = self.__init
        except:
            self.__init__(kind=Fplot.__GV2)
        assert self.__kind == Fplot.__G3D,f"use plot3D only if u want draw 3D gfx, change ur kind type to: {Fplot.__G3D}"
        assert isinstance(x,(np.ndarray,list)),"x must be numpy array or list"
        assert isinstance(y,(np.ndarray,list)),"x must be numpy array or list"
        assert isinstance(z,(np.ndarray,list)),"x must be numpy array or list"
        assert len(set((len(x),len(y),len(z))))==1,'arrays must all be same length'
        self.__check_assert(typ='xyz',**d)
        datf = pd.DataFrame({'x':x,'y':y,'z':z})
        datf.info = label
        self.__df.append(datf)
        self.__d.update(self.__clean_dict(d))
    
    def __repr__(self):
        return ''
    
    def __clean_dict(self,d):
        return {k:v for k,v in d.items() if k in Fplot.__expectD[self.__kind]}   

    def show(self):
        dd = self.__clean_axis_dict(self.__d)
        if self.__kind == Fplot.__G2D:
            if len(self.__df)>1:
                return self.__df[0].scatter2D(x='x',y='y',other_df=self.__df[1:],**self.__d),self.__init__(kind=Fplot.__G2D,**dd)
            else:
                return self.__df[0].scatter2D(x='x',y='y',**self.__d),self.__init__(kind=Fplot.__G2D,**dd)
        elif self.__kind == Fplot.__G3D:
            if len(self.__df)>1:
                return self.__df[0].scatter3D(x='x',y='y',z='z',other_df=self.__df[1:],**self.__d),self.__init__(kind=Fplot.__G3D,**dd)
            else:
                return self.__df[0].scatter3D(x='x',y='y',z='z',**self.__d),self.__init__(kind=Fplot.__G3D,**dd)
        elif self.__kind == Fplot.__GV2:
            return self.__df[0].draw_vectors(point=('x','y'),vector=('ux','uy'),**self.__d),self.__init__(kind=Fplot.__GV2,**dd)
        elif self.__kind == Fplot.__GV3:
            return self.__df[0].draw_vectors(point=('x','y','z'),vector=('ux','uy','uz'),**self.__d),self.__init__(kind=Fplot.__GV3,**dd)
        elif self.__kind == Fplot.__H:
            return self.__df.histogram(x=list(self.__df.columns),**self.__d),self.__init__(kind=Fplot.__H,**dd)
        elif self.__kind == Fplot.__P:
            print(self.__d)
            if len(self.__df)>1:
                return self.__df[0].scatterPolar(theta='theta',r='r',other_df=self.__df[1:],**self.__d),self.__init__(kind=Fplot.__P,**dd)
            else:
                return self.__df[0].scatterPolar(theta='theta',r='r',**self.__d),self.__init__(kind=Fplot.__P,**dd)


def linear_regression(x,y,degre=1,xlabel='x',ylabel='y',plot=True):
    x = np.asanyarray(x) if isinstance(x,list) else x
    y = np.asanyarray(y) if isinstance(y,list) else y
    degre = min(max(degre,0),3)
    idx = np.isfinite(x) & np.isfinite(y)
    resultat = np.polyfit(x[idx],y[idx],degre)
    p=np.poly1d(resultat,variable=xlabel)
    y_mod = np.poly1d(resultat)(x)
    print(f'best polynomial of degree={degre} between {xlabel} et {ylabel} is :')
    print(ylabel+'=')
    print(p)
    if plot:
        gfx = Fplot(kind='scatter2D')
        gfx.xlabel(xlabel).ylabel(ylabel).xgrid(20).ygrid(20).plot(x,y,'experimental').plot(x,y_mod,'fit model')
        return gfx.show()


def compute_ntc_model(temp,resistor,**d):
    if isinstance(temp,list): temp = np.asarray(temp)
    if isinstance(resistor,list): resistor = np.asarray(resistor)
    T0=298.15
    print(f"compute logR and inverse 1/T ..\n")
    __invT = 1/(273.15+temp)
    __lnR = np.log(resistor)
    anim_bar(100,8,0.25)
    print('\n')
    print("compute regression ...\n")
    anim_bar(100,10,0.3)
    print('\n')
    idx = np.isfinite(__invT) & np.isfinite(__lnR)
    resultat = np.polyfit(__invT[idx],__lnR[idx],1)
    #print(f"résultat .. ln(R)={resultat[0]}*(1/T)+{resultat[1]}")
    beta = resultat[0]
    R0 = np.exp(resultat[1]+beta/T0)
    print(f'characteristics of the resistor NTC ... \nBeta={resultat[0]:.1f}\tR25={R0:.1f} Ohm  @{T0-273.15} °C')
    __R_mod=R0*np.exp(beta*(1/(273.15+temp)-1/T0))
    print("\ngraphic of regression")
    gf = Fplot(kind = "scatter2D")
    gf.plot(x=temp,y=resistor,label='R experimental')
    gf.plot(x=temp,y=__R_mod,label='R modelisation')
    return gf.show()

def display_progress(x, tot,ini_txt=''):
    p=int(100*x/tot)
    deb,fin='▓'*p,'░'*(100-p)
    print(ini_txt+' |'+deb+fin+'|'+str(p)+"%",end='\r') 

def anim_bar(xmax,step,dt):
    for i in range(0,xmax,step):
        display_progress(i,xmax)
        sleep(dt)