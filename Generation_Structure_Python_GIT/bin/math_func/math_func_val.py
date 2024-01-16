
import FreeCAD as App
import FreeCADGui, ImportGui, Part, Sketcher, math
import numpy as np


def gyroide(abscisse, amplitude, phi=0):
    return [amplitude*math.cos(i + phi)*math.sin(i + phi) for i in abscisse]

doc = FreeCAD.newDocument()
sketch = doc.addObject("Sketcher::SketchObject", 'sketch')

# Variables 

ep_y = 1
ep_x = 1

diam_lat_x = 40
diam_lat_y = 40

espacement_y = 20
espacement_x = 20
amp_y = 1
amp_x = 1

## /!\ (espacement_y/2) > a+(ep/2) pour rester dans le cadre
nb_cos_y = diam_lat_y/espacement_y
nb_cos_x = diam_lat_x/espacement_x
periode = diam_lat_x

tmps_echantillonnage = 0.1

## creation du contour

sketch.addGeometry(Part.LineSegment( App.Vector(0,0,0), App.Vector(diam_lat_x,0,0)),True)
sketch.addGeometry(Part.LineSegment( App.Vector(diam_lat_x,0,0), App.Vector(diam_lat_x,diam_lat_y,0)),True)
sketch.addGeometry(Part.LineSegment( App.Vector(diam_lat_x,diam_lat_y,0), App.Vector(0,diam_lat_y,0)),True)
sketch.addGeometry(Part.LineSegment( App.Vector(0,diam_lat_y,0), App.Vector(0,0,0)),True)


current_pos=(0,0,0)

for j in range(int(nb_cos_y)):
    current_pos=(0,j*espacement_y,0)
    echantillonnage = [i for i in np.arange(0, periode, tmps_echantillonnage)]
    pts_fct = gyroide(echantillonnage, amp_x)

    pts_freecad = [App.Vector(echantillonnage[i], pts_fct[i]+current_pos[1]+(espacement_y/2)-(ep_y/2), 0) for i in range(len(pts_fct))]

    for pts in pts_freecad:
        sketch.addGeometry(Part.Point(pts), True)


    _finalbsp_poles = []
    _finalbsp_knots = []
    _finalbsp_mults = []
    _bsps = []
    _bsps.append(Part.BSplineCurve())
    _bsps[-1].interpolate(pts_freecad, PeriodicFlag=False)
    _bsps[-1].increaseDegree(3)
    _finalbsp_poles.extend(_bsps[-1].getPoles())
    _finalbsp_knots.extend(_bsps[-1].getKnots())
    _finalbsp_mults.extend(_bsps[-1].getMultiplicities())
    sketch.addGeometry(Part.BSplineCurve(_finalbsp_poles,_finalbsp_mults,_finalbsp_knots,False,3,None,False),False)

    pts_freecad = [App.Vector(echantillonnage[i], pts_fct[i]+(ep_y/2)+(espacement_y/2)+current_pos[1], 0) for i in range(len(pts_fct))]

    for pts in pts_freecad:
        sketch.addGeometry(Part.Point(pts), True)


    _finalbsp_poles = []
    _finalbsp_knots = []
    _finalbsp_mults = []
    _bsps = []
    _bsps.append(Part.BSplineCurve())
    _bsps[-1].interpolate(pts_freecad, PeriodicFlag=False)
    _bsps[-1].increaseDegree(3)
    _finalbsp_poles.extend(_bsps[-1].getPoles())
    _finalbsp_knots.extend(_bsps[-1].getKnots())
    _finalbsp_mults.extend(_bsps[-1].getMultiplicities())
    sketch.addGeometry(Part.BSplineCurve(_finalbsp_poles,_finalbsp_mults,_finalbsp_knots,False,3,None,False),False)

    #fermeture des bords

    sketch.addGeometry(Part.LineSegment( App.Vector(0,pts_fct[0]-(ep_y/2)+(espacement_y/2)+current_pos[1],0), App.Vector(0,pts_fct[0]+(ep_y/2)+(espacement_y/2)+current_pos[1],0)),False)


for l in range(int(nb_cos_x)):
    current_pos=(l*espacement_x,0,0)
    echantillonnage = [i for i in np.arange(0, periode, tmps_echantillonnage)]
    pts_fct = gyroide(echantillonnage, amp_y)

    pts_freecad = [App.Vector(pts_fct[i]+current_pos[0]+(espacement_x/2)-(ep_x/2), echantillonnage[i],0) for i in range(len(pts_fct))]

    for pts in pts_freecad:
        sketch.addGeometry(Part.Point(pts), True)


    _finalbsp_poles = []
    _finalbsp_knots = []
    _finalbsp_mults = []
    _bsps = []
    _bsps.append(Part.BSplineCurve())
    _bsps[-1].interpolate(pts_freecad, PeriodicFlag=False)
    _bsps[-1].increaseDegree(3)
    _finalbsp_poles.extend(_bsps[-1].getPoles())
    _finalbsp_knots.extend(_bsps[-1].getKnots())
    _finalbsp_mults.extend(_bsps[-1].getMultiplicities())
    sketch.addGeometry(Part.BSplineCurve(_finalbsp_poles,_finalbsp_mults,_finalbsp_knots,False,3,None,False),False)

    pts_freecad = [App.Vector(pts_fct[i]+current_pos[0]+(espacement_x/2)+(ep_x/2), echantillonnage[i],0) for i in range(len(pts_fct))]

    for pts in pts_freecad:
        sketch.addGeometry(Part.Point(pts), True)


    _finalbsp_poles = []
    _finalbsp_knots = []
    _finalbsp_mults = []
    _bsps = []
    _bsps.append(Part.BSplineCurve())
    _bsps[-1].interpolate(pts_freecad, PeriodicFlag=False)
    _bsps[-1].increaseDegree(3)
    _finalbsp_poles.extend(_bsps[-1].getPoles())
    _finalbsp_knots.extend(_bsps[-1].getKnots())
    _finalbsp_mults.extend(_bsps[-1].getMultiplicities())
    sketch.addGeometry(Part.BSplineCurve(_finalbsp_poles,_finalbsp_mults,_finalbsp_knots,False,3,None,False),False)

    #fermeture des bords

    sketch.addGeometry(Part.LineSegment( App.Vector(pts_fct[0]-(ep_y/2)+(espacement_y/2)+current_pos[0],0,0), App.Vector(pts_fct[0]+(ep_y/2)+(espacement_y/2)+current_pos[0],0,0)),False)