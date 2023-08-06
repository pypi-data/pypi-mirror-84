# -*- coding: utf-8 -*-
"""
Created on Tue Mar 24 13:37:34 2020

@author: jazzn
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 13:56:58 2020

@author: jazzn
"""

import sys
import random
import io
import base64
import pandas as pd
import chempy as cp
import requests
from sympy import *
import urllib.parse
import random
from collections import OrderedDict
import chempy as cp
import numpy as np
import json

sin = lambda x:np.sin(x/180*np.pi)
cos = lambda x:np.cos(x/180*np.pi)
asin = lambda x:np.arcsin(x)*180/np.pi
acos = asin = lambda x:np.arccos(x)*180/np.pi

def superLoc(df,idx,*cols,converters={},sample=None):
    if sample != None:
        idx = random.sample(list(df.index),sample)
    if isinstance(idx,int):
        return tuple([converters.get(col,lambda x:x)(df.loc[idx,col]) for col in cols])
    elif isinstance(idx,list):
        return tuple([[converters.get(col,lambda x:x)(df.loc[indx,col]) for indx in idx] for col in cols])
    
    
def ppcm(a,b):
    """ppcm(a,b): calcul du 'Plus Petit Commun Multiple' entre 2 nombres entiers a et b"""
    if (a==0) or (b==0):
        return 0
    else:
        return (a*b)//pgcd(a,b)
def pgcd(a,b):
    """pgcd(a,b): calcul du 'Plus Grand Commun Diviseur' entre les 2 nombres entiers a et b"""
    if b==0:
        return a
    else:
        r=a%b
        return pgcd(b,r)
    
def getIonicFormula(f_cat,f_ani):
    """ f_cat, f_ani : formule chimique cation anion au format CP
        return : {formule solution ionique},{"coef_cat":c1,"coef_ani":c2}
    """
    def no_1(x):
        return x if x != 1 else ""
    f_cat = f_cat.replace(u'\xa0', u' ')
    f_ani = f_ani.replace(u'\xa0', u' ')
    index = list("₀₁₂₃₄₅₆₇₈₉")
    catCP = cp.Substance.from_formula(f_cat)
    aniCP = cp.Substance.from_formula(f_ani)
    charge_cat , charge_ani = catCP.charge , aniCP.charge
    PPCM = ppcm(charge_cat,charge_ani)
    c1 , c2 = int(abs(PPCM/charge_cat)) , int(abs(PPCM/charge_ani))
    par1c , par2c , par3c = "(" if c1>1 else "" , ")" if c1>1 else "" , index[c1] if c1>1 else ""
    par1a , par2a , par3a = "(" if c2>1 else "" , ")" if c2>1 else "" , index[c2] if c2>1 else ""
    cationC = cp.Substance.from_formula(f_cat.split("+")[0]).unicode_name
    anionC = cp.Substance.from_formula(f_ani.split("-")[0]).unicode_name
    ionicS = f"{par1c}{cationC}{par2c}{par3c}{par1a}{anionC}{par2a}{par3a}"
    ionicSCP = f"{par1c}{f_cat.split('+')[0]}{par2c}{no_1(c1)}{par1a}{f_ani.split('-')[0]}{par2a}{no_1(c2)}"
    ionicF = f"{no_1(c1)}{catCP.unicode_name}(aq) + {no_1(c2)}{aniCP.unicode_name}(aq)"
    dissolution_react = f"{ionicS} → {ionicF}"
    return {"dissolution reaction":dissolution_react,"ionic solidCP":ionicSCP,"ionic solid":ionicS,"ionic formula":ionicF,"coef_cat":c1,"coef_ani":c2}

def convert2img(url,sizeX=200,sizeY=200,opt=None):
    img = f"""<p><img src="{url}" alt="" width="{sizeX}" /></p>"""
    return img

def convertStrReac2HTML(reaction):
    R = cp.Reaction.from_string(reaction)
    subst = {k: cp.Substance.from_formula(k) for k in R.keys()}
    return R.html(subst)

def convertReacProd2Reaction(reac,prod,converters = lambda x:x):
    reac = converters(reac)
    prod = converters(prod)
    reacCP, prodCP = cp.balance_stoichiometry(reac, prod)
    txt , reaction = [],""
    for esp,coef in reacCP.items():
        txt.append(f"{coef} {esp} ")
    reaction = " + ".join(txt)
    txt = []
    for esp,coef in prodCP.items():
        txt.append(f"{coef} {esp} ")
    reaction = reaction + " -> " + " + ".join(txt)
    return convertStrReac2HTML(reaction)
    
