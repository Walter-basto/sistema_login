from tkinter import *
from tkinter import ttk   # por causa do treeview
import  customtkinter as ctk
import sqlite3  # banco de dados
from tkinter import messagebox #caixa de dialogo
import webbrowser   # abrir pagina no navegador
from reportlab.pdfgen import canvas  # arquivo pdf
from reportlab.lib.pagesizes import letter, A4  # formato da folha 
from reportlab.pdfbase import pdfmetrics  
from reportlab.pdfbase.ttfonts import TTFont  # font da folha 
from reportlab.platypus import SimpleDocTemplate, Image




class  gerar_pdf_relatorios():
        #aparecera no site
       def printCliente(self):
           webbrowser.open("cliente.pdf")
        #  gerar pdf 
       def  gerar_relatorio_cliente(self):
           
           self.codigoRel=self.codigo_entry.get()
           self.nomeRel=self.nome_entry.get()
           self.telefoneRel=self.telefone_entry.get()
           self.cidadeRel=self.cidade_entry.get()
           self.emailRel=self.email_entry.get()
           self.assuntoRel=self.assunto_entry.get()
           #  gerar pdf 
           self.c=canvas.Canvas("cliente.pdf")
            #text do pdf
           self.c.setFont("Helvetica-Bold",24)
           self.c.drawString(200,790,'Ficha do cliente')#titulo
            #conteudo/representa
           self.c.setFont("Helvetica-Bold",10)
           self.c.drawString(50,700,'Codigo:') 
           self.c.drawString(50,670,'Nome:' )
           self.c.drawString(50,630,'Telefone:')
           self.c.drawString(50,600,'Cidade:')
           self.c.drawString(50,570,'Email:')
           self.c.drawString(50,530,'Assunto:')
           
           #conteudo/valores
           self.c.setFont("Helvetica",10)
           self.c.drawString(150,700,self.codigoRel) 
           self.c.drawString(150,670,self.nomeRel )
           self.c.drawString(150,630,self.telefoneRel)
           self.c.drawString(150,600,self.cidadeRel)
           self.c.drawString(150,570,self.emailRel)
           self.c.drawString(150,530,self.assuntoRel)
           
           
           
           self.c.showPage()
           self.c.save()
           self.printCliente()


