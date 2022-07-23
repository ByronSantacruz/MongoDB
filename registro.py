#Librerias
from tkinter import*
from tkinter import ttk
from tkinter import messagebox
import pymongo

#Coneccion con mongodb
MONGO_HOST="localhost"
MONGO_PUERTO="27017"
MONGO_TIEMPO_FUERA=1000
MONGO_URI="mongodb://"+MONGO_HOST+":"+MONGO_PUERTO+"/"

#Conecion con la base no relacional de mongo
MONGO_BASEDATOS="registros"
MONGO_COLECCION="estudiantes"
cliente=pymongo.MongoClient(MONGO_URI,serverSelectionTimeoutMS=MONGO_TIEMPO_FUERA)
baseDatos=cliente[MONGO_BASEDATOS]
coleccion=baseDatos[MONGO_COLECCION]
ID_ALUMNO=""

#Metodo de mostrar datos
def mostrarDatos(id="",nombre="",nota1="",nota2=""):
    objectoBuscar={}
    if len(id)!=0:
        objectoBuscar["_id"]=id
    if len(nombre)!=0:
        objectoBuscar["Nombre"]=nombre
    if len(nota1)!=0:
        objectoBuscar["Nota 1"]=nota1
    if len(nota2)!=0:
        objectoBuscar["Nota 2"]=nota2    

    try:
        registros=tabla.get_children()
        for registro in registros:
            tabla.delete(registro)
        for documento in coleccion.find(objectoBuscar):
            tabla.insert("",0,text=documento["_id"],values=documento["Nombre"])
        
    except pymongo.errors.ServerSelectionTimeoutError as errorTiempo:
        print("Tiempo exedido"+errorTiempo)
    except pymongo.errors.ConnectionFailure as errorConexion:
        print("Fallo al conectar mongodb"+errorConexion)

#Metodo insertar
def crearRegistro():
    if len(id.get())!=0 and len(nombre.get())!=0 and len(nota1.get())!=0 and len(nota2.get())!=0:
        try:
            documento={"_id":id.get(),"Nombre":nombre.get(),"Nota 1":nota1.get(),"Nota 2":nota2.get()}
            coleccion.insert_one(documento)
            id.delete(0,END)
            nombre.delete(0,END)
            nota1.delete(0,END)
            nota2.delete(0,END)
        except pymongo.errors.ConnectionFailure as error:
            print(error)
    else:
        messagebox.showerror(message="Los campos no pueden estar vacios")
    mostrarDatos()

#Metodo de boton
def dobleClickTabla(event):
    global ID_ALUMNO
    ID_ALUMNO=str(tabla.item(tabla.selection())["text"])
    #print(ID_ALUMNO)
    documento=coleccion.find({"_id":(ID_ALUMNO)})[0]
    #print(documento)
    id.delete(0,END)
    id.insert(0,documento["_id"])
    nombre.delete(0,END)
    nombre.insert(0,documento["Nombre"])
    nota1.delete(0,END)
    nota1.insert(0,documento["Nota 1"])
    nota2.delete(0,END)
    nota2.insert(0,documento["Nota 2"])
    crear["state"]="disabled"
    editar["state"]="normal"
    borrar["state"]="normal"

#Metodo de modificar
def editarRegistro():
    global ID_ALUMNO
    if len(id.get())!=0 and len(nombre.get())!=0 and len(nota1.get())!=0 and len(nota2.get())!=0:
        try:
            idBuscar={"_id":(ID_ALUMNO)}
            nuevosValores={"_id":id.get(),"Nombre":nombre.get(),"Nota 1":nota1.get(),"Nota 2":nota2.get()}
            coleccion._update_retryable(idBuscar,nuevosValores)
            id.delete(0,END)
            nombre.delete(0,END)
            nota1.delete(0,END)
            nota2.delete(0,END)
        except pymongo.errors.ConnectionFailure as error:
            print(error)
    else:
        messagebox.showerror("Los campos no pueden estar vacios")
    mostrarDatos()  
    crear["state"]="normal"
    editar["state"]="disabled"
    borrar["state"]="disabled"

#Metodo de eliminar
def borrarRegistro():
    global ID_ALUMNO
    try:
        idBuscar={"_id":(ID_ALUMNO)}
        coleccion.delete_one(idBuscar)
        id.delete(0,END)
        nombre.delete(0,END)
        nota1.delete(0,END)
        nota2.delete(0,END)
    except pymongo.errors.ConnectionFailure as error:
        print(error)
    crear["state"]="normal"
    editar["state"]="disabled"
    borrar["state"]="disabled"
    mostrarDatos()

def buscarRegistro():
    mostrarDatos(buscarId.get(),buscarNombre.get(),buscarNota1.get(),buscarNota2.get())

#Mostrar inferfaz grafica
ventana=Tk()
tabla=ttk.Treeview(ventana,columns=2)
tabla.grid(row=1,column=0,columnspan=2)
tabla.heading("#0",text="ID:")
tabla.heading("#1",text="Nombres:")
tabla.bind("<Double-Button-1>",dobleClickTabla)

#ID
Label(ventana,text="ID del estudiante:                                                         ").grid(row=2,column=0)
id=Entry(ventana)
id.grid(row=2,column=1,sticky=W+E)
id.focus()

#nombre
Label(ventana,text="Nombre del estudiante:                                              ").grid(row=3,column=0)
nombre=Entry(ventana)
nombre.grid(row=3,column=1,sticky=W+E)

#Nota 1
Label(ventana,text="Nota 1 del estudiante:                                                 ").grid(row=4,column=0)
nota1=Entry(ventana)
nota1.grid(row=4,column=1,sticky=W+E)

#Nota 2
Label(ventana,text="Nota 2 del estudiante:                                                 ").grid(row=5,column=0)
nota2=Entry(ventana)
nota2.grid(row=5,column=1,sticky=W+E)

#Boton crear
crear=Button(ventana,text="Crear alumno",command=crearRegistro,bg="red",fg="black")
crear.grid(row=6,columnspan=2,sticky=W+E)

#Boton de modificar
editar=Button(ventana,text="Modificar alumno",command=editarRegistro,bg="Purple")
editar.grid(row=7,columnspan=2,sticky=W+E)
editar["state"]="disabled"

#Boton borrar
borrar=Button(ventana,text="Borrar alumno",command=borrarRegistro,bg="gray")
borrar.grid(row=8,columnspan=2,sticky=W+E)
borrar["state"]="disabled"


#buscar por ID
Label(ventana,text="Buscar por ID:                                                               ").grid(row=9,column=0)
buscarId=Entry(ventana)
buscarId.grid(row=9,column=1,sticky=W+E)
#buscar por nombre
Label(ventana,text="Buscar por nombre:                                                     ").grid(row=10,column=0)
buscarNombre=Entry(ventana)
buscarNombre.grid(row=10,column=1,sticky=W+E)
#buscar por Nota 1
Label(ventana,text="Buscar por nota 1:                                                        ").grid(row=11,column=0)
buscarNota1=Entry(ventana)
buscarNota1.grid(row=11,column=1,sticky=W+E)
#buscar por Nota 2
Label(ventana,text="Buscar por nota 2:                                                        ").grid(row=12,column=0)
buscarNota2=Entry(ventana)
buscarNota2.grid(row=12,column=1,sticky=W+E)

#Boton Buscar
buscar=Button(ventana,text="Buscar alumno",command=buscarRegistro,bg="blue")
buscar.grid(row=13,columnspan=2,sticky=W+E)


mostrarDatos()
ventana.mainloop()