def convertRedox2Reac(Ox1,Red1,Ox2,Red2):
    """Ox,Red orderedDict of 1/2 Eq reaction
    return reac,prod : set of reaction
    """
    e1 = cp.Equilibrium(ox1, red1)
    e2 = cp.Equilibrium(red2 , ox2)
    cs = cp.Equilibrium.eliminate([e1, e2], 'e-')
    redox_eq = str(e1*cs[0] + e2*cs[1]).replace("=","->")
    redox_eq = cp.Reaction.from_string(redox_eq)
    prod = set(redox_eq.prod)
    reac = set(redox_eq.reac)
    return reac,prod

def convert2LatexXAZ(el,A,Z):
    """ convertit el,A,Z en représentation latex
        el : str Ex H
        A,Z chimie
    """
    txt = f"""{{\\displaystyle {{}}_{{{Z}}}^{{{A}}}\operatorname {{{el}}} }}"""
    return txt

def convertList2Str(L,sep=', '):
    txt = ", ".join(L[:-1])
    txt += " et "+L[-1]       
    return txt

def convert2gfx(gfx_text,x_min=-10,x_max=10,y_min=-10,y_max=10,dx=1,dy=1):
    gfx_text = str(urllib.parse.quote(gfx_text))
    url = f"""https://graphsketch.com/?eqn1_color=1&eqn1_eqn={gfx_text}&eqn2_color=2&eqn2_eqn=&eqn3_color=3&eqn3_eqn=&eqn4_color=4&eqn4_eqn=&eqn5_color=5&eqn5_eqn=&eqn6_color=6&eqn6_eqn=&x_min={x_min}&x_max={x_max}&y_min={y_min}&y_max={y_max}&x_tick={dx}&y_tick={dy}&x_label_freq=5&y_label_freq=5&do_grid=0&do_grid=1&bold_labeled_lines=0&bold_labeled_lines=1&line_width=4&image_w=650&image_h=425"""
    iframe = f"""<p><iframe style="width: 850px; height: 495px; overflow: hidden;" src="{url}" width="1000" height="1000" scrolling="no">Iframes not supported</iframe></p>"""
    return iframe

def convert2gfx3(gfx_text1,gfx_text2,gfx_text3,x_min=-10,x_max=10,y_min=-10,y_max=10,dx=1,dy=1,colors = [1,2,3]):
    gfx_text1 = str(urllib.parse.quote(gfx_text1))
    gfx_text2 = str(urllib.parse.quote(gfx_text2))
    gfx_text3 = str(urllib.parse.quote(gfx_text3))
    c1,c2,c3 = tuple(colors)
    url = f"""https://graphsketch.com/?eqn1_color={c1}&eqn1_eqn={gfx_text1}&eqn2_color={c2}&eqn2_eqn={gfx_text2}&eqn3_color={c3}&eqn3_eqn={gfx_text3}&eqn4_color=4&eqn4_eqn=&eqn5_color=5&eqn5_eqn=&eqn6_color=6&eqn6_eqn=&x_min={x_min}&x_max={x_max}&y_min={y_min}&y_max={y_max}&x_tick={dx}&y_tick={dy}&x_label_freq=5&y_label_freq=5&do_grid=0&do_grid=1&bold_labeled_lines=0&bold_labeled_lines=1&line_width=4&image_w=650&image_h=425"""
    iframe = f"""<p><iframe style="width: 850px; height: 495px; overflow: hidden;" src="{url}" width="1000" height="1000" scrolling="no">Iframes not supported</iframe></p>"""
    return iframe

def convert2gfx2(gfx_text1,gfx_text2,x_min=-10,x_max=10,y_min=-10,y_max=10,dx=1,dy=1,colors = [1,2]):
    gfx_text1 = str(urllib.parse.quote(gfx_text1))
    gfx_text2 = str(urllib.parse.quote(gfx_text2))
    c1,c2 = tuple(colors)
    url = f"""https://graphsketch.com/?eqn1_color={c1}&eqn1_eqn={gfx_text1}&eqn2_color={c2}&eqn2_eqn={gfx_text2}&eqn3_color=3&eqn3_eqn=&eqn4_color=4&eqn4_eqn=&eqn5_color=5&eqn5_eqn=&eqn6_color=6&eqn6_eqn=&x_min={x_min}&x_max={x_max}&y_min={y_min}&y_max={y_max}&x_tick={dx}&y_tick={dy}&x_label_freq=5&y_label_freq=5&do_grid=0&do_grid=1&bold_labeled_lines=0&bold_labeled_lines=1&line_width=4&image_w=650&image_h=425"""
    iframe = f"""<p><iframe style="width: 850px; height: 495px; overflow: hidden;" src="{url}" width="1000" height="1000" scrolling="no">Iframes not supported</iframe></p>"""
    return iframe

