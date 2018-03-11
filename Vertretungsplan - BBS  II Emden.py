from tkinter import ttk
from tkinter import *
import requests
import json
import os

# variables
page = 0
vplan = None
tableContent = []
navigationLabel = None
leftArrow = None
rightArrow = None
tableHeaders = ["Datum", "Kurs", "Stunde", "Fach", "Raum", "Lehrer", "Info"]
#tableHeaders = ["ID", "Datum", "Kurs", "Stunde", "Fach", "Raum", "Lehrer", "Info"] # test

# config setup
config = {}
configNames = ["Kurs", "History", "Isolate", "width", "height"]
for i in configNames:
    config[i] = False
if os.path.exists('config.json'):
    config = json.loads(open('config.json', 'r').read())

width = config['width']
height = config['height']
if width < 600:
    width = 600
if height < 150:
    height = 150
if (width / 50) != (width // 50):
    width = (width // 50) * 50
if (height / 50) != (height // 50):
    height = (height // 50) * 50
amountRows = (height - 100) // 50

# Tkinter GUIroot = Tk()
root.iconbitmap("icon.ico")
root.title("Vertretungsplan - BBS II Emden //./ by zlyfa! © 2018")
root.geometry('%sx%s+0+0' % (width, height))
root.configure(background='#257BF4')

def getVplan():
    url = "https://zlyfer.net/vertretungsplan/api/api.php?interface=false&vshistory=false"
    if config['History']:
        url = url.replace('vshistory', 'vsnormal')
    if config['Isolate']:
        if config['Kurs']:
            url += "&Kurs=%s" % (config['Kurs'])
    vplan = requests.get(url).text
    vplan = json.loads(vplan)
    return (vplan)

def tableHeaderGen():
    for header_text in tableHeaders:
        header = Label(
            root,
            text=header_text,
            fg="#fff",
            bg="#257BF4",
            font="Helvetica 16 bold"
        )
        header.place(
            x=tableHeaders.index(header_text)*width/len(tableHeaders),
            y=0,
            width=width/len(tableHeaders),
            height=50
        )
        root.update()
    return

def tableContentGen():
    global vplan
    global tableContent
    if vplan == None:
        vplan = getVplan()
    for header_text in tableHeaders:
        for counter in range((page * amountRows), ((page * amountRows) + amountRows)):
            if counter < len(vplan['vertretungen']):
                entry = vplan['vertretungen'][counter]
                if counter <= (page * amountRows) + amountRows:
                    if header_text == "Datum":
                        text = entry[header_text.lower()].split(" ")[0].replace(',', ' - ') + entry[header_text.lower()].split(" ")[1][:-5]
                    elif header_text == "ID": # test
                        text = str(counter+1) # test
                    else:
                        text = entry[header_text.lower()]
                    bgcolor = "#3D8AF5"
                    fgcolor = "#fff"
                    if not config['Isolate']:
                        if entry['kurs'] == config['Kurs']:
                            bgcolor = "#fff"
                            fgcolor = "#3D8AF5"
                    block = Label(
                        root,
                        text=text,
                        fg=fgcolor,
                        bg=bgcolor,
                        font="Helvetica 12 bold"
                    )
                    tableContent.append(block)
                    block.place(
                        x=tableHeaders.index(header_text)*width/len(tableHeaders),
                        y=((counter+1) - (page * amountRows)) * 50,
                        width=width/len(tableHeaders),
                        height=50
                    )
                    root.update()
    return

def placeLoadingLabel():
    label = Label(
        root,
        text="Laden..",
        fg="#fff",
        bg="#3D8AF5",
        font="Helvetica 20 bold"
    )
    label.place(
        x=0,
        y=50,
        width=width,
        height=height-50
    )
    return (label)

def removeLoadingLabel(label):
    label.destroy()
    return

def clearTableContent():
    for i in tableContent:
        i.destroy()
    return

def navigationLabelGen():
    global navigationLabel
    if navigationLabel != None:
        navigationLabel.destroy()
    labelPage = 0
    if (len(vplan['vertretungen']) // amountRows) == (len(vplan['vertretungen']) / amountRows):
        labelPage = len(vplan['vertretungen']) // amountRows
    elif (len(vplan['vertretungen']) // amountRows) != (len(vplan['vertretungen']) / amountRows):
        labelPage = len(vplan['vertretungen']) // amountRows + 1
    navigationLabel = Label(
        root,
        text="%s / %s" % (page + 1, labelPage),
        fg="#fff",
        bg="#5598F7",
        font="Helvetica 20 bold"
    )
    navigationLabel.place(
        x=(width/5)*2,
        y=height-50,
        width=width/5,
        height=50
    )
    return

def navigationArrows(arrow):
    global page
    newpage = page
    if arrow == "next":
        if (len(vplan['vertretungen']) // amountRows) == (len(vplan['vertretungen']) / amountRows):
            if page + 1== (len(vplan['vertretungen']) // amountRows):
                page = 0
            elif (page * amountRows + amountRows) < len(vplan['vertretungen']):
                page += 1
        elif (len(vplan['vertretungen']) // amountRows) != (len(vplan['vertretungen']) / amountRows):
            if page == (len(vplan['vertretungen']) // amountRows):
                page = 0
            elif ((page * amountRows) + amountRows) < len(vplan['vertretungen']):
                page += 1
    elif arrow == "prev":
        if page > 0:
            page -= 1
        elif page == 0:
            if (len(vplan['vertretungen']) // amountRows) == (len(vplan['vertretungen']) / amountRows):
                page = (len(vplan['vertretungen']) // amountRows) - 1
            else:
                page = (len(vplan['vertretungen']) // amountRows)
    if newpage != page:
        navigationLabelGen()
        clearTableContent()
        tableContentGen()
    return

def navigationArrowsNext():
    navigationArrows("next")
    return

def navigationArrowsPrev():
    navigationArrows("prev")
    return
def hoverLeftArrowEnter(event):
    global leftArrow
    leftArrow['bg'] = "#3D8AF5"
    return
def hoverLeftArrowLeave(event):
    global leftArrow
    leftArrow['bg'] = "#257BF4"
    return
def hoverRightArrowEnter(event):
    global leftArrow
    rightArrow['bg'] = "#3D8AF5"
    return
def hoverRightArrowLeave(event):
    global leftArrow
    rightArrow['bg'] = "#257BF4"
    return

def navigationArrowsGen():
    global leftArrow
    global rightArrow
    leftArrow = Button(
        root,
        text="<",
        fg="#fff",
        bg="#257BF4",
        activeforeground="#fff",
        activebackground="#5598F7",
        font="Helvetica 20 bold",
        borderwidth=0,
        command=navigationArrowsPrev
    )
    leftArrow.place(
        x=0,
        y=height-50,
        width=(width/5)*2,
        height=50
    )
    rightArrow = Button(
        root,
        text=">",
        fg="#fff",
        bg="#257BF4",
        activeforeground="#fff",
        activebackground="#5598F7",
        font="Helvetica 20 bold",
        borderwidth=0,
        command=navigationArrowsNext
    )
    rightArrow.place(
        x=(width/5)*3,
        y=height-50,
        width=(width/5)*2,
        height=50
    )
    return

loadingLabel = placeLoadingLabel()
tableHeaderGen()
tableContentGen()
navigationArrowsGen()
navigationLabelGen()
removeLoadingLabel(loadingLabel)
leftArrow.bind('<Enter>', hoverLeftArrowEnter)
leftArrow.bind('<Leave>', hoverLeftArrowLeave)
rightArrow.bind('<Enter>', hoverRightArrowEnter)
rightArrow.bind('<Leave>', hoverRightArrowLeave)

root.mainloop()
