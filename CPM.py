from kivy.config import Config
Config.set('graphics','width','500')
Config.set('graphics','height','300')
Config.set('graphics', 'resizable', 0)
Config.set('graphics', 'borderless', 1)
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.uix.filechooser import FileChooserIconView
from kivy.core.window import Window
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from flask import Flask,render_template
import random
import pandas as pd
import math
import matplotlib.pyplot as plt
import webbrowser
n=''
def levels(l):
    level1,nodes=[],[]
    for i in l:
        nodes.append(i[0])
        if i[2]==[]:
            level1.append(i[0])
    levels=[level1]
    last=level1
    visited=[]
    visited.extend(level1)
    while True:
        if len(visited)==len(nodes):
            break
        level=[]
        for k in last:
            for j in l:
                parents=j[2]
                max=0
                maxp=''
                for i in parents:
                    if nodes.index(i)>=max:
                        maxp=i
                if maxp==k:
                    level.append(j[0])
        levels.append(level)
        last=level
        visited.extend(level)
    return(levels)
def read(s):
    d=pd.read_csv(s)
    parents,parent=list(d['Parents']),[]
    for i in parents:
        if ',' in str(i):
            i=list(i)
            parent.append(i)
        elif str(i)=='nan':
            parent.append([])
        else:
            parent.append(list(str(i)))
    parents=[]
    for i in parent:
        x=[]
        for j in i:
            if j!=',':
                x.append(j)
        parents.append(x)
    labels,label=list(d['Labels']),[]
    for i in labels:
        label.append(i)
    descs,desc=list(d['Description']),[]
    for i in descs:
        desc.append(i)
    durations,duration=list(d['Duration']),[]
    for i in durations:
        i=int(i)
        duration.append(i)
    length=len(duration)
    l=[]
    for i in range(length):
        l.append([label[i],duration[i],parents[i],desc[i]])
    return l
def answer(l):
    child={}
    for i in l:
        child[i[0]]=[]
    for i in l:
        for k in l:
            if i[0] in k[2]:
                child[i[0]].append(k[0])
    l1,l2,l3={},{},{}
    for i in l:
        d={}
        d['Label']=i[0]
        d['duration']=i[1]
        d['Description']=i[3]
        if i[2]!=[]:
            max=0
            for k in i[2]:
                if l1[k]['earliest_finish']>=max:
                    max=l1[k]['earliest_finish']
            d['earliest_start']=max
        else:
            d['earliest_start']=0
        d['earliest_finish']=d['earliest_start']+d['duration']
        l1[i[0]]=d
    last=l1[l[len(l)-1][0]]['earliest_start']
    l=l[::-1]
    for i in l:
        d={}
        d['Label']=i[0]
        d['duration']=i[1]
        d['Description']=i[3]
        if child[i[0]]!=[]:
            min=(float('inf'))
            for k in child[i[0]]:
                if l2[k]['latest_start']<=min:
                    min=l2[k]['latest_start']
            d['latest_finish']=min
            d['latest_start']=d['latest_finish']-d['duration']
        else:
            d['latest_start']=last
            d['latest_finish']=d['latest_start']+d['duration']
        l2[i[0]]=d
    for k in l2.keys():
            d={}
            d['Label']=l2[k]['Label']
            d['duration']=l2[k]['duration']
            d['earliest_start']=l1[k]['earliest_start']
            d['earliest_finish']=l1[k]['earliest_finish']
            d['latest_start']=l2[k]['latest_start']
            d['latest_finish']=l2[k]['latest_finish']
            d['Float']=abs(d['latest_finish']-d['earliest_finish'])
            d['Span']=abs(d['latest_finish']-d['earliest_start'])
            d['Description']=l2[k]['Description']
            l3[k]=d
    return l3
def graph(n):
    colors=['blue','orange','green','purple','maroon','navy','teal','fuchsia','grey','lime','aqua']
    l=read(n)
    x,y=6,5
    yd=[]
    d={}
    last=''
    final=answer(l)
    critical=[]
    for k in final.keys():
        if final[k]['Float']==0:
            critical.append(final[k]['Label'])
    used=[]
    l=levels(l)
    c=2
    c1=0
    d,d1={},{}
    last=l[0][0]
    for i in l:
        c1+=5
        max=0
        for k in i:
            body=final[k]
            text=[k,body['earliest_finish']-body['earliest_start'],body['earliest_start'],body['earliest_finish'],body['latest_start'],body['latest_finish'],abs(body['latest_start']-body['earliest_finish']),abs(body['latest_finish']-body['earliest_finish'])]
            yd.append(y)
            if (body['earliest_finish']-body['earliest_start']>=max):
                max=body['earliest_finish']-body['earliest_start']
            d1[k]=text
            y+=2
        x,y=x+max,y+2
    yd=yd[::-1]
    x,y=6,yd[0]
    for i in l:
        c1+=5
        max=0
        for k in i:
            body=final[k]
            text=[k,body['earliest_finish']-body['earliest_start'],body['earliest_start'],body['earliest_finish'],body['latest_start'],body['latest_finish'],abs(body['latest_start']-body['earliest_finish']),abs(body['latest_finish']-body['earliest_finish'])]
            plt.plot([x,x+body['earliest_finish']-body['earliest_start']],[y,y],lw=10)
            plt.annotate(k,xy=(x,y))
            if (body['earliest_finish']-body['earliest_start']>=max):
                max=body['earliest_finish']-body['earliest_start']
            d1[k]=text
            y-=2
        x,y=x+max+1,y-2