class banco_dados():
    def limpa_tela(self):
        self.codigo_entry.delete(0,END)
        self.nome_entry.delete(0,END)
        self.telefone_entry.delete(0,END)
        self.cidade_entry.delete(0,END)
        self.email_entry.delete(0,END)
        self.assunto_entry.delete(0,END)
        
    def conecta_bd(self):
        self.conn=sqlite3.connect("clientes.db")
        self.cursor=self.conn.cursor()
        print("banco de dados conectado com sucesso")
         
    def  desconecta_bd(self):
        self.conn.close()
        print("banco de dados desconectado")
        
    def montarTabelas(self):
        self.conecta_bd()
        self.cursor.execute(""" 
            CREATE TABLE IF NOT EXISTS clientes(
                Cod INTEGER    PRIMARY KEY AUTOINCREMENT,
                Nome     CHAR(40) NOT NULL,
                Telefone     INTEGER(20) NOT NULL,
                Cidade       CHAR(40) NOT NULL,
                Email       CHAR(40) NOT NULL,
                Assunto      CHAR(40) NOT NULL
            )
        """)
        self.conn.commit()
        print("tabela criada com sucesso")
        self.desconecta_bd()     
    def data_entry(self):    
        self.codigo=self.codigo_entry.get()
        self.nome=self.nome_entry.get()
        self.telefone=self.telefone_entry.get()
        self.cidade=self.cidade_entry.get()
        self.email=self.email_entry.get()
        self.assunto=self.assunto_entry.get()
        
    def add_cliente(self):
        self.data_entry()
        self.conecta_bd()
        self.cursor.execute(""" INSERT INTO  clientes (Nome,Telefone,Cidade,Email,Assunto)
            VALUES(?,?,?,?,?)""",(self.nome,self.telefone,self.cidade,self.email,self.assunto))
        try:
            if (self.nome=='' or self.telefone=='' or self.cidade=='' or self.email=='' or self.assunto==''):
               messagebox.showerror(title="formulario",message="ERROR!!!, por faço preencher todo os campos")   
            else:
                self.conn.commit()
                messagebox.showinfo(title="formulario",message=f"parabens{self.nome}, inserido com sucesso")
                print(" inserido com sucesso")
                self.desconecta_bd()
                self.select_lista()# inserir os dados na treeview
                self.limpa_tela()
        except:
            messagebox.showerror(title="formulario",message="ERROR!!!,verifique se os campos estão corretos")
            self.desconecta_bd()
    def select_lista(self):
        self.listaCli.delete(*self.listaCli.get_children())
        self.conecta_bd()
        lista=self.cursor.execute(""" SELECT Cod, Nome,Telefone,Cidade,Email,Assunto FROM clientes
            ORDER BY Nome ASC;""")
        for i in lista:
            self.listaCli.insert("",END,value=i)
        self.desconecta_bd()
        
    def OnDoubleClick(self,event):
        self.limpa_tela()
        self.listaCli.selection()
        for n in self.listaCli.selection():
           col1,col2,col3,col4,col5,col6=self.listaCli.item(n,'values')
           self.codigo_entry.insert(END,col1)
           self.nome_entry.insert(END,col2)
           self.telefone_entry.insert(END,col3)
           self.cidade_entry.insert(END,col4)
           self.email_entry.insert(END,col5)
           self.assunto_entry.insert(END,col6)
    
    def deleta_cliente(self):
        self.data_entry()
        self.conecta_bd()
        self.cursor.execute("""DELETE FROM clientes WHERE Cod=?""",(self.codigo))
        self.conn.commit()
        self.desconecta_bd()
        self.select_lista()
        self.limpa_tela()
        
        
    def altera_cliente(self):
        self.data_entry()
        self.conecta_bd()
        self.cursor.execute("""UPDATE clientes SET Nome=?,Telefone=?,Cidade=?,Email=?,Assunto=?  WHERE Cod=?""",(self.nome,self.telefone,self.cidade,self.email,self.assunto,self.codigo))
        self.conn.commit()
        self.desconecta_bd()
        self.select_lista()
        self.limpa_tela()   



