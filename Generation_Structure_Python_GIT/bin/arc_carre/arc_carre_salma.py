import FreeCAD as App
import FreeCADGui, ImportGui, Part, Sketcher, math
doc=FreeCAD.newDocument()
sketch = doc.addObject("Sketcher::SketchObject", 'Sketch')
# Dimensions caractéristiques dela géométrie arc 1 et 2 calculées (voir schéma)
ep=0.7
rayon1= 5
rayon2=ep+rayon1
alpha1=math.pi / 2
alpha2=math.radians(36)
alpha3=math.radians(54)
normale=(0, 0, 1)
point_centre=(0, 0, 0)
dimlat_x=30
dimlat_y=30
nb_geo_x=3
nb_geo_y=3
lx = dimlat_x / nb_geo_x
ly = dimlat_y / nb_geo_y
cote_carre= lx+2*(rayon2-rayon1)
# épaisseurs:
epx=(lx/2)- cote_carre
epy=(ly/2)- cote_carre


 # Construction des structures################################################### 


 # Curseur de position (repère local à chaque losange)
current_pos = (0,0,0)

# i = Numéro de losange y (ligne)
# j = Numéro de losange x (colonne)
for j in range(nb_geo_y):
	for i in range(nb_geo_x):
		current_pos = ((lx+2*rayon2) * i, (ly+2*rayon2) * j, 0)
		# point avec current
		#1 er quart 
		pt1e = App.Vector(current_pos[0]+0,current_pos[1]+ 0, current_pos[2]+0)
		pt2e = App.Vector(current_pos[0]+rayon1,current_pos[1]+ 0, current_pos[2]+0)
		pt3e=App.Vector(current_pos[0]+rayon2,current_pos[1]+ 0, current_pos[2]+0)
		pt11e=App.Vector(current_pos[0]+0, current_pos[1]+rayon2, current_pos[2]+0)
		pt12e=App.Vector(current_pos[0]+0, current_pos[1]+rayon1,current_pos[2]+0)
		pt4e=App.Vector(current_pos[0]+math.sqrt((rayon2**2)-((ly/2)+rayon2-(cote_carre/2)-ep)),current_pos[1]+(ly/2)+rayon2-(cote_carre/2)-ep,current_pos[2]+0)
		pt5e=App.Vector(current_pos[0]+(lx/2)+rayon2,current_pos[1]+rayon2*math.sin(math.radians(36)),current_pos[2]+0)
		pt6e=App.Vector(current_pos[0]+(lx/2)+rayon2,current_pos[1]+rayon2*math.sin(math.radians(36))+ep,current_pos[2]+0)
		pt7e=App.Vector(current_pos[0]+rayon2*math.cos(math.radians(54))+ep,current_pos[1]+rayon2*math.sin(math.radians(36))+ep,current_pos[2]+0)
		pt8e=App.Vector(current_pos[0]+rayon2*math.cos(math.radians(54))+ep,current_pos[1]+(ly/2)+rayon2,current_pos[2]+0)
		pt9e=App.Vector(current_pos[0]+rayon2*math.cos(math.radians(54)),current_pos[1]+(ly/2)+rayon2,current_pos[2]+0)
		pt10e=App.Vector(current_pos[0]+(ly/2)+rayon2-(cote_carre/2)-ep,current_pos[1]+math.sqrt((rayon2**2)-(ly/2)+rayon2-(cote_carre/2)-ep),current_pos[2]+0)
		pt15e=App.Vector(current_pos[0]+(lx/2)+(rayon2),current_pos[1]+0,current_pos[2]+0)
		pt16e=App.Vector(current_pos[0]+0,current_pos[1]+(ly/2)+(rayon2),current_pos[2]+0)
		pt17e=App.Vector(current_pos[0]+(lx/2)+(rayon2),current_pos[1]+(ly/2)+(rayon2),current_pos[2]+0)
		pt19e= App.Vector(current_pos[0]+(lx/2)+(rayon2)-(cote_carre/2)-ep,current_pos[1]+ (ly/2)+(rayon2),current_pos[2]+0)
		pt20e=App.Vector(current_pos[0]+rayon2*math.cos(math.radians(54)),current_pos[1]+rayon2*math.sin(math.radians(54)),current_pos[2]+0)
		pt21e=App.Vector(current_pos[0]+rayon2*math.cos(math.radians(36)),current_pos[1]+rayon2*math.sin(math.radians(36)),0+current_pos[2])
		#Lignes 
		linesym= sketch.addGeometry(Part.LineSegment(pt20e, pt9e), False)
		line215= sketch.addGeometry(Part.LineSegment(pt21e, pt5e), False)
		line76= sketch.addGeometry(Part.LineSegment(pt6e, pt7e),False)
		line3= sketch.addGeometry(Part.LineSegment(pt17e, pt15e), True)
		line5= sketch.addGeometry(Part.LineSegment(pt17e, pt16e), True)
		line3= sketch.addGeometry(Part.LineSegment(pt1e, pt15e), True)
		line3= sketch.addGeometry(Part.LineSegment(pt1e, pt16e), True)
		#ligne 7-8:
		line78 = sketch.addGeometry(Part.LineSegment(pt7e, pt8e),False)
		# ligne 16-11:
		line1= sketch.addGeometry(Part.LineSegment(pt11e, pt16e),True)
		# ligne 3-15:
		line2= sketch.addGeometry(Part.LineSegment(pt3e, pt15e), True)

		
		#Constructuion des arcs:
		arc = sketch.addGeometry(Part.ArcOfCircle(Part.Circle(pt1e,App.Vector(0,0,1),rayon1),0, alpha1), False)
		arc2 = sketch.addGeometry(Part.ArcOfCircle(Part.Circle(pt1e,App.Vector(0,0,1),rayon2),0, alpha2), False)
		arc3 = sketch.addGeometry(Part.ArcOfCircle(Part.Circle(pt1e,App.Vector(0,0,1),rayon2),alpha3, alpha1), False)
		

		# 2 eme quart 
		# 2eme carre 
		pt1be = App.Vector(current_pos[0]+2*((lx/2)+rayon2),current_pos[1]+0,current_pos[2]+0)
		pt16be=App.Vector(current_pos[0]+2*((lx/2)+rayon2),current_pos[1]+(ly/2)+(rayon2),current_pos[2]+0)
		lineW= sketch.addGeometry(Part.LineSegment(pt1be, pt15e), True)
		lineV= sketch.addGeometry(Part.LineSegment(pt17e, pt16be), True)
		linez=sketch.addGeometry(Part.LineSegment(pt1be, pt16be), True)
		# les points 
		alpha4=math.pi
		alpha5=math.pi/2
		pt2be = App.Vector(current_pos[0]+2*((lx/2)+rayon2)-rayon1, current_pos[1]+0, current_pos[2]+0)
		pt3be=App.Vector(current_pos[0]+2*((lx/2)+rayon2)-rayon2,current_pos[1]+ 0, current_pos[2]+0)
		pt11be=App.Vector(current_pos[0]+2*((lx/2)+rayon2), current_pos[1]+rayon2, current_pos[2]+0)
		pt12be=App.Vector(current_pos[0]+2*((lx/2)+rayon2),current_pos[1]+ rayon1, current_pos[2]+0)
		pt5be=App.Vector(current_pos[0]+(lx/2)+rayon2,current_pos[1]+rayon2*math.sin(math.radians(36)),current_pos[2]+0)
		pt6be=App.Vector(current_pos[0]+(lx/2)+rayon2,current_pos[1]+rayon1,current_pos[2]+0)
		pt7be=App.Vector(current_pos[0]+2*(lx/2+rayon2)-rayon2*math.cos(math.radians(54))-ep,current_pos[1]+rayon2*math.sin(math.radians(36))+ep,current_pos[2]+0)
		pt8be=App.Vector(current_pos[0]+2*(lx/2+rayon2)-rayon2*math.cos(math.radians(54))-ep,current_pos[1]+(ly/2)+rayon2,current_pos[2]+0)
		pt9be=App.Vector(current_pos[0]+rayon2*math.cos(math.radians(54)),current_pos[1]+(ly/2)+rayon2,current_pos[2]+0)
		# construction des arcs droites
		arcb = sketch.addGeometry(Part.ArcOfCircle(Part.Circle(pt1be,App.Vector(0,0,1),rayon1),alpha5, alpha4), False)
		arc2b = sketch.addGeometry(Part.ArcOfCircle(Part.Circle(pt1be,App.Vector(0,0,1),rayon2),alpha5, alpha5+alpha2), False)
		arc3b = sketch.addGeometry(Part.ArcOfCircle(Part.Circle(pt1be,App.Vector(0,0,1),rayon2),alpha5+alpha3, alpha4), False)
		# point delimitant arcs ( a de bas et b de haut )
		ptae=App.Vector(current_pos[0]+2*(lx/2+rayon2)-rayon2*math.cos(math.radians(54)),current_pos[1]+rayon2*math.sin(math.radians(54)),current_pos[2]+0)
		ptbe=App.Vector(current_pos[0]+2*(lx/2+rayon2)-rayon2*math.cos(math.radians(36)),current_pos[1]+rayon2*math.sin(math.radians(36)),current_pos[2]+0)
		#ligne 5a et b9
		line5a= sketch.addGeometry(Part.LineSegment(ptbe, pt5e), False)
		#ligne7b-6:
		line7b6= sketch.addGeometry(Part.LineSegment(pt6e, pt7be),False)
		#ligne 7b-8b:
		line78b = sketch.addGeometry(Part.LineSegment(pt7be, pt8be),False)

		#les deux quarts du haut 
		# Constructuons des deux quarts du haut # Construction deux carree hauts 
		pt16ce=App.Vector(current_pos[0]+0,current_pos[1]+2*((ly/2)+(rayon2)),current_pos[2]+0)
		pt17ce=App.Vector(current_pos[0]+((lx/2)+(rayon2)),current_pos[1]+2*((ly/2)+(rayon2)),current_pos[2]+0)
		pt1ce = App.Vector(current_pos[0]+2*((lx/2)+rayon2),current_pos[1]+2*((ly/2)+(rayon2)),current_pos[2]+0)
		# ligne 16c-17c:
		line= sketch.addGeometry(Part.LineSegment(pt16e, pt16ce), True)
		line= sketch.addGeometry(Part.LineSegment(pt16ce, pt17ce), True)
		line= sketch.addGeometry(Part.LineSegment(pt17ce, pt17e), True)
		line= sketch.addGeometry(Part.LineSegment(pt17ce, pt1ce), True)
		line= sketch.addGeometry(Part.LineSegment(pt1ce, pt16be), True)
		# Constructuons des deux quarts du haut 
		#Construction des arcs haut gauche :
		arc1 = sketch.addGeometry(Part.ArcOfCircle(Part.Circle(pt16ce,App.Vector(0,0,1),rayon1),-alpha1, 0, False))
		arc= sketch.addGeometry(Part.ArcOfCircle(Part.Circle(pt16ce,App.Vector(0,0,1),rayon2),2*math.pi-alpha2,0), False)
		arc= sketch.addGeometry(Part.ArcOfCircle(Part.Circle(pt16ce,App.Vector(0,0,1),rayon2),-alpha1,2*math.pi-alpha1+alpha2, False))
		#Construction des arcs haut droite :
		arc1 = sketch.addGeometry(Part.ArcOfCircle(Part.Circle(pt1ce,App.Vector(0,0,1),rayon1),math.pi,-alpha1, False))
		arc= sketch.addGeometry(Part.ArcOfCircle(Part.Circle(pt1ce,App.Vector(0,0,1),rayon2),math.pi,(3/2)*math.pi-alpha3), False)
		arc= sketch.addGeometry(Part.ArcOfCircle(Part.Circle(pt1ce,App.Vector(0,0,1),rayon2),3/2*(math.pi)-alpha2,-alpha1, False))
		# carre milieu 
		pt8ce=App.Vector(current_pos[0]+rayon2*math.cos(math.radians(54))+ep,current_pos[1]+2*(lx/2+rayon2)-rayon2*math.sin(math.radians(36))-ep,current_pos[2]+0)
		pt7ce=App.Vector(current_pos[0]+2*(lx/2+rayon2)-rayon2*math.cos(math.radians(54))-ep,current_pos[1]+2*(lx/2+rayon2)-rayon2*math.sin(math.radians(36))-ep,current_pos[2]+0)
		pt6ce=App.Vector(current_pos[0]+(lx/2)+rayon2,current_pos[1]+2*(lx/2+rayon2)-rayon2*math.sin(math.radians(36))-ep,current_pos[2]+0)
		#ligne 7c-8:
		line = sketch.addGeometry(Part.LineSegment(pt8ce, pt8e),False)
		#ligne 6c-8c:
		line = sketch.addGeometry(Part.LineSegment(pt8ce, pt6ce),False)
		#ligne 7c-8b:
		line = sketch.addGeometry(Part.LineSegment(pt8be, pt7ce),False)
		#ligne 7c-6c:
		line = sketch.addGeometry(Part.LineSegment(pt6ce, pt7ce),False)
		# fermeture des arcs haut
		pt11ce=App.Vector(current_pos[0]+0,current_pos[1]+2*((ly/2)+rayon2)-rayon2, current_pos[2]+0)
		pt12ce=App.Vector(current_pos[0]+0,current_pos[1]+2*((ly/2)+rayon2)-rayon1, current_pos[2]+0)
		"""
		line = sketch.addGeometry(Part.LineSegment(pt12ce, pt11ce),False)
		"""
		pt2ce = App.Vector(current_pos[0]+rayon1,current_pos[1]+2*((ly/2)+(rayon2)) ,current_pos[2]+ 0)
		pt3ce=App.Vector(current_pos[0]+rayon2,current_pos[1]+2*((ly/2)+(rayon2)), current_pos[2]+0)
		"""
		line = sketch.addGeometry(Part.LineSegment(pt2ce, pt3ce),False)
		"""
		pt2de = App.Vector(current_pos[0]+2*((lx/2)+rayon2)-rayon1,current_pos[1]+2*((ly/2)+(rayon2)), current_pos[2]+0)
		pt3de=App.Vector(current_pos[0]+2*((lx/2)+rayon2)-rayon2,current_pos[1]+2*((ly/2)+(rayon2)), current_pos[2]+0)
		"""
		line = sketch.addGeometry(Part.LineSegment(pt2de, pt3de),False)
		"""
		pt11de=App.Vector(current_pos[0]+2*((lx/2)+rayon2), current_pos[1]+2*((ly/2)+rayon2)-rayon2, current_pos[2]+0)
		pt12de=App.Vector(current_pos[0]+2*((lx/2)+rayon2),current_pos[1]+2*((ly/2)+rayon2)- rayon1,current_pos[2]+ 0)
		"""
		line = sketch.addGeometry(Part.LineSegment(pt12de, pt11de),False)
		"""
		# fermerure arcs intermediaires 
		ptse=ptb=App.Vector(current_pos[0]+rayon2*math.cos(math.radians(36)),current_pos[1]+2*(lx/2+rayon2)-rayon2*math.sin(math.radians(36)),current_pos[2]+0)
		ptue=App.Vector(current_pos[0]+rayon2*math.cos(math.radians(54)),current_pos[1]+2*(lx/2+rayon2)-rayon2*math.sin(math.radians(54)),current_pos[2]+0)
		pt5ce=App.Vector(current_pos[0]+(lx/2)+rayon2,current_pos[1]+2*(lx/2+rayon2)-rayon2*math.sin(math.radians(36)),current_pos[2]+0)
		line= sketch.addGeometry(Part.LineSegment(pt20e, ptue), False)
		line= sketch.addGeometry(Part.LineSegment(pt5ce, ptse), False)
		ptke=App.Vector(current_pos[0]+2*(lx/2+rayon2)-rayon2*math.cos(math.radians(36)),current_pos[1]+2*(lx/2+rayon2)-rayon2*math.sin(math.radians(36)),current_pos[2]+0)
		ptle=App.Vector(current_pos[0]+2*(lx/2+rayon2)-rayon2*math.cos(math.radians(54)),current_pos[1]+2*(lx/2+rayon2)-rayon2*math.sin(math.radians(54)),current_pos[2]+0)
		line= sketch.addGeometry(Part.LineSegment(pt5ce, ptke), False)
		line= sketch.addGeometry(Part.LineSegment(ptae, ptle), False)
		# Fermeture des bords 
		if i==0 : 
			if j==0:
				line= sketch.addGeometry(Part.LineSegment(pt11e, pt12e),False)
				line = sketch.addGeometry(Part.LineSegment(pt12ce, pt11ce),False)
			elif j== nb_geo_y-1:
				line= sketch.addGeometry(Part.LineSegment(pt11e, pt12e),False)
				line = sketch.addGeometry(Part.LineSegment(pt12ce, pt11ce),False)
			if j>0:
				line= sketch.addGeometry(Part.LineSegment(pt11e, pt12e),False)
				line = sketch.addGeometry(Part.LineSegment(pt12ce, pt11ce),False)
		if j==0 : 
			if i==0:
				line23= sketch.addGeometry(Part.LineSegment(pt2e, pt3e),False)
				line= sketch.addGeometry(Part.LineSegment(pt2be, pt3be),False)
			elif i== nb_geo_x-1:
				line23= sketch.addGeometry(Part.LineSegment(pt2e, pt3e),False)
				line= sketch.addGeometry(Part.LineSegment(pt2be, pt3be),False)
			if i>0:
				line23= sketch.addGeometry(Part.LineSegment(pt2e, pt3e),False)
				line= sketch.addGeometry(Part.LineSegment(pt2be, pt3be),False)
		if j==nb_geo_y-1 : 
			if i==0:
				line = sketch.addGeometry(Part.LineSegment(pt2de, pt3de),False)
				line = sketch.addGeometry(Part.LineSegment(pt2ce, pt3ce),False)
			elif i== nb_geo_x-1:
				line = sketch.addGeometry(Part.LineSegment(pt2de, pt3de),False)
				line = sketch.addGeometry(Part.LineSegment(pt2ce, pt3ce),False)
			if i>0:
				line = sketch.addGeometry(Part.LineSegment(pt2de, pt3de),False)
				line = sketch.addGeometry(Part.LineSegment(pt2ce, pt3ce),False)
		if i==nb_geo_x-1 : 
			if j==0:
				line= sketch.addGeometry(Part.LineSegment(pt11be, pt12be),False)
				line = sketch.addGeometry(Part.LineSegment(pt12de, pt11de),False)
			elif j== nb_geo_x-1:
				line= sketch.addGeometry(Part.LineSegment(pt11be, pt12be),False)
				line = sketch.addGeometry(Part.LineSegment(pt12de, pt11de),False)
			if j>0:
				line= sketch.addGeometry(Part.LineSegment(pt11be, pt12be),False)
				line = sketch.addGeometry(Part.LineSegment(pt12de, pt11de),False)
		
		