def find(n):
    colors=['blue','orange','green','purple','maroon','navy','teal','fuchsia','grey','lime','aqua']
    l=read(n)
    x,y=60,50
    d={}
    last=''
    final=answer(l)
    critical=[]
    for k in final.keys():
        if final[k]['Float']==0:
            critical.append(final[k]['Label'])
    used=[]
    c=0
    l=levels(l)
    c=200
    c1=0
    d,d1={},{}
    last=l[0][0]
    for i in l:
        c1+=50
        for k in i:
            for j in colors:
                if j not in used:
                    color=j
                    break
                elif(len(used)==len(colors)):
                    used=[]
                    color=colors[1]
            body=final[k]
            text=[k,body['earliest_finish']-body['earliest_start'],body['earliest_start'],body['earliest_finish'],body['latest_start'],body['latest_finish'],abs(body['latest_start']-body['earliest_finish']),abs(body['latest_finish']-body['earliest_finish'])]
            d[k]=[x,y,text,body['Description']]
            d1[k]=text
            y+=200
            used.append(color)
            last=d[k]
        x,y=x+c,150+c1
    #For Lines:
    l=read(n)
    l1=[]
    l2=[]
    for i in l:
        for j in i[2]:
            x1,y1,x2,y2=d[i[0]][0],d[i[0]][1],d[j][0],d[j][1]
            angle = math.atan2(y2 - y1, x2 - x1) * (180 / math.pi)
            length = math.sqrt((x2 - x1) * (x2 - x1)  + (y2 - y1) * (y2 - y1))
            l1.append([x1,y1,x2,y2,angle,length])
    #For Critical Path
    for i in critical[1:]:
        x1,y1,x2,y2=d[i][0],d[i][1],last[0],last[1]
        angle = math.atan2(y2 - y1, x2 - x1) * (180 / math.pi)
        length = math.sqrt((x2 - x1) * (x2 - x1)  + (y2 - y1) * (y2 - y1))
        l2.append([x1,y1,x2,y2,angle,length])
        last=[x1,y1]
    return(l1,d,l2,final)
class MyButton(Button):
    pass
class MyL(FloatLayout):
    label=Label(text='Choose a CSV File!!',pos=(0,-50))
    def __init__(self,**kwargs):
        super(MyL,self).__init__(**kwargs)
        Window.bind(on_request_close=self.exit_app)
        self.cb=MyButton(text="",on_press=self.sfc,size_hint=(None,None),size=(100,130),pos=(200,100),font_size=20,background_normal='CSV.jpg')
        self.add_widget(self.cb)
        self.add_widget(MyL.label)
    def sfc(self,instance):
        fc=FileChooserIconView()
        popup=Popup(title="Choose a csv file!!",content=fc,size_hint=(0.9,0.9))
        def selected_file(self,selection):
            popup.dismiss()
            select=selection[0]
            select1=list(select)[::-1]
            if(select1[:3]==['v','s','c']):
                global n
                n=select
                Window.close()
            else:
                #self.parent.parent.parent.parent.add_widget(MyL.label)
                MyL.label.text='Please choose a CSV File only!!'
        fc.bind(selection=selected_file)
        popup.open()
    def exit_app(self,instance):
        App.get_running_app().stop()
        Window.close()
class My(App):
    def build(self):
        return MyL()
if __name__=='__main__':
    My().run()
    graph(n)
    plt.show()
    app=Flask(__name__)
    @app.route('/cpm')
    def cpm():
        l1,d,l2,final=find(n)
        return render_template("CPM.html",d=d,l1=l1,l2=l2)
    @app.route('/table')
    def table():
        l1,d,l2,final=find(n)
        final1=[]
        for i in final.keys():
            l=[final[i]['Label'],final[i]['duration'],final[i]['earliest_start'],final[i]['earliest_finish'],final[i]['latest_start'],final[i]['latest_finish'],final[i]['Float'],final[i]['Span']]
            final1.append(l)
        final1=final1[::-1]
        return render_template("table.html",final=final1)
    print('You can view your cpm at http://127.0.0.1:5000/cpm!!')
    print('You can view your table at http://127.0.0.1:5000/table!!')
    app.run(port=5000)