def convert2link(url,title = "link"):
    return f"""<a title="{title}" href="{url}" target="_blank" rel="noopener">url</a></p>"""


import requests
import json

def convert2listPythonStyle(lst,converter = lambda x:x):
    txt = []
    for l in lst:
        txt.append(converter(l))
    new_txt = " , ".join(txt)
    new_txt = "["+new_txt+"]"
    return new_txt

def clean_code(code):
    code = code.replace('\n','<br>')
    code = code.replace('/ta/',"&nbsp; &nbsp; &nbsp;&nbsp")
    return code

def convert2wiki_main_image(title):
    url = 'https://en.wikipedia.org/w/api.php'
    data = {
        'action' :'query',
        'format' : 'json',
        'formatversion' : 2,
        'prop' : 'pageimages|pageterms',
        'piprop' : 'original',
        'titles' : title
    }
    response = requests.get(url, data)
    json_data = json.loads(response.text)
    result = json_data['query']['pages'][0]['original']['source'] if len(json_data['query']['pages']) >0 else 'Not found'
    if result != "Not found":
        return convert2img(result)
    else:
        return None
    
def convert2HTMLList(tab):
    txt = "<ul>"
    for t in tab:
        txt += f"<li>{t}</li>"
    txt += "</ul>"
    return txt
        

def convert2sci(x,CS=3):
    CS = int(sorted([2,CS,10])[1])
    mantisse,puiss = f"""{x:.10e}""".split("e")
    mantisse=mantisse[:mantisse.index('.')+CS+1]
    multiply = 	u"\u00D7"
    if int(puiss)==0:
        return f"""{mantisse}"""
    else:
        return f"""{mantisse} {multiply} 10<sup>{int(puiss)}</sup>"""   

def convert2sci_unicode(x,CS=3):
    unic_exp = {'-':"⁻",'0':0x2070, '1':0x00B9, '2':0x00B2, '3':0x00B3, '4':0x2074, '5':0x2075, '6':0x2076, '7':0x2077, '8':0x2078, '9':0x2079}
    CS = int(sorted([2,CS,10])[1])
    if x == 0:
        return "0"
    mantisse,puiss = f"""{x:.10e}""".split("e")
    puiss = int(puiss)
    mantisse=mantisse[:mantisse.index('.')+CS+1]
    multiply = 	u"\u00D7"
    txt_puiss = str(puiss)
    print(txt_puiss)
    txt_expression = ""
    for t in txt_puiss:
        if t == "-":
            txt_expression += unic_exp[t]
        else: txt_expression += chr(unic_exp[t])
    if puiss==0:
        return f"""{mantisse}"""
    else:
        return f"""{mantisse} {multiply} 10{txt_expression}"""   

def shuffleList(*L):
    """
    Parameters
    ----------
    *L : tuple de listes

    Returns
    -------
    tuple de listes mélangé

    """
    list_zipped = list(zip(*L))
    random.shuffle(list_zipped)
    return zip(*list_zipped)

def convert2chemTopo(cid):
    """
    Parameters
    ----------
    cid : (int)

    Returns
    -------
    (str) url de l'image topologique de la molécule cid.

    """
    return f"""<p><img src="https://pubchem.ncbi.nlm.nih.gov/image/imgsrv.fcgi?cid={cid}&amp;t=l" alt="" width="250" height="250" /></p>"""

def convertDegreDec2DegMin(dd,opt=None,typ="GPS"):
    """
    params : 
        dd : deg decima Ex : 122.3658°
        opt = "Lat" | "Lon" | None
        typ = "GPS" | "dms" | "dms_str" | "dm" | "dm_str"
    Converti des degré décimaux Ex -19.4840833333° au format GPGGA
        return ('1929.0450', 'S')
    """
    is_positive = dd >= 0
    dd = abs(dd)
    minutes , seconds = divmod(dd*3600 , 60)
    degrees,minutes = divmod(minutes,60)
    minuts = minutes + seconds/60
    deg = abs(degrees)
    if is_positive:
        if opt == 'Lat':
            L = "N"
        else:
            L = "E"
    else:
        if opt == "Lat":
            L = "S"
        else:
            L = "W"
    if typ == "GPS":
        if opt is None:
            return f"{deg*100+minutes:.4f}"
        else:
            return f"{deg*100+minutes:.4f}",L
    elif typ == "dms":
        return degrees,minutes,seconds
    elif typ == "dms_str":
        return f"""{degrees:.0f}° {minutes:.0f} min {seconds:.2f} s """
    elif typ == "dm":
        return degrees , minuts
    elif typ == "dm_str":
        return f"{degrees:.0f}° {minuts:.4f} min"
        
