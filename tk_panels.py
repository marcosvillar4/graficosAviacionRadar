from tkinter import ttk, W, E
from tkinter import *



def datalabel(mainframe, vcmd, vars):
    dataLf = ttk.Labelframe(mainframe, text="Data", padding=(3, 3, 12, 12))
    dataLf.grid(column=0, row=1, padx=20, pady=20, columnspan=3, sticky='WE', ipadx=10, ipady=10)
    dataLf.columnconfigure(1, weight=1, pad=10)
    dataLf.rowconfigure(list(range(4)), pad=5)

    lat_entry = ttk.Entry(dataLf, width=7, textvariable=vars[0], validate='all', validatecommand=vcmd)
    lat_entry.grid(column=1, row=0, sticky=(W, E))
    ttk.Label(dataLf, text="Latidud: ").grid(column=0, row=0, sticky=W)

    long_entry = ttk.Entry(dataLf, width=7, textvariable=vars[1], validate='all', validatecommand=vcmd)
    long_entry.grid(column=1, row=1, sticky=(W, E))
    ttk.Label(dataLf, text="Longitud: ").grid(column=0, row=1, sticky=W)

    offset_entry = ttk.Entry(dataLf, width=7, textvariable=vars[2], validate='all', validatecommand=vcmd)
    vars[2].set("0")
    offset_entry.grid(column=1, row=2, sticky=(W, E))
    ttk.Label(dataLf, text="Offset: ").grid(column=0, row=2, sticky=W)


    ttk.Label(dataLf, text="Archivo: ").grid(column=0, row=3, sticky=W)
    ttk.Label(dataLf, textvariable=vars[3]).grid(column=1, row=3, sticky=W)
    ttk.Button(dataLf, text="Seleccionar archivo", command=vars[4]).grid(column=0, row=4, sticky=W)


    return dataLf


def graphlabel(mainframe, vars):

    sizeList = ["xx-small", "x-small", "small", "medium", "large", "x-large", "xx-large"]

    graphLf = ttk.Labelframe(mainframe, text="Configuracion Grafico", padding=(3, 3, 12, 12))
    graphLf.grid(column=0, row=2, padx=20, pady=20, columnspan=3, sticky='WE', ipadx=10, ipady=10)

    graphLf.columnconfigure(1, weight=1, pad=10)
    graphLf.rowconfigure(list(range(4)), pad=5)

    graph_entry = ttk.Entry(graphLf, width=7, textvariable=vars[0])
    graph_entry.grid(column=1, row=0, sticky=(W, E))
    ttk.Label(graphLf, text="Nombre grafico: ").grid(column=0, row=0, sticky=W)

    ttk.Label(graphLf, text="Tamaño anotaciones: ").grid(column=0,row=1, sticky=W)
    size = ttk.Combobox(graphLf, textvariable=vars[1], width=7)
    size['values'] = sizeList
    size.current(3)
    size.grid(column=1,row=1, sticky=(W, E))

    return graphLf


def waypointFrame(mainframe, vars):

    waypointLf = ttk.Labelframe(mainframe, text="Waypoints", padding=(3, 3, 12, 12))

    waypointLf.grid(column=4, row=0, rowspan=2)

    Listbox(waypointLf, height=10).grid(row=0, column=0)