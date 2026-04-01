from tkinter.filedialog import askopenfilename
from tkinter import messagebox
from typing import Any

import gpxpy
from geopy.distance import geodesic
from tkinter import * 
from tkinter import ttk
import matplotlib.pyplot as plt
import adjustText

from tk_panels import datalabel, graphlabel, waypointFrame

root = Tk()
gpxdata = gpxpy.gpx.GPX
lat = StringVar()
long = StringVar()
filenamevar = StringVar()
graphname = StringVar()
filename = StringVar()
sizevar = StringVar()
offset = StringVar()
waypointListWrapper = StringVar()

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
    waypointList = getwaypoints()
    temp = []
    for i in waypointList:
        temp.append(i[2])
    waypointListWrapper.set(temp)


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

    elif (long.get() == "" or lat.get() == ""):
        messagebox.showwarning(message="Latitud o Longitud Base no especificadas!")

    print("_______________________________________________________________")

    alturas, distancias, waypointlabels, xwaypoints, ywaypoints = coord_calc()

    plot_func(alturas, distancias, waypointlabels, xwaypoints, ywaypoints)
    return None


def coord_calc() -> tuple[list[Any], list[Any], list[Any], list[Any], list[Any]]:
    datalist = getdistances()
    waypoints = getwaypoints()
    # print(datalist)

    distancias = []
    alturas = []

    for i in datalist:
        distancias.append(i[0])
        alturas.append((i[1] * 3.28084) / 100)  # Conversion de altura metros del GPX a pies

    xwaypoints = []
    ywaypoints = []
    waypointlabels = []

    for i in waypoints:
        xwaypoints.append(i[0])
        ywaypoints.append((i[1] * 3.28084) / 100)
        waypointlabels.append(i[2])
    return alturas, distancias, waypointlabels, xwaypoints, ywaypoints


def plot_func(alturas: list[Any], distancias: list[Any], waypointlabels: list[Any], xwaypoints: list[Any],
              ywaypoints: list[Any]):
    fig, ax = plt.subplots()

    # ax.set_ylim(bottom=0)

    ax.set_xlabel("Distancia (NM)")
    ax.set_ylabel("Altura (FL)")
    ax.grid(visible=True)

    lines = ax.plot(distancias, alturas, lw=4)
    ax.scatter(xwaypoints, ywaypoints, c='r', marker='x')

    anotations = [plt.text(xwaypoints[i], ywaypoints[i], waypointlabels[i], size=sizevar.get()) for i in
                  range(len(xwaypoints))]

    plt.title(graphname.get())  # filenamevar.get().split('/')[-1].removesuffix('.gpx')
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

    plt.ylim((0, max(alturas) * 1.25))
    plt.xlim((0, max(distancias) * 1.25))

    adjustText.adjust_text(anotations, arrowprops=dict(arrowstyle="-", color='red'), objects=lines, max_move=(10, 10),
                           expand=(1.2, 1.2), force_text=(1.25, 1.25))  # , prevent_crossings=True, only_move= "y")
    plt.show()


def terminateProgram(event):
    root.destroy()

def main():

    root.title("Graficos")

    vcmd = (root.register(validatefloat), '%P')
    
    root.bind("<Control-q>", terminateProgram)

    mainframe = ttk.Frame(root, padding=(3, 3, 12, 12))
    mainframe.grid(column=0, row=0, sticky=(N, W, E, S))

    waypointLf = waypointFrame(mainframe, [waypointListWrapper])
    dataLf = datalabel(mainframe, vcmd, [lat, long, offset, filename, selectfile])
    graphLf = graphlabel(mainframe, [graphname, sizevar])








    ttk.Button(mainframe, text="Generar Grafico", command=generargrafico).grid(column=0, row=3, sticky=W)

    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    mainframe.columnconfigure(2, weight=1)
    for child in mainframe.winfo_children():
        child.grid_configure(padx=5, pady=5)

    #lat_entry.focus()
    #root.bind("<Return>", calculate)

    root.mainloop()


main()
