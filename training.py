
# coding: utf-8

# In[22]:


import numpy as np
import pandas as pd
import keras
from keras.models import Sequential,model_from_json
from keras.layers import Dense


# In[23]:


json_file = open('model.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
model = model_from_json(loaded_model_json)
model.load_weights("model.h5")
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])


# In[24]:


ds=pd.read_csv('indian_liver_patient.csv')


# In[25]:


ds['Result']=ds['Result'].where(ds['Result']==1, 0)
mean1 = ds[ds['Result']==1]['Albumin_and_Globulin_Ratio'].mean()
mean0 = ds[ds['Result']==0]['Albumin_and_Globulin_Ratio'].mean()
def mean_ratio(cols):
    Ratio = cols[0]
    Result = cols[1]
    if pd.isnull(Ratio):
        if Result==1:
            return mean1
        else:
            return mean0
        
    else:return Ratio   
    
corr_ratio = ds[['Albumin_and_Globulin_Ratio','Result']].apply(mean_ratio,axis=1)    
ds['Albumin_and_Globulin_Ratio']=corr_ratio 


# In[26]:


gender_dummy = pd.get_dummies(ds['Gender'],drop_first=True)
ds = pd.concat([gender_dummy,ds],axis=1)
ds.drop('Gender',axis=1,inplace=True)


# In[27]:


x = ds.drop('Result',axis=1)


# In[28]:


from sklearn.preprocessing import StandardScaler
sc= StandardScaler()
sc.fit(x)


# In[36]:


from tkinter import *
root=Tk()
root.title("LIV-TOOL")
"""frame = Frame(root,bg="powder blue")
frame.pack()"""
age=StringVar()
gen=StringVar()
tot_bil=StringVar()
dir_bil=StringVar()
alk_phos=StringVar()
alam_amin=StringVar()
asp_amin=StringVar()
tot_pro=StringVar()
alb=StringVar()
alb_glo=StringVar()
res=StringVar()

a=""
b=""
c=""
d=""
e=""
f=""
g=""
h=""
i=""
j=""
k=""
r=""

def fun():
    global a,b,c,d,e,f,g,h,i,j,r,model,sc
    a=int(age.get())
    b=gen.get()
    c=float(tot_bil.get())
    d=float(dir_bil.get())
    e=int(alk_phos.get())
    f=int(alam_amin.get())
    g=int(asp_amin.get())
    h=float(tot_pro.get())
    i=float(alb.get())
    j=float(alb_glo.get())
    r=res.get()
    if r=="Patient":
        r=1
    else:
        r=0
    if b=='Female':
        b=0
    else:
        b=1
    x2=np.array([[b,a,c,d,e,f,g,h,i,j]])
    x2=sc.transform(x2)
    y=np.array([[r]])
    model.fit(x2, y, batch_size = 1, epochs =100)
   


def fun1():
    age.set("")
    gen.set("")
    tot_bil.set("")
    dir_bil.set("")
    alk_phos.set("")
    alam_amin.set("")
    asp_amin.set("")
    tot_pro.set("")
    alb.set("")
    alb_glo.set("")

        

 
    

    
label=Label(root,text="LIVER DISEASE TRAINER",font=("bold,Helvetica",30),fg="Steel blue")
label.grid(row=0,columnspan=5)

label1=Label(root,text="Age",font=("bold,Courier",25),fg="Steel blue")
entry1=Entry(root,textvariable=age,bd=10,insertwidth=4,font=15)
label2=Label(root,text="Gender",font=("bold,Courier",25),fg="Steel blue")
entry2=OptionMenu(root,gen,'Male','Female')
entry2.config(font=("bold,Courier",20),fg="Steel blue")
gen.set('Select')
label3=Label(root,text="Total_Bilirubin",font=("bold,Courier",25),fg="Steel blue")
entry3=Entry(root,textvariable=tot_bil,bd=10,insertwidth=4,font=15)
label4=Label(root,text="Direct_Bilirubin",font=("bold,Courier",25),fg="Steel blue")
entry4=Entry(root,textvariable=dir_bil,bd=10,insertwidth=4,font=15)
label5=Label(root,text="Alkaline_Phosphotase",font=("bold,Courier",25),fg="Steel blue")
entry5=Entry(root,textvariable=alk_phos,bd=10,insertwidth=4,font=15)
label6=Label(root,text="Alamine_Aminotransferase",font=("bold,Courier",25),fg="Steel blue")
entry6=Entry(root,textvariable=alam_amin,bd=10,insertwidth=4,font=15)
label7=Label(root,text="Aspartate_Aminotransferase",font=("bold,Courier",25),fg="Steel blue")
entry7=Entry(root,textvariable=asp_amin,bd=10,insertwidth=4,font=15)
label8=Label(root,text="Total_Protiens",font=("bold,Courier",25),fg="Steel blue")
entry8=Entry(root,textvariable=tot_pro,bd=10,insertwidth=4,font=15)
label9=Label(root,text="Albumin",font=("bold,Courier",25),fg="Steel blue")
entry9=Entry(root,textvariable=alb,bd=10,insertwidth=4,font=15)
label10=Label(root,text="Albumin_and_Globulin_Ratio",font=("bold,Courier",25),fg="Steel blue")
entry10=Entry(root,textvariable=alb_glo,bd=10,insertwidth=4,font=15)
label11=Label(root,text="Result",font=("bold,Courier",25),fg="Steel blue")
entry11=OptionMenu(root,res,'Patient','Not Patient')
entry11.config(font=("bold,Courier",20),fg="Steel blue")
res.set('Select')



label1.grid(row=1,sticky=W,pady=15,padx=10)
label2.grid(row=1,column=2,sticky=W)
entry1.grid(row=1,column=1,padx=20,ipady=10)
entry2.grid(row=1,column=3,padx=20,ipady=5,ipadx=30)

label3.grid(row=3,sticky=W,pady=15,padx=10)
label4.grid(row=3,column=2,sticky=W)
entry3.grid(row=3,column=1,padx=20,ipady=10)
entry4.grid(row=3,column=3,padx=20,ipady=10)

label5.grid(row=5,sticky=W,pady=15,padx=10)
label6.grid(row=5,column=2,sticky=W)
entry5.grid(row=5,column=1,padx=20,ipady=10)
entry6.grid(row=5,column=3,padx=20,ipady=10)

label7.grid(row=7,sticky=W,pady=15,padx=10)
label8.grid(row=7,column=2,sticky=W)
entry7.grid(row=7,column=1,padx=20,ipady=10)
entry8.grid(row=7,column=3,padx=20,ipady=10)

label9.grid(row=9,sticky=W,pady=15,padx=10)
label10.grid(row=9,column=2,sticky=W)
entry9.grid(row=9,column=1,padx=20,ipady=10)
entry10.grid(row=9,column=3,padx=20,ipady=10)

label11.grid(row=11,column=0,sticky=W,pady=15,padx=10)
entry11.grid(row=11,column=1,padx=20,ipady=5,ipadx=10)


b1 = Button(root,text="Train",command=fun,fg="white",bg="blue",font=("bold,Courier",25))
b1.grid(row=13,column=1,ipadx=20,ipady=5)
b2 = Button(root,text="Reset",command=fun1,fg="white",bg="grey",font=("bold,Courier",25))
b2.grid(row=13,column=2,ipadx=20,ipady=5)

while 1:
	root.update()
	if(a!=""):
	 break



"""
print(a)
print(b)
print(c)
print(d)
print(e)
print(f)
print(g)
print(h)
print(i)
print(j)
print(r)"""

root.mainloop()


# In[ ]:


rr