def convert2coloredBox(color):
    return f"""<div style="background-color: {color} ; padding: 10px; border: 1px solid green;">"""

def convert2chemFormula(formula):
    return cp.Substance.from_formula(formula).unicode_name

def convert2chem3D(cid,width=300,height=200):
    return f"""<iframe style="width: {width}px; height: {height}px;" frameborder="0" src="https://embed.molview.org/v1/?mode=balls&cid={cid}&bg=white"></iframe>"""

def convertDataframe2XML(df,init="donnée"):
    def row_to_xml(row):
        xml = ["<xmp>",f'<{init}>']
        for i, col_name in enumerate(row.index):
            xml.append(f'<{col_name}>{row.iloc[i]}</{col_name}>')
        xml.append(f'</{init}>')
        xml.append("</xmp>")
        return '\n'.join(xml)
    res = '\n'.join(df.apply(row_to_xml, axis=1))
    res=res.replace("\n","<br />\n")
    res = res.replace("<br />","")
    return res

def convertDataframe2csv(df,sep=";"):
    ligne1 = sep.join(list(df.columns))+"\n"
    for idx in list(df.index):
        elems = []
        for col in df.columns:
            elems.append(str(df.at[idx,col]))
        ligne1 += sep.join(elems)+"\n"
    return ligne1.replace("\n","<br />\n")

def convertDataframe2json(df):
    result = df.to_json(orient="records")
    parsed = json.loads(result)
    res=json.dumps(parsed, indent=4,ensure_ascii=False)
    return res.replace("\n","<br />\n")

def converters(glob_var,conv):
    """

    Parameters
    ----------
    glob_var : globals()
    conv : dict
        Ex {"x":conv2url,...}

    Returns
    -------
    None.

    """
    assert isinstance(conv,dict),"conv doit être un dict"
    result = []
    for k,fnct in conv.items():
        a = glob_var[k]
        a = fnct(a)
        result.append(a)
    return tuple(result)

def alea(mmin,mmax,precision):
    p = 10**-precision
    return round(random.uniform(mmin/p,mmax/p))*p

def get_wiki_main_pic_url(title):
    response = requests.get('https://en.wikipedia.org/w/api.php',params={'action': 'query','prop':'pageimages','format':'json','piprop':'original','titles':title,'formatversion':2})
    try:
        return response.json()['query']['pages'][0]['original']['source']
    except:
        print(f"{title} url no found")
        return None
    
def linear(a,b,x_min=-1,x_max=10):
    """ a (flt) coef_dir
        b (flr) ordonnée à l'origine
        s'utilive avec convert2gfx
        convert2gfx(*linear(1.139,0,-1,200))
    """
    def get_dx(x):
        rs = [1,2,4,5]
        z,exp = tuple([float(k) for k in f"{x:.3e}".split("e")])
        dz = 99
        for r in rs:
            ddz = abs(z-r)
            if ddz<dz:
                dz = ddz
                rr = r
        return rr*10**exp
    x = np.linspace(x_min,x_max,25)
    y = a*x+b
    y_exp = f"{a}x+{b}"
    y_max = 1.2*max(y)
    y_min = min(y)-0.1*y_max
    dx = get_dx(abs(x_min-x_max)/20)
    dy = get_dx(abs(y_max-y_min)/20)
    if np.isclose(dy,0):
        dy = y_max/10
    y_min, y_max , x_min , x_max = y_min-2*dy , y_max+2*dy , x_min-2*dx , x_max+2*dx 
    return y_exp,x_min,x_max,y_min,y_max,dx,dy

def linear2(a0,b0,a1,b1,x_min=-1,x_max=10,colors = [1,2]):
    """
    Parameters
    ----------
    a0 : TYPE float
        coef dir droite 0.
    b0 : TYPE float
        ord orig droite 0.
    a1 : TYPE float
        coef dir droite 1.
    b1 : TYPE float
        ord orig droite 1.
    x_min : TYPE, optional
        DESCRIPTION. valeur min des absisses The default is -1.
    x_max : TYPE, optional
        DESCRIPTION. valeur max des absisses The default is 10.
    Returns
    -------
    tuple for be use with function cnvert2gfx2(*linear2) for draw 2 linear gfx with graphsketch
    Exemple
    convert2gfx2(*linear2(1,2,0,0,-0.1,2))

    """
    def get_dx(x):
        rs = [1,2,4,5]
        z,exp = tuple([float(k) for k in f"{x:.3e}".split("e")])
        dz = 99
        for r in rs:
            ddz = abs(z-r)
            if ddz<dz:
                dz = ddz
                rr = r
        return rr*10**exp
    dr0 = linear(a0,b0,x_min,x_max)
    dr1 = linear(a1,b1,x_min,x_max)
    #convert2gfx2(gfx_text1,gfx_text2,x_min=-10,x_max=10,y_min=-10,y_max=10,dx=1,dy=1,colors = [1,2]
    x_min = min(dr0[1],dr1[1])
    x_max = max(dr0[2],dr1[2])
    dx , dy = min(dr0[5],dr1[5]), min(dr0[6],dr1[6])
    y_min , y_max = min(dr0[3],dr1[3]) , max(dr0[4],dr1[4])
    if y_max/dy>20:
        dy = get_dx(y_max/10)
    return dr0[0],dr1[0],x_min,x_max,y_min,y_max,dx,dy,colors

