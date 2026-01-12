from tkinter.filedialog import askopenfilename
from tkinter import messagebox

import gpxpy
from geopy.distance import geodesic
from tkinter import *
from tkinter import ttk
import matplotlib.pyplot as plt
import adjustText
from scipy import interpolate
import numpy as np


root = Tk()
gpxdata = gpxpy.gpx.GPX
lat = StringVar()
long = StringVar()
filenamevar = StringVar()
graphname = StringVar()
filename = StringVar()
sizevar = StringVar()

def validatefloat(P):
    if P == "":
        return True  # Allow an empty string for deletion
    try:
        float(P)
        return True
    except ValueError:
        return False

def loadgpxfile(file):
    gpx_file = open(file, 'r')

    gpx = gpxpy.parse(gpx_file)



    return gpx

def selectfile():
    global gpxdata
    filenamevar.set(askopenfilename(filetypes=[("GPX File", "*.gpx")]))
    filename.set(filenamevar.get().split('/')[-1])
    gpxdata = loadgpxfile(filenamevar.get())

def getdistances():
    datalist = []

    for track in gpxdata.tracks:
        for segment in track.segments:
            for point in segment.points:
                distance = geodesic((point.latitude, point.longitude), (lat.get(), long.get())).nautical
                datalist.append([distance, point.elevation])
                #print(f'Time: {point.time} | Point at (Lat: {point.latitude}, Long: {point.longitude}) -> {point.elevation}m')

    return datalist

def getwaypoints():
    waypoints = []

    for waypoint in gpxdata.waypoints:
        #print(f'Waypoint name: {waypoint.name}')
        #print(f'Latitude: {waypoint.latitude}, Longitude: {waypoint.longitude}')
        distance = geodesic((waypoint.latitude, waypoint.longitude), (lat.get(), long.get())).nautical
        waypoints.append([distance, waypoint.elevation, waypoint.name])

    return waypoints

def generargrafico():

    if (filenamevar.get() == ""):
        messagebox.showerror(message="Archivo no seleccionado")
        return None

    print("_______________________________________________________________")





    datalist = getdistances()
    waypoints = getwaypoints()
    #print(datalist)

    distancias = []
    alturas = []



    for i in datalist:
        distancias.append(i[0])
        alturas.append((i[1] * 3.28084) / 100) # Conversion de altura metros del GPX a pies



    xwaypoints = []
    ywaypoints = []
    waypointlabels = []

    for i in waypoints:
        xwaypoints.append(i[0])
        ywaypoints.append((i[1] * 3.28084) / 100)
        waypointlabels.append(i[2])


    fig, ax = plt.subplots()

    #ax.set_ylim(bottom=0)


    ax.set_xlabel("Distancia (NM)")
    ax.set_ylabel("Altura (FL)")
    ax.grid(visible=True)

    lines = ax.plot(distancias, alturas, lw=4)
    ax.scatter(xwaypoints, ywaypoints, c='r', marker='x')





    anotations = [plt.text(xwaypoints[i], ywaypoints[i], waypointlabels[i], size=sizevar.get()) for i in range(len(xwaypoints))]



    plt.title(graphname.get()) #filenamevar.get().split('/')[-1].removesuffix('.gpx')
    print(plt.get_backend())
    match plt.get_backend().lower():
        case "tkagg":
            mng = plt.get_current_fig_manager()
            mng.window.state("zoomed")
        case "wxagg":
            mng = plt.get_current_fig_manager()
            mng.frame.maximize(True)
        case "qt4agg":
            mng = plt.get_current_fig_manager()
            mng.window.showMaximized()


    plt.ylim((0,max(alturas) * 1.25))
    plt.xlim((0, max(distancias) * 1.25))

    adjustText.adjust_text(anotations,arrowprops=dict(arrowstyle="-", color='red'), objects=lines, max_move=(10, 10), expand=(1.2,1.2), force_text=(1.25,1.25))#, prevent_crossings=True, only_move= "y")
    plt.show()
    return None

def main():

    root.title("Graficos")

    vcmd = (root.register(validatefloat), '%P')


    mainframe = ttk.Frame(root, padding=(3, 3, 12, 12))
    mainframe.grid(column=0, row=0, sticky=(N, W, E, S))

    dataLf = datalabel(mainframe, vcmd)
    graphLf = graphlabel(mainframe)



    ttk.Button(mainframe, text="Generar Grafico", command=generargrafico).grid(column=0, row=3, sticky=W)

    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    mainframe.columnconfigure(2, weight=1)
    for child in mainframe.winfo_children():
        child.grid_configure(padx=5, pady=5)

    #lat_entry.focus()
    #root.bind("<Return>", calculate)

    root.mainloop()

def datalabel(mainframe, vcmd):
    dataLf = ttk.Labelframe(mainframe, text="Data", padding=(3, 3, 12, 12))
    dataLf.grid(column=0, row=1, padx=20, pady=20, columnspan=3, sticky='WE', ipadx=10, ipady=10)
    dataLf.columnconfigure(1, weight=1, pad=10)
    dataLf.rowconfigure(list(range(4)), pad=5)

    lat_entry = ttk.Entry(dataLf, width=7, textvariable=lat, validate='all', validatecommand=vcmd)
    lat_entry.grid(column=1, row=0, sticky=(W, E))
    ttk.Label(dataLf, text="Latidud: ").grid(column=0, row=0, sticky=W)

    long_entry = ttk.Entry(dataLf, width=7, textvariable=long, validate='all', validatecommand=vcmd)
    long_entry.grid(column=1, row=1, sticky=(W, E))
    ttk.Label(dataLf, text="Longitud: ").grid(column=0, row=1, sticky=W)



    ttk.Label(dataLf, text="Archivo: ").grid(column=0, row=3, sticky=W)
    ttk.Label(dataLf, textvariable=filename).grid(column=1, row=3, sticky=W)
    ttk.Button(dataLf, text="Seleccionar archivo", command=selectfile).grid(column=0, row=4, sticky=W)


    return dataLf

def graphlabel(mainframe):

    sizeList = ["xx-small", "x-small", "small", "medium", "large", "x-large", "xx-large"]

    graphLf = ttk.Labelframe(mainframe, text="Configuracion Grafico", padding=(3, 3, 12, 12))
    graphLf.grid(column=0, row=2, padx=20, pady=20, columnspan=3, sticky='WE', ipadx=10, ipady=10)

    graphLf.columnconfigure(1, weight=1, pad=10)
    graphLf.rowconfigure(list(range(4)), pad=5)

    graph_entry = ttk.Entry(graphLf, width=7, textvariable=graphname)
    graph_entry.grid(column=1, row=0, sticky=(W, E))
    ttk.Label(graphLf, text="Nombre grafico: ").grid(column=0, row=0, sticky=W)

    ttk.Label(graphLf, text="Tamaño anotaciones: ").grid(column=0,row=1, sticky=W)
    size = ttk.Combobox(graphLf, textvariable=sizevar, width=7)
    size['values'] = sizeList
    size.current(3)
    size.grid(column=1,row=1, sticky=(W, E))

    return graphLf

main()