class Application(ctk.CTk,banco_dados,gerar_pdf_relatorios):
    def __init__(self):
        super().__init__()
        self.configuration()
        self.frames_da_tela()
        self.widgets_frame1()
        self.lista_frame2()
        self.montarTabelas()
        self.select_lista()
        self.altera_cliente()
        self.menus()
       
    def configuration(self):
        self.title("cadastro de cliente")    
        self.geometry("1280x450")
        self.configure(background="#303030")
        self.resizable(FALSE,FALSE)
        
    def frames_da_tela(self):
        self.frame1=ctk.CTkFrame(self,bg_color="#303030",width=315,height=450)
        self.frame1.place(x=0,y=0)

        self.frame2=ctk.CTkFrame(self,bg_color="green",width=965,height=450)
        self.frame2.place(x=315,y=0)
        
    def widgets_frame1(self):
        #codigo do botoes
        self.btn_limpar=ctk.CTkButton(self.frame1,text="Limpar",width=60,corner_radius=20,command=self.limpa_tela,fg_color="Red")
        self.btn_limpar.place(x=150,y=40)
        
        self.btn_buscar=ctk.CTkButton(self.frame1,text="Buscar",width=60,corner_radius=20,command=self.select_lista,fg_color="Blue")
        self.btn_buscar.place(x=225,y=40)
        
        self.btn_novo=ctk.CTkButton(self.frame1,text="Novo",width=65,corner_radius=20,command=self.add_cliente,fg_color="green")
        self.btn_novo.place(x=10,y=380)
        
        self.btn_alterar=ctk.CTkButton(self.frame1,text="Alterar",width=60,corner_radius=20,command=self.altera_cliente,fg_color="darkblue")
        self.btn_alterar.place(x=110,y=380)
        
        self.btn_apagar=ctk.CTkButton(self.frame1,text="Apagar",width=60,corner_radius=20,command=self.deleta_cliente,fg_color="darkred")
        self.btn_apagar.place(x=210,y=380)
        
        
        #codigo 
        self.lb_codigo=Label(self.frame1,text="Codigo",font=("Century Gothic bold",10),bg="#303030")
        self.lb_codigo.place(x=10,y=10)
        self.codigo_entry=ctk.CTkEntry(self.frame1,placeholder_text="não digite".upper(),font=("Century Gothic bold",14),width=130,corner_radius=20)
        self.codigo_entry.place(x=10,y=40)
        
        self.lb_nome=Label(self.frame1,text="Nome",font=("Century Gothic bold",10),bg="#303030")
        self.lb_nome.place(x=10,y=75)
        self.nome_entry=ctk.CTkEntry(self.frame1,placeholder_text="nome completo".upper(),font=("Century Gothic bold",14),width=300,corner_radius=20)
        self.nome_entry.place(x=10,y=95)
        
        self.lb_telefone=Label(self.frame1,text="Telefone",font=("Century Gothic bold",10),bg="#303030")
        self.lb_telefone.place(x=10,y=125)
        self.telefone_entry=ctk.CTkEntry(self.frame1,placeholder_text="somente numeros".upper(),font=("Century Gothic bold",14),width=300,corner_radius=20)
        self.telefone_entry.place(x=10,y=145)
        
        self.lb_cidade=Label(self.frame1,text="Cidade",font=("Century Gothic bold",10),bg="#303030")
        self.lb_cidade.place(x=10,y=185)
        self.cidade_entry=ctk.CTkEntry(self.frame1,placeholder_text="sem abreviação".upper(),font=("Century Gothic bold",14),width=300,corner_radius=20)
        self.cidade_entry.place(x=10,y=205)
        
        self.lb_email=Label(self.frame1,text="Email",font=("Century Gothic bold",10),bg="#303030")
        self.lb_email.place(x=10,y=240)
        self.email_entry=ctk.CTkEntry(self.frame1,placeholder_text="exemple@gmail.com".upper(),font=("Century Gothic bold",14),width=300,corner_radius=20)
        self.email_entry.place(x=10,y=260)
        
        self.lb_assunto=Label(self.frame1,text="Assunto",font=("Century Gothic bold",10),bg="#303030")
        self.lb_assunto.place(x=10,y=300)
        self.assunto_entry=ctk.CTkEntry(self.frame1,placeholder_text="comentario".upper(),font=("Century Gothic bold",14),width=300,corner_radius=20)
        self.assunto_entry.place(x=10,y=320)
        
    def lista_frame2(self):
       
        self.listaCli=ttk.Treeview(self.frame2,height=450,column=("col1","col2","col3","col4","col5","col6"))
        self.listaCli.place(x=0,y=0)
        self.listaCli.heading("#0",text="")
        self.listaCli.heading("#1",text="Codigo")
        self.listaCli.heading("#2",text="Nome")
        self.listaCli.heading("#3",text="Telefone")
        self.listaCli.heading("#4",text="Cidade")
        self.listaCli.heading("#5",text="Email")
        self.listaCli.heading("#6",text="Assunto")
            
        self.listaCli.column("#0",width=5)
        self.listaCli.column("#1",width=80)
        self.listaCli.column("#2",width=200)
        self.listaCli.column("#3",width=150)
        self.listaCli.column("#4",width=150)
        self.listaCli.column("#5",width=155)
        self.listaCli.column("#6",width=200)
        
            
        self.scrolLista=Scrollbar(self.frame2,orient="vertical")
        self.listaCli.configure(yscroll=self.scrolLista.set)
        self.scrolLista.place(x=940,y=0,width=25,height=450)
        self.listaCli.bind("<Double-1>",self.OnDoubleClick) 
          
    
    def Quit(self):
        self.destroy()
     
    def menus(self):
        
        menubar=Menu(self)
        self.config(menu=menubar)
        
        filemenu=Menu(self)
        menubar.add_cascade(label="opções",menu=filemenu)
        filemenu.add_command(label="sair",command=self.Quit)
        
        filemenu2=Menu(self)
        menubar.add_cascade(label="Relatorios",menu=filemenu2)
        filemenu2.add_command(label="limpar cliente",command=self.limpa_tela)
        filemenu2.add_command(label="ficha do cliente",command=self.gerar_relatorio_cliente)
         
    
    
    
    
if __name__=="__main__":
    app=Application()
    app.mainloop()