def exponential(c0,c1,t_demi,x_min=-1,x_max=10):
    """ retourne une relation du type C0.exp(-tln(2)/tdemi)+C1
        s'utilise avec convert2gfx
        convert2gfx(*exponential(1.139,0,-1,200))
    """
    def get_dx(x):
        rs = [1,2,4,5]
        z,exp = tuple([float(k) for k in f"{x:.3e}".split("e")])
        dz = 99
        for r in rs:
            ddz = abs(z-r)
            if ddz<dz:
                dz = ddz
                rr = r
        return rr*10**exp
    x = np.linspace(x_min,x_max,25)
    y = c0*np.exp(-x*np.log(2)/t_demi)+c1
    y_exp = f"""{c0}exp(-x*ln(2)/{t_demi})+{c1}"""
    y_max = 1.2*max(y)
    y_min = -0.1*y_max
    dx = get_dx(abs(x_min-x_max)/20)
    dy = get_dx(abs(y_max-y_min)/20)
    if np.isclose(dy,0):
        dy = y_max/10
    y_min, y_max , x_min , x_max = y_min-2*dy , y_max+2*dy , x_min-2*dx , x_max+2*dx 
    return y_exp,x_min,x_max,y_min,y_max,dx,dy


def exponential2(c0,c1,t_demi1,b0,b1,t_demi2,x_min=-1,x_max=10,colors = [1,2]):
    """
    retourne 2 expressions c0.exp(-tln(2)/tdemi)+c1 (if avec b0 b1) 
    -------
    tuple for be use with function cnvert2gfx2(*linear2) for draw 2 linear gfx with graphsketch
    Exemple
    convert2gfx2(*exponential2(100,0,25,100,0,10))

    """
    def get_dx(x):
        rs = [1,2,4,5]
        z,exp = tuple([float(k) for k in f"{x:.3e}".split("e")])
        dz = 99
        for r in rs:
            ddz = abs(z-r)
            if ddz<dz:
                dz = ddz
                rr = r
        return rr*10**exp
    dr0 = exponential(c0,c1,t_demi1,x_min,x_max)
    dr1 = exponential(b0,b1,t_demi2,x_min,x_max)
    #convert2gfx2(gfx_text1,gfx_text2,x_min=-10,x_max=10,y_min=-10,y_max=10,dx=1,dy=1,colors = [1,2]
    x_min = min(dr0[1],dr1[1])
    x_max = max(dr0[2],dr1[2])
    dx , dy = min(dr0[5],dr1[5]), min(dr0[6],dr1[6])
    y_min , y_max = min(dr0[3],dr1[3]) , max(dr0[4],dr1[4])
    if y_max/dy>20:
        dy = get_dx(y_max/10)
    return dr0[0],dr1[0],x_min,x_max,y_min,y_max,dx,dy,colors

def wave(T,A=[1,2,3]):
    """ T (float): en ms
        A = [] amplitude des harmoniques
        s'utilive avec convert2gfx
        convert2gfx(*convert2gfx(*wave(1.139))
    """
    def get_dx(x):
        rs = [1,2,4,5]
        z,exp = tuple([float(k) for k in f"{x:.3e}".split("e")])
        dz = 99
        for r in rs:
            ddz = abs(z-r)
            if ddz<dz:
                dz = ddz
                rr = r
        return rr*10**exp
    t = np.linspace(0,(3+alea(0,1,1)/10)*T)
    y = np.zeros(len(t))
    y_exp = []
    for k,a in enumerate(A):
        w =2*(k+1)*np.pi/T
        y += a*np.sin(w*t)
        y_exp.append(f"{a}*sin({w}x)")
    y_exp = " + ".join(y_exp)
    y_max = 1.2*max(y)
    y_min = - y_max
    x_max = max(t)
    x_min = -T/4
    dx, dy = get_dx(T/10), get_dx(y_max/10)
    return y_exp,x_min,x_max,y_min,y_max,dx,dy
    
