import tkinter as tk
import sqlite3
from tkinter import ttk, messagebox


FontBaslik = ("Verdana", 32)
FontNormal = ("Arial", 12)

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Kayıt Sistemi")
        self.geometry("1000x440-5+10")
        self.resizable(False,False)
        
        self.varIsim = tk.StringVar()
        self.varNumara = tk.StringVar()
        self.varFoto = tk.StringVar()
        self.varNot = tk.StringVar()
        
        self.vtbaglan()
        self.frameler()
        
    def frameler(self): 
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=2)
        self.columnconfigure(2, weight=3)
        self.columnconfigure(3, weight=4)
        
        
        baslikFrame = BaslikFrame(self, column=0, row=0)
        arabulFrame = ArabulFrame(self, column=2, row=0)
        fotoFrame =  FotoFrame(self, column=3, row=0)
        self.menuFrame = MenuFrame(self, column=0, row=2)
        veriFrame = VeriFrame(self, column=0, row=1)
        self.listFrame = ListFrame(self, column=1, row=2)
        self.listFrame.listele()
        
        
    def vtbaglan(self):
        self.baglan = sqlite3.connect("rehber.db")
        self.cursor = self.baglan.cursor()
        sql =  """
        create table if not exists 'defter' (
        id integer primary key autoincrement not null,
        isim text,
        numara text,
        foto text,
        nott text)
        """
        self.cursor.execute(sql)
        self.baglan.commit()
        

        
    
class BaslikFrame(tk.Frame):
    def __init__(self, sahip, column, row):
        tk.Frame.__init__(self, sahip, bg="lightblue")
        self.configure(relief=tk.RAISED, border=2)
        tk.Label(self, text="Kayıt Sistemi", font=FontBaslik, bg="lightblue").pack()
        self.grid(column=column, row=row, columnspan=2, sticky="NEWS", padx=5, pady=5)

        

class ArabulFrame(tk.Frame):
    def __init__(self, sahip, column, row):
        
        super().__init__(sahip)
        self.configure(relief=tk.GROOVE, border=2)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=2)
        
        isim = tk.Label(self, text="İsim Ara", font=FontNormal)
        isim.grid(column=0, row=0)
        
        tel = tk.Label(self, text="Telefon Ara", font=FontNormal)
        tel.grid(column=0, row=1)
        
        araİsim = tk.Entry(self, bg="bisque" )
        araİsim.grid(column=1, row=0, sticky="NEWS")
        
        araTel = tk.Entry(self, bg="bisque" )
        araTel.grid(column=1, row=1, sticky="NEWS")
        
        self.grid(column=column, row=row, sticky="NEWS", padx=5, pady=5)
        
class FotoFrame(tk.Frame):
    def __init__(self, sahip, column, row):
        super().__init__(sahip)
        self.configure(relief=tk.GROOVE)
        
        self.bos_foto = tk.PhotoImage(file="./images/ornek.png")
        
        self.foto = tk.Label(self, image=self.bos_foto)
        self.foto["image"] = self.bos_foto
        self.foto.pack(fill=tk.BOTH, expand=True)
        
        self.grid(column=column, row=row, rowspan=2, sticky="NEWS", padx=5, pady=5)
        

class MenuFrame(tk.Frame):
    def __init__(self, sahip, column, row):
        super().__init__(sahip)
        self.sahip = sahip
        self.duzenelenenID = 0
        self.configure(relief=tk.GROOVE, border=2)
        self.columnconfigure(0, weight=1)
        
        for i in range(0,4):
            self.rowconfigure(i, weight=1) 
        
        btn_kayit_ekle = tk.Button(self, text="Kaydet", command=self.kaydet)
        btn_kayit_ekle.grid(column=0, row=0, sticky="NEWS")
        
        btn_kayit_sil = tk.Button(self, text="Kayıt Sil ", command=self.sil)
        btn_kayit_sil.grid(column=0, row=1, sticky="NEWS")
        
        btn_duzenle = tk.Button(self, text="Düzenle ", command=self.kayit_güncelle)
        btn_duzenle.grid(column=0, row=2, sticky="NEWS")


        
        self.grid(column=column, row=row, sticky="NEWS")
        
        btn_sirala = tk.Button(self, text="İsme Göre Sırala ")
        btn_sirala.grid(column=0, row=3, sticky="NEWS")

        btn_cik = tk.Button(self, text="Çıkış", bg='lightcoral', command=quit)
        btn_cik.grid(column=0, row=4, sticky="NEWS")
        
        self.grid(column=column, row=row, rowspan=2, sticky="NEWS", padx=5, pady=5)
        
        
    def kaydet(self):
        sql = "insert into defter (isim, numara, foto, nott)" \
              "values('{}','{}','{}','{}')".format(self.sahip.varIsim.get(),
                                                   self.sahip.varNumara.get(),
                                                   self.sahip.varFoto.get(),
                                                   self.sahip.varNot.get(),)
        self.sahip.cursor.execute(sql)
        self.sahip.baglan.commit()
        self.sahip.listFrame.listele()
        
    def sil(self):
        yanit = messagebox.askquestion('Rehber Uygulaması',
                'Seçili Kayıtları Silmek İstediğinizden Emin Misiniz?',
                icon="warning")
        if yanit == "yes":
            for sil_id in self.sahip.listFrame.tv.selection():
                # print(self.sahip.listFrame.tv.item(sil_id))
                sql = "delete from defter where id={}".format(
                    self.sahip.listFrame.tv.item(sil_id)['values'][0])
                self.sahip.cursor.execute(sql)
            self.sahip.baglan.commit()
            self.sahip.listFrame.tv.delete(*self.sahip.listFrame.tv.selection())
            
    def kayit_aktar(self, widget):
        al = self.sahip.listFrame.tv.selection()[0]
        item = self.sahip.listFrame.tv.item(al)
        self.duzenlenenID = item['values'][0]
        self.sahip.varIsim.set(item['values'][1])
        self.sahip.varNumara.set(item['values'][2])
        self.sahip.varFoto.set(item['values'][3])
        self.sahip.varNot.set(item['values'][4])
        
    def kayit_güncelle(self):
        if self.duzenlenenID != 0:
            sql = "update defter set isim='{}', numara='{}', foto='{}', nott='{}' where id={}".format(
                self.sahip.varIsim.get(),
                self.sahip.varNumara.get(),
                self.sahip.varFoto.get(),
                self.sahip.varNot.get(),
                self.duzenlenenID)
        print(sql)
        self.sahip.cursor.execute(sql)
        self.sahip.baglan.commit()
        self.sahip.listFrame.listele()
        self.duzenlenenID = 0
        self.sahip.varIsim.set("")
        self.sahip.varNumara.set("")
        self.sahip.varFoto.set("")
        self.sahip.varNot.set("")

        
        
