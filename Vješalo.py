from tkinter import *
from tkinter.colorchooser import *
from tkinter.simpledialog import *
from sqlite3 import *
from random import *
import winsound
from time import *

class Vješalo(Frame):
    def __init__(self,root):
        super().__init__(root)
        self.R=root
        self.R.title('Vješalo')
        self.grid()
        self.R.resizable(FALSE,FALSE)
        self.brojac=0
        self.greske=0
        self.dobivene=int(open('Datoteke/Broj_dobivenih.txt','r').read())
        self.odigrane=int(open('Datoteke/Broj_partija.txt','r').read())
        self.iskoristeno=[]
        self.iskoristenostring=''
        self.rijec=self.odabir_rijeci()
        self.file=open('Datoteke/Tražena_riječ.txt','w')
        self.file.write(self.rijec)
        self.file.close()
        self.kreiraj()
        self.prvaboja()

    def kreiraj(self):
        self.vrijemepocetka=clock()
        self.vrijemedok=open('Datoteke/Vrijeme.txt','w')
        self.vrijemedok.write(str(self.vrijemepocetka)+'\n')
        
        for i in range(len(self.rijec)):
            Label(self,text='_').grid(row=1,column=i)

        self.C=Canvas(self,bg='white')
        self.C.grid(row=0,column=0,columnspan=len(self.rijec))
        self.C.create_line(300,300,300,600)
        self.E1=StringVar()
        
        Entry(self,textvariable=self.E1, width=10).grid(row=3,column=0, columnspan=len(self.rijec))
        self.R.bind('<Return>',self.provjeri)
       
        self.C.create_line(45+115,220,105+115,220, width='5', fill='sienna')
        self.C.create_line(75+115,220,75+115,70,width='5', fill='sienna')
        self.C.create_line(75+115,70, 120+115,70,width='5', fill='sienna')
        self.C.create_line(75+115,90, 90+115,70,width='5', fill='sienna')
        self.C.create_line(120+115,70, 120+115,90)
        
        self.vK=StringVar()
        Label(self.R,textvariable=self.vK).grid(row=0,column=5)
       
        self.slo=StringVar()
        Label(self, textvariable=self.slo).grid(row=2,column=0, columnspan=len(self.rijec))

        menu=Menu(self.R)
        
        dat=Menu(menu)
        dat.add_command(label='Nova igra',command=self.nova, accelerator='Ctrl+N')
        dat.add_command(label='Zatvori',command=self.kraj, accelerator='Esc')
        menu.add_cascade(label='Datoteka',menu=dat)

        ure=Menu(menu)
        ure.add_command(label='Boja',command=self.boja)
        menu.add_cascade(label='Uredi',menu=ure)

        pom=Menu(menu)
        pom.add_command(label='Kako igrati?', command=self.pomoc)
        menu.add_cascade(label='Pomoć',menu=pom)
        
        self.R.config(menu=menu)
        self.R.bind('<Control-n>',self.nova)
        self.R.bind('<Escape>',self.kraj)
        self.R.protocol("WM_DELETE_WINDOW", self.kraj)
        

    def pomoc(self):
        messagebox.showinfo('Pomoć', '''Cilj igre je pogoditi traženu riječ. \n Unesite slovo te ga provjerite pritiskom na tipku Enter.''')
        return
    
    def prvaboja(self):
        a=open('Datoteke/Boja.txt','r')
        self.boja=a.read()
        a.close()
        self.C.config(bg=self.boja)

    def odabir_rijeci(self):        
        conn=connect('rijeci.sqlite3')
        c=conn.cursor()
        
        upit='''SELECT Riječ
                FROM Riječi'''
        
        a=c.execute(upit)
        
        lista=[]
        for i in a:
            lista.append(i)
            
        br=randint(0,len(lista)-1)
        rijec=str(lista[br])
        self.odabir=''
        
        for i in rijec:
            if i in 'QWERTZUIOPŠĐŽĆČLKJHGFDSAMNBVCXY':
                self.odabir+=i
        return self.odabir
    
    def boja(self,e=None):
        self.boja=askcolor()[1]
        self.C.config(bg=self.boja)
        a=open('Datoteke/Boja.txt','w')
        a.write(self.boja)
        a.close()
        return
        
    def kraj(self,e=None):
        if messagebox.askyesno('Izvještaj','Želite li zatvoriti ovu igru?'):
            self.file_kraj()
            winsound.PlaySound(None, winsound.SND_ASYNC)
            self.R.destroy()
        return

    def nova(self,e=None):
        if messagebox.askyesno('Izvještaj','Želite li otvoriti novu igru?'):
                        a=open('Datoteke/Tražena_riječ.txt','w')
                        a.write('')
                        a.close()
                        self.R.destroy()
                        Vješalo(Tk())
                        winsound.PlaySound(None, winsound.SND_ASYNC)
                        
    def koordinate(self,e):
        self.vK.set('({},{})'.format(e.x,e.y))
        return
    
    def provjeri(self,e=None):        
        prije=0
        poslije=0
        slovo= self.E1.get().upper()
        
        if slovo in self.iskoristeno:
            messagebox.showinfo('Greška','Slovo je već iskorišteno')
            self.E1.set('')

        elif len(slovo)!=1:
            messagebox.showinfo('Greška','Moguće je unjeti samo jedan znak')
            self.E1.set('')
            
        else:
            self.iskoristeno+=[slovo]
            self.iskoristenostring+=slovo+' '
            self.slo.set(self.iskoristenostring)
            
            for i in range(len(self.rijec)):
                
                if slovo == self.rijec[i]:
                    Label(self,text= self.rijec[i]).grid(row=1,column=i)
                    self.brojac+=1
                    poslije=prije+1
                    
                else:
                    prije=0
                    
                if self.brojac==len(self.rijec):
                    self.dobivene+=1
                    b=open('Datoteke/Broj_dobivenih.txt','w')
                    b.write(str(self.dobivene))
                    b.close()
                    self.odigrane+=1
                    d=open('Datoteke/Broj_partija.txt','w')
                    d.write(str(self.odigrane))
                    d.close()
                    self.vrijemekraja=clock()
                    self.vrijemedok.write(str(self.vrijemekraja))
                    self.vrijemedok.close()
                    izvještaj=Iskocni_pobijeda(self.R)
                    
                    if messagebox.askyesno('Izvještaj','Želite li igrati ponovno?'):
                        self.file_nastavak()
                        self.R.destroy()
                        Vješalo(Tk())
                        winsound.PlaySound(None, winsound.SND_ASYNC)
                        
                    else:
                        winsound.PlaySound(None, winsound.SND_ASYNC)
                        self.file_kraj()
                        self.R.destroy()
                        
            if prije==poslije:
                self.greske+=1
                if self.greske==1:
                    a=self.C.create_oval(110+115,90,130+115,110)
                    a
                elif self.greske==2:
                    b=self.C.create_line(120+115,110,120+115,160)
                    b
                elif self.greske==3:
                    c=self.C.create_line(120+115,120,140+115,145)
                    c
                elif self.greske==4:
                    d=self.C.create_line(120+115,120,100+115,145)
                    d
                elif self.greske==5:
                    e=self.C.create_line(120+115,160,140+115,185)
                    e
                elif self.greske==6:
                    f=self.C.create_line(120+115,160,100+115,185)
                    
                if self.greske==6:
                    self.odigrane+=1
                    d=open('Datoteke/Broj_partija.txt','w')
                    d.write(str(self.odigrane))
                    d.close()

                    izvještaj=Iskocni_gubitak(self.R)
                    
                    if messagebox.askyesno('Izvještaj','Želite li igrati ponovno?'):
                        self.file_nastavak()
                        self.R.destroy()
                        Vješalo(Tk())
                        winsound.PlaySound(None, winsound.SND_ASYNC)
                        
                    else:
                        self.file_kraj()
                        winsound.PlaySound(None, winsound.SND_ASYNC)
                        self.R.destroy()
                     
                self.E1.set('')
                return
            
            self.E1.set('')
        return

    def file_kraj(self):
        a=open('Datoteke/Tražena_riječ.txt','w')
        a.write('')
        a.close()
        b=open('Datoteke/Boja.txt','w')
        b.write('white')
        b.close()
        c=open('Datoteke/Vrijeme.txt','w')
        c.write('')
        c.close()
        d=open('Datoteke/Broj_dobivenih.txt','w')
        d.write('0')
        d.close()
        e=open('Datoteke/Broj_partija.txt','w')
        e.write('0')
        e.close()
        return

    def file_nastavak(self):
        a=open('Datoteke/Tražena_riječ.txt','w')
        a.write('')
        a.close()
        c=open('Datoteke/Vrijeme.txt','w')
        c.write('')
        c.close()
        return
        
    