def convert_question_2_MC(html_text,typ="MC"):
    """Exemple de multichoix :
        |3     3_^12   15_3     15_12   12|
        delimitation par pipe
        bonne réponse précédé de ^
        separation des réponses _
    """
    new_text = ""
    f = open('testClozeMC.html','w')
    f.write(html_text)
    f.close()
    with open('testClozeMC.html', "r") as f:
        for line in f.readlines():
            if "|" in line:
                idx_i = line.index("|",0)
                idx_f = line.index("|",idx_i+1)
                text = line[idx_i+1:idx_f]
                a_reply = text.split('_')
                a_reply_final = []
                g_reply_final = []
                for rep in a_reply:
                    if "^" in rep:
                        a_reply_final.append(rep.replace("^",""))
                        g_reply_final.append(rep.replace("^",""))
                    else:
                        a_reply_final.append(rep)
                random.shuffle(a_reply_final)
                text_final = line[:idx_i]+multi_qr(g_reply_final,a_reply_final,typ=typ)+line[idx_f+1:]
                new_text += text_final
            else:
                new_text += line
    return new_text

def generate_xml(func,nb,cat=None,stype="random"):
    name = func.__name__
    cat = name if cat == None else cat
    questions = []
    if stype == "random":
        parameters = [random.randint(0,nb) for i in range(nb)]
    elif stype == "toto":
        parameters = range(nb)
    elif stype == "list":
        parameters = nb #nb est une liste
    for param in parameters:
        r = func(param)
        if r is not None:
            questions.append(func(param))
    file = open(name + ".xml","w",encoding="utf8")
    moodle_xml(name,questions,cloze_question,category = f'{cat}/', iostream = file)
    file.close()
    print("Questions were saved in " + name + ".xml, that can be imported into Moodle")
     
def num_q(x,p=0.001,sci = False,score=1,**d):
    """Return formatted string for numerical question, that can be included into
    cloze type moodle question.
    x ... correct answer, p ... precision, score ...... score
    d dict for unit {"g_unit":...,"a_unit":....,"score_unit":1}
    """
    g_unit = d.get("g_unit",None)
    a_unit = d.get("a_unit",None)
    score_unit = d.get("score_unit",1)
    if (g_unit != None) and (a_unit != None):
        txt_unit = multi_qr(g_unit,a_unit,score=score_unit)
    else:
        txt_unit = ""
    if sci:
        return "{"+f"{score}:NUMERICAL:={x:e}:{p}~{x:e}:{10*p}"+"} "+txt_unit
    else:
        return "{"+f"{score}:NUMERICAL:={x}:{p}~{x}:{10*p}"+"} "+txt_unit 

def str_q(x,score=1):
    return "{"+f"{score}:SHORTANSWER:="+"%s}" %(x)


def num_qr(x , precision=0.02 , score=1,**d):
    if x == 0:
        return num_q(0,1e-4,score=score,**d)
    else:
        return num_q(x,x*precision,score=score,**d)

def num_qr_list(xs,qs=[],unit="",precision=0.02,score=1):
    if isinstance(unit,str):
        unit = [unit]*len(xs)
    if qs == []:
        qs = ["  "]*len(xs)
    tab = [q+"  :"+num_qr(x,precision=precision,score=score)+f" {u}" for x,q,u in zip(xs,qs,unit)]
    return convert2HTMLList(tab)
    

def multi_qr(list_good_reply,list_reply,score = 1,typ="MC"):
    if isinstance(list_good_reply,str):
        list_good_reply = [list_good_reply]
    list_reply = list(set(list_good_reply+list_reply))
    resultat = []
    for rep in list_reply:
        if rep in list_good_reply:
            resultat.append((rep,100))
        else:
            resultat.append((rep,0))
    return multi_q(resultat,score=score,typ=typ)

def multi_q(answers,score = 1,typ="MC"):
    """Return formatted string for multichoice question, that can be included into
    cloze type moodle question.
    answers is a list of pairs (question, percent)
    """
    if typ == "MC":
        zboub = "MCS"
    elif typ == "MCV":
        zboub = "MCVS"
    else:
        zboub = "MCHS"
    q  = "{"+f"{score}:{zboub}:"
    for i in answers:
        q = q+f"~%{i[1]}%{i[0]}\n"
    q = q+"}"
    return q