class VeriFrame(tk.Frame):
    def __init__(self, sahip, column, row):
        super().__init__(sahip)
        self.configure(relief=tk.GROOVE, border=2)
        
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=2)
        self.columnconfigure(2, weight=1)
        
        
        isim = tk.Label(self, text="Adı Soyadı", font=FontNormal)
        isim.grid(column=0, row=0, sticky="NW")
        
        telefon = tk.Label(self, text="Telefon Numarası", font=FontNormal)
        telefon.grid(column=0, row=1, sticky="NW")
    
        foto = tk.Label(self, text="Fotoğraf", font=FontNormal)
        foto.grid(column=0, row=2, sticky="NW")
        
        nott = tk.Label(self, text="Açıklama", font=FontNormal)
        nott.grid(column=0, row=3, sticky="NW")
        
        
        eIsim = tk.Entry(self, textvariable=sahip.varIsim)
        eIsim.grid(column=1, row=0, columnspan=2, sticky="NEWS")
        
        eTelefon = tk.Entry(self, textvariable=sahip.varNumara)
        eTelefon.grid(column=1, row=1, columnspan=2, sticky="NEWS")
        
        eFoto = tk.Entry(self, textvariable=sahip.varFoto)
        eFoto.grid(column=1, row=2, sticky="NEWS")
        
        eNott = tk.Entry(self, textvariable=sahip.varNot)
        eNott.grid(column=1, row=3, columnspan=2, sticky="NEWS")
        
        gozat = tk.Button(self, text="Gözat")
        gozat.grid(row=2, column=2, sticky="NEWS")
        
        self.grid(column=column, row=row, sticky="NEWS", columnspan=3, padx=5, pady=5)
        
class ListFrame(tk.Frame):
    def __init__(self, sahip, column, row):
        super().__init__(sahip)
        self.sahip = sahip
        self.columnconfigure(0, weight=1)
        self.configure(relief=tk.GROOVE, border=2)
        
        self.tv = ttk.Treeview(self, show="headings")
        ybar = tk.Scrollbar(self, orient=tk.VERTICAL, command=self.tv.yview)
        self.tv.configure(yscroll=ybar.set)
        self.tv.grid(column=0, row=0, sticky="NEWS")
        self.tv['column'] = ('id', 'isim', 'telefon', 'foto', 'not') 
        
        self.tv.column('#0', width=0, stretch=tk.NO)
        self.tv.column('id', width=80, anchor=tk.E)
        self.tv.column('isim', anchor=tk.CENTER)
        self.tv.column('telefon', width=100, anchor=tk.W)
        self.tv.column('foto', width=100, anchor=tk.W)
        self.tv.column('not', width=100,anchor=tk.W)
        
        self.tv.heading('#0', text='', anchor=tk.CENTER)
        self.tv.heading('id', text='ID', anchor=tk.CENTER)
        self.tv.heading('isim', text='Adı Soyadı', anchor=tk.CENTER)
        self.tv.heading('telefon', text='Telefon', anchor=tk.CENTER)
        self.tv.heading('foto', text='Fotoğraf', anchor=tk.CENTER)
        self.tv.heading('not', text='Açıklama', anchor=tk.CENTER)
        
        self.tv.bind("<Double-1>", self.sahip.menuFrame.kayit_aktar)
        
        self.grid(column=column, row=row, columnspan=4, sticky="NEWS", padx=5, pady=5)
        
    
    def listele(self):
        self.tv.delete(*self.tv.get_children())
        sql = "select * from defter"
        self.sahip.cursor.execute(sql)  
        
        veriler = self.sahip.cursor.fetchall()
        for veri in veriler :
            self.tv.insert('', 'end',
                           values=(veri[0], veri[1], veri[2], 
                                   veri[3], veri[4],))


if __name__== '__main__':
    pencere = App()
    pencere.mainloop()
    