class Iskocni_pobijeda(Dialog):
    def body(self, root):
        lista_slika=['Slike/Vatromet.gif','Slike/Veseli.gif']
        lista_muzike=['Muzika/Eye.wav','Muzika/Pljesak.wav','Muzika/Final.wav']

        pjesma=lista_muzike[randint(0,len(lista_muzike)-1)]
        winsound.PlaySound(pjesma, winsound.SND_ASYNC )

        self.R = root
        self.title('Izvještaj')
        a=open('Datoteke/Tražena_riječ.txt','r')
        rijec=a.read()
        a.close()
        Label(self.R, text='Čestitamo, pogodili ste traženu riječ: ' + rijec ).grid(row=0,column=0)
        
        self.L=Label(self)
        self.L.pack()
        slika=PhotoImage(file=lista_slika[randint(0,len(lista_slika)-1)])
        self.L['image']=slika
        self.L.image=slika

        vrijemedok=open('Datoteke/Vrijeme.txt','r')
        pocetak=float(vrijemedok.readline().strip())
        kraj=float(vrijemedok.readline())
        vrijemedok.close()
        vrijeme=int(kraj-pocetak)

        Label(self.R, text = 'Vaše vrijeme za rješavanje riječi: ' +str(vrijeme)+' sekundi').grid(row=2,column=0)

        self.dobivene=int(open('Datoteke/Broj_dobivenih.txt','r').read())
        self.odigrane=int(open('Datoteke/Broj_partija.txt','r').read())
        self.izgubljene=self.odigrane-self.dobivene

        Label(self.R, text= 'Broj odigranih: ' + str(self.odigrane)).grid(row=3,column=0)
        Label(self.R, text= 'Broj dobivenih: ' + str(self.dobivene)).grid(row=4,column=0)  
        return
    
    def apply(self):
        return
    