def multichoice_question(answers, name):
    """
    XML string for moodle multiple choice question.
    answers ... a list of pairs (answer,fraction),
              fraction tells how much percent is worth the answer 
    name ... name of the question
    """
    q  = """<question type="multichoice">
    <name>
      <text> %s </text>
    </name>
    <questiontext format="html">
      <text><![CDATA[<p>Odkljukaj pravilne izjave!<br></p>]]></text>
    </questiontext>
    <generalfeedback format="html">
      <text></text>
    </generalfeedback>
    <defaultgrade>1.0000000</defaultgrade>
    <penalty>0.3333333</penalty>
    <hidden>0</hidden>
    <single>false</single>
    <shuffleanswers>true</shuffleanswers>
    <answernumbering>abc</answernumbering>
    <correctfeedback format="html">
      <text>Odgovor je pravilen.</text>
    </correctfeedback>
    <partiallycorrectfeedback format="html">
      <text>Odgovor je delno pravilen.</text>
    </partiallycorrectfeedback>
    <incorrectfeedback format="html">
      <text>Odgovor je nepravilen.</text>
    </incorrectfeedback>
    <shownumcorrect/>""" %name
    for answer in answers:
        q = q + """
        <answer fraction="%f" format="html">
        <text><![CDATA[%s]]></text>
          <feedback format="html">
            <text></text>
          </feedback>
        </answer>
        """ % (answer[1],answer[0])
    q = q + "</question>"
    return q

def cloze_question(tekst, name, feedback=''):
    """
    XML string for moodle cloze question.
    tekst ... string with question in cloze format. (see
         https://docs.moodle.org/29/en/Embedded_Answers_(Cloze)_question_type )
    name ... name of the question
    """
    q = """
  <question type="cloze">
    <name>
        <text>%s</text>
    </name>
    <questiontext format="html">
        <text><![CDATA[%s]]></text>
    </questiontext>
    <generalfeedback format="html">
      <text>%s</text>
    </generalfeedback>
    <penalty>0.2000000</penalty>
    <hidden>0</hidden>
  </question>
        """ % (name,tekst,feedback)
    return q

def moodle_xml(name, questions, template_fun, category = '',iostream=sys.stdout):
    """Write moodle xml file to be imported into Moodle.
    name ... name of the category, where the questions will be put
    questions ... list of strings containing xml code for the questions
    template_fun ... cloze_question or multichoice_question
    category ... optional upper category (default '')
    iostream ... file handle or other IOStream (default STDOUT)
    """
    iostream.write("""
<?xml version="1.0" encoding="UTF-8"?>
<quiz>
<!-- question: 0  -->
  <question type="category">
    <category>
    <text>$course$/""" + category + name + """</text>

    </category>
  </question>
    """)
    for i in range(len(questions)):
        iostream.write(template_fun(questions[i], name+str(i)))
    iostream.write("</quiz>")
    
class Jokers:
    def __init__(self,var,nb,stype,converters={}):
        stype = stype.replace(" ","").replace("_","")
        assert len(stype)==len(var)*nb,f"incorrect lenght stype lenght -> {len(stype)} | vars -> {len(var)*nb}"
        assert ("0" in stype or "1" in stype),f"stype {stype} ne doit contenir que 0 ou 1"
        self.var = var
        self.nb = nb
        self.stype = stype
        self.converters = converters
        listvar = []
        for v in var:
            for idx in range(1,nb+1):
                listvar.append(v+str(idx))
        self.list_var = listvar
        self.get_joker_dict()

    def get_joker_dict(self):
        """définit un dict des variables
        Exemple "{'e1': 0, 'e2': 0, 'e3': 0, 'r1': 0, 'r2': 1, 'r3': 1, 'p1': 0, 'p2': 1, 'p3': 1}"
        """
        self.dic_var = {v:int(s) for v,s in zip(self.list_var,list(self.stype))}
        return str(self.dic_var)
    
    def set_joker_value(self,var,func,*params):
        result = ""
        d = {}
        for v,typ in self.dic_var.items():
            if v[0] == var:
                d[v] = typ
        for v,typ in d.items():
            if v[0] == var and typ == 0:
                r = func(*params)
                result += f"{v}={r}\n"
        return result


        
    def set_joker_alpha_value_by_list(self,var,lst,fill_default=""):
        """retourne une chaine définissane les variables var1 utilisable avec un exec
        Ex : r1 = 'toto'
            r2 = 'tata'
        """
        result = ""
        if len(lst)<self.nb:
            lst += [fill_default for _ in range(self.nb-len(lst))]
        assert len(lst)>=self.nb,"La liste est trop petite par rapport aux variables"
        idx = 0
        d = {}
        for v,typ in self.dic_var.items():
            if v[0] == var:
                d[v] = typ
        for v,typ in d.items():
            if v[0] == var and typ == 0:
                fnct = self.converters.get(var,lambda x:x)
                r = fnct(lst[idx])
                if "'" in r:
                    result += f"""{v}="{r}"\n"""
                elif '"' in r:
                    result += f"""{v}='{r}'\n"""
                else:
                    result += f"""{v}='{r}'\n"""
            idx += 1
        return result
    
    def set_joker_numeric_value_by_list(self,var,lst,output_format=None,fill_default=""):
        result = ""
        if len(lst)<self.nb:
            lst += [fill_default for _ in range(self.nb-len(lst))]
        idx = 0
        d = {}
        for v,typ in self.dic_var.items():
            if v[0] == var:
                d[v] = typ
        for v,typ in d.items():
            if v[0] == var and typ == 0:
                fnct = self.converters.get(var,lambda x:x)
                if lst[idx] != fill_default:
                    r = fnct(lst[idx])
                    if output_format == None:
                        if isinstance(r,str):
                            result += f"""{v}="{r}"\n"""
                        else:
                            result += f"""{v}={r}\n"""
                    else:
                        toto = format(r,output_format)
                        result += f"{v}= '{toto}'\n"
                else:
                    result += f"{v}= '{fill_default}'\n"
            idx += 1
        return result
    
    def set_joker_numeric_value_by_function(self,var,func_exp):
        def sfunc(f_exp,var):
            jokers = self.var.replace(var[0],"")
            new_f_exp = f_exp
            for j in list(jokers):
                new_f_exp = new_f_exp.replace('_'+j[0],j[0]+v[1])
            return new_f_exp
        result = ""
        d = {}
        for v,typ in self.dic_var.items():
            if v[0] == var:
                d[v] = typ
        for v,typ in d.items():
            if v[0] == var and typ == 0:
                r = sfunc(func_exp,v)
                result += f"{v}={r}\n"
        return result
    
    def set_joker_multichoice_response_by_list(self,var,g_lst,a_lst,score=1,typ="MC"):
        idx, result , d = 0,"",{}
        for v,typs in self.dic_var.items():
            if v[0] == var:
                d[v] = typs
        for v,typs in d.items():
            if v[0] == var and typs == 1:
                g_reply = g_lst[idx]
                result += f"{v}='{g_reply}'\n"
                result += f"""{v} = multi_qr({v},{a_lst},score={score},typ="{typ}")\n"""
            idx += 1
        return result
        
    def set_joker_short_response_by_list(self,var,lst):
        idx = 0
        result = ""
        d = {}
        for v,typ in self.dic_var.items():
            if v[0] == var:
                d[v] = typ
        for v,typ in d.items():
            if v[0] == var and typ == 1:
                fnct = self.converters.get(var,lambda x:x)
                r = fnct(lst[idx])
                result += f"{v}='{r}'\n"
                result += f"{v} = str_q({v})\n"
            idx += 1
        return result
    
    def set_joker_numeric_response_by_function(self,var,func_exp,precision=0.01,fill_default=""):
        def sfunc(f_exp,var):
            jokers = self.var.replace(var[0],"")
            new_f_exp = f_exp
            for j in list(jokers):
                new_f_exp = new_f_exp.replace('_'+j[0],j[0]+v[1])
            return new_f_exp
        result = ""
        d = {}
        for v,typ in self.dic_var.items():
            if v[0] == var:
                d[v] = typ
        for v,typ in d.items():
            if v[0] == var and typ == 1:
                r = sfunc(func_exp,v)
                result += f"{v}={r}\n"
                result += f"{v} = num_qr({v},{precision})\n"
        return result
    
    def set_joker_numeric_response_by_list(self,var,lst,rtyp="num",precision=0.01,fill_default=""):
        result = ""
        if len(lst)<self.nb:
            lst += [fill_default for _ in range(self.nb-len(lst))]
        idx = 0
        d = {}
        for v,typ in self.dic_var.items():
            if v[0] == var:
                d[v] = typ
        for v,typ in d.items():
            if v[0] == var and typ == 1:
                r = lst[idx]
                if r != fill_default:
                    result += f"{v}={r}\n"
                    result += f"{v} = num_qr({v},{precision})\n"
                else:
                    result += f"{v}='{r}'\n"
            idx += 1
        return result
    
    def set_jokers_numeric_value_and_response_by_list(self,var,lst,precision=0.01,output_format=None):
        txt0 = self.set_joker_numeric_value_by_list(var,lst,output_format=output_format)
        txt1 = self.set_joker_numeric_response_by_list(var,lst,precision=precision)
        return txt0+txt1