class Iskocni_gubitak(Dialog):
    def body(self, root):
        lista_slika=['Slike/Tužni.gif','Slike/Objeseni.gif','Slike/Smrt.gif']
        lista_muzike=['Muzika/Nothing.wav','Muzika/Serenity.wav', 'Muzika/Gubitak.wav','Muzika/Sad.wav']
        pjesma=lista_muzike[randint(0,len(lista_muzike)-1)]
        winsound.PlaySound(pjesma, winsound.SND_ASYNC )
        self.R = root
        self.title('Izvještaj')
        a=open('Datoteke/Tražena_riječ.txt','r')
        rijec=a.read()
        a.close()

        Label(self.R, text='Nažalost, izubili ste.').grid(row=0,column=0)
        Label(self.R, text='Tražena riječ bila je: ' + rijec).grid(row=1,column=0)
        self.L=Label(self)
        self.L.pack()
        slika=PhotoImage(file=lista_slika[randint(0,len(lista_slika)-1)])
        self.L['image']=slika
        self.L.image=slika
        self.dobivene=int(open('Datoteke/Broj_dobivenih.txt','r').read())
        self.odigrane=int(open('Datoteke/Broj_partija.txt','r').read())
        self.izgubljene=self.odigrane-self.dobivene

        Label(self.R, text= 'Broj odigranih: ' + str(self.odigrane)).grid(row=3,column=0)
        Label(self.R, text= 'Broj dobivenih: ' + str(self.dobivene)).grid(row=4,column=0)
        return

    def apply(self):
        return

    
v=Vješalo(Tk())
