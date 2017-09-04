#!/usr/bin/python3.4.0
# -*- coding: utf-8 -*-
#  designed by Mohamed SAMB DIC2 Info

#  maillage.py

import time
from fonctions import *

#definition des variables globaux
p=1
isConnected = False#indicateur de connection

#creation de la variable socket associée au client
sockClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
"""FOnction de connexion/deconnexion au serveur"""
def fonctConnect():
	global isConnected,sockClient
	
	if varBtnConnect.get()=="Connexion":
		try:
			isConnected = True
			sockClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			sockClient.connect(("127.0.0.1", 3333))
			btnConnect.configure(bg='red')
			varBtnConnect.set("Déconnexion")
		except:
			showerror("connexion", "Impossible de se connecter au serveur")
	else:
		sockClient.send(str("disconnect").encode())
		btnConnect.configure(bg='#007980')
		varBtnConnect.set("Connexion")
		isConnected = False


"""Fonction qui centre le maillage importe"""
def center(toplevel):
    toplevel.update_idletasks()
    w = toplevel.winfo_screenwidth()
    h = toplevel.winfo_screenheight()
    size = tuple(int(_) for _ in toplevel.geometry().split('+')[0].split('x'))
    x = w/2 - size[0]/2
    y = h/2 - size[1]/2
    toplevel.geometry("%dx%d+%d+%d" % (size + (x, y)))

"""Fonction pour importer un fichier de maillage"""
def openFile():
	if not isConnected:
		showerror("Connection error","Veuillez vous connectez au niveau du serveur")
	else:
		receivedFiles = askopenfilenames(parent=fenetre, initialdir="/home/sambman/Documents/Projects/maillageTk/files/",
							   filetypes =[("Text File", "text {.txt}")],
							   title = "Choisir le fichier des sommets et le fichier des coordonnées correspondant."
							   )
		filesMaillage = fenetre.splitlist(receivedFiles)
		print(filesMaillage)
		if len(filesMaillage)==2:
			
			fileCoords = filesMaillage[0]
			fileSoms = filesMaillage[1]
			
			rCoords = fileCoords.split('.')[0]
			rSoms = fileSoms.split('.')[0]
			
			print(rCoords,"\n",rSoms)
			
			rCoords = rCoords[0:len(rCoords)-6]
			rSoms = rSoms[0:len(rSoms)-4]
			
			
			fileOk = rSoms==rCoords
			ext = fileCoords.find("Coords.txt") and fileSoms.find("Soms.txt")
			print(ext)
			if ext==-1 or not fileOk:
				showerror("Erreur fichier", "Les fichiers doivent être de même initial. Exemple *Coords.txt et *Soms.txt")
			else:
				#tracé du maillage impoté
				dlg1 = Toplevel(master=fenetre)
				dlg1.geometry("600x600")
				center(dlg1)

				fig = plt.figure()
				traceur = fig.add_subplot(111)
				canvas = FigureCanvasTkAgg(fig, master=dlg1)
				canvas.get_tk_widget().pack()
				#ajout de la barre de navigation
				toolbar = NavigationToolbar2TkAgg(canvas, dlg1)
				toolbar.update()
				canvas._tkcanvas.pack()
				
				#Ouverture de fichiers pour la recuperation des coordonnees
				lignes = list
				with open(fileCoords,"r") as ficCoords:
					lignes = ficCoords.readlines()
				
				#recuperation des coordonnees
				coords = [lignes[i].split(' ') for i in range(0,len(lignes))]
				coords = [[float(coords[i][0]),float(coords[i][1][0:len(coords[i][1])-1])] for i in range(0,len(coords))]
				
				#Ouverture du fichier pour recuperer numeros de sommets
				lignes = list
				with open(fileSoms,"r") as ficSoms:
					lignes = ficSoms.readlines()
				
				#recuperation des numeros
				sommets = [lignes[i].split(' ') for i in range(0,len(lignes))]
				sommets= [[int(sommets[i][0]),int(sommets[i][1]),int(sommets[i][2][0:len(sommets[i][2])-1])] for i in range(0,len(sommets))]
				
				#recuperation des triangles à colorier
				triangles = getTriangles(coords,sommets)
				
				#recuperation des triplets pour le dessin
				triplets = getTabTriplets(triangles)
				coordsGrav = coordsGravite(triplets)#recuperation coordonnees centres de gravite
				#tracage du maillage
				for i in range(0,len(triplets)):
					traceur.add_patch(Polygon(triplets[i], closed=True,fill=False, color='#FF0000'))#on applique la couleur obtenue avec l'integrale
					traceur.add_patch(Polygon(triplets[i], closed=True,fill=False, color='#000000',linestyle='dashdot'))
				
				canvas.show()
				

		else:
			showerror("Chargement fichier", "Deux fichiers de même initial doivent être chargés en même temps")
                           
"""Fonction qui trace un maillage rectangulaire"""
def rectangulaire():
	fig.clear()
	traceur = fig.add_subplot(111)
	for i in range(0,p+1):
		traceur.plot([0,1],[float(i)/p,float(i)/p],'#8B6914',lw=2) #tracee des traits horizontaux
		traceur.plot([float(i)/p,float(i)/p],[0,1],'#8B6914',lw=2) #tracee des traits verticaux
		traceur.plot([float(i)/p,0],[0,float(i)/p],'#ADD8E6',lw=2) #tracee des traits obliques de la partie basse du carre
		traceur.plot([float(i)/p,1],[1,float(i)/p],'#ADD8E6',lw=2) #tracee des traits obliques de la partie haute du carre
	canvas.show()
	
"""Fonction qui trace un maillage triangulaire"""
def triangulaire():
	fig.clear()
	traceur = fig.add_subplot(111)
	for i in range(0,p+1):
		traceur.plot([0,1-float(i)/p],[float(i)/p,float(i)/p],'#8B6914',lw=2) #tracee des traits horizontaux
		traceur.plot([float(i)/p,float(i)/p],[0,1-float(i)/p],'#8B6914',lw=2) #tracee des traits verticaux
		traceur.plot([float(i)/p,0],[0,float(i)/p],'#ADD8E6',lw=2) # tracee des traits obliques 
	
	canvas.show()

"""Fonction qui trace un maillage polygonal"""
def polygonal():
	if p<3:
		showerror("polygonal", "Le maillage polygonal necessite au moins trois(3) points")
	else:
		fig.clear()
		traceur = fig.add_subplot(111)
		
		#dessin du polygone à mailler
		x,y = unit_poly_verts(p)#reception des sommets du maillage polygonal
		x = np.array(x)
		y = np.array(y)
		
		print("Avant 3")
		my_tri = mtri.Triangulation(x,y)
		print("Avant 4")
		refiner = mtri.UniformTriRefiner(my_tri)  #plot the original triangulation
		print("Avant 5")
		for t in my_tri.triangles:
			t_i = [t[0], t[1], t[2], t[0]]
			traceur.plot(x[t_i],y[t_i] ,'k',linewidth=1.5)
		print("Apres")
		
		canvas.show()	
		
"""Fonction qui genere le maillage"""
def genereMaillage():
	global p
	if isConnected==False:
		showerror("Connection error","Veuillez vous connectez au niveau du serveur")
	else:
		
		try:
			time.sleep(2)
			p = int(spin.get())
			cmdServeur = str(p)+" "+ch.get()
			if ch.get()=="domaine triangulaire":
				
				sockClient.send(cmdServeur.encode())
				triangulaire()
			elif ch.get()=="domaine rectangulaire":
				rectangulaire()
				sockClient.send(cmdServeur.encode())
			elif ch.get()=="domaine polygonal":
				polygonal()
				sockClient.send(cmdServeur.encode())
			else:
				showerror("maillage", "Le type de maillage "+ch.get()+" entré n'est pas pris en compte")
		except:
			showerror("entrée", "Veuillez entrer un nombre valide")


"""Fonction pour sauvegarder  notre maillage"""
def sauvegarder():
	if not isConnected:
		showerror("Connection error","Veuillez vous connectez au niveau du serveur")
	else:
		
		try:
			nomfic = askstring("nom du fichier", "Entrer le nom du fichier")
			if nomfic!="" or numfic!=str(None):
				enreg=True
				if askyesno("Enregistrer", "Confirmation de sauvegarde ?"):
					time.sleep(2)
					cmd = str(p)+" "+ch.get()+" "+nomfic
					if ch.get()=="domaine rectangulaire":
						sockClient.send(cmd.encode())
						sauvegardeRect(nomfic,"rectangle/",p)
					elif ch.get()=="domaine triangulaire":
						sockClient.send(cmd.encode())
						sauvegardeTri(nomfic,"triangle/",p)
					elif ch.get()=="domaine polygonal":
						sockClient.send(cmd.encode())
						showinfo("maillage", "Le stockage de ce type de maillage n'est pas encore défini au niveau du serveur'")
						
					else:
						showerror("maillage", "Le type de maillage "+ch.get()+" entré n'est pas pris en compte")
						enreg=False
					if enreg:
						showinfo("Infos","Maillage correctement enrégistré")
			else:
				showerror("Erreur", "Le nom du fichier ne doit pas être vide")


		except:
			showerror("Erreur","Maillage non encore spécifié")
	
"""Coloriage maillage
prend un tableau de triplets et un tableau des valeurs correspondantes
obtenues en integrant la fonction f(x,y)
"""
def coloriage(tabTriangles, tabIntegrales):
	if not isConnected:
		showerror("Connection error","Veuillez vous connectez au niveau du serveur")
	else:
		time.sleep(2)
		fig.clear()
		traceur = fig.add_subplot(111)
		
		tabTriplets = getTabTriplets(tabTriangles)#recuperation du tableau de triplets
		coordsGrav = coordsGravite(tabTriplets)#recuperation coordonnees centres de gravite
        
		if ch.get()=="domaine polygonal":
			print("Coloriage non disponible")
		else:
			#envoi du commande de coloriage au serveur
			cmd = str(p)+" "+ch.get()+" coloriage"
			sockClient.send(cmd.encode())
			
			for i in range(0,len(tabTriplets)):
				col = round(tabIntegrales[i]*100)
				if col<0:
					col=0
				elif col>=278:
					col=277
				traceur.add_patch(Polygon(tabTriplets[i], closed=True,fill=True, color=COLORS[col]))#on applique la couleur obtenue avec l'integrale
				traceur.add_patch(Polygon(tabTriplets[i], closed=True,fill=False, color='#000000',linestyle='dashdot'))
				traceur.text(coordsGrav[i][0], coordsGrav[i][1], str(i+1), size=2+p%10, ha='center',va='center')
								 
			canvas.show()


"""Fonction qui regroupe tout ce qui est lie a la fonction affine"""
def fonctTemp():
	
	print("Voici ma fonction affine")
	fvar = fonct.get()
	fonction.set("f(x,y)= "+fonct.get())
	ok = True
	x=0
	y=0
	
	try:
		f = eval(fvar)
		print(fvar)
		ok = (len(fvar.split('x'))==2) and (len(fvar.split('y'))==2)
		print("After ok")
	except:
		ok = False
	if not ok:
		showerror("fonction", "La fonction saisie ne respecte pas le format.")
	else:
		coords=sommets=triangles=list
		print("Application de la fonction de temperature")
			
		#recuperation des coordonnees
		coords = getCoords("tmp",ch.get(),p)
				
		#recuperation des numeros
		sommets = getSommets("tmp")
		
		triangles = getTriangles(coords,sommets)#recuperation des triangles à colorier
		
		inteTriangles = getIntegrales(triangles,fvar)#valeurs des integrales au niveau de chaque element fini du maillage
		
		coloriage(triangles,inteTriangles)#application des couleurs
		
	fonct.set("")#reinitialiser la fonction
	

"""Fonction a appliquer a la fermeture de l'application afin de liberer les ressources"""
def on_closing():
	global sockClient,fenetre
	try:
	    sockClient.send(str("disconnect").encode())
	except:
		print("pk")
		
	fenetre.quit()

#corps principal du programme
fenetre = Tk()
fenetre.title('Maillage visuel')
fenetre['bg'] = 'white'
fenetre.resizable(width=False, height=False)

#framePanel
framePane = PanedWindow(fenetre, orient=VERTICAL)
framePane.pack(side=LEFT, expand=Y, fill=BOTH, pady=2, padx=2)

#Frame1
frame1 = Frame(None, borderwidth=2, relief=GROOVE,  bg='grey')
framePane.add(frame1)

Label(frame1,text="Entrer un p", bg="#1E90FF").pack(padx=5, pady=5)
spin = Spinbox(frame1, from_=1, to=1000)
spin.pack()
#choix du maillage
ch = StringVar()
ch.set("domaine rectangulaire")
choix = ttk.Combobox(frame1, justify=LEFT, textvariable=ch, values="domaine\ rectangulaire domaine\ triangulaire domaine\ polygonal")
choix.pack(padx=5, pady=15)
Button(frame1, text="valider", bg="#007980", command=genereMaillage).pack(padx=5,pady=5)
Button(frame1, text="sauvegarder", bg="#007980", command=sauvegarder).pack(padx=5,pady=45)

#frame 3
"""Cette frame concerne la saisie de la fonction de temperature à appliquer au maillage"""
frame3 = Frame(None, borderwidth=2, relief=GROOVE, bg='grey')
label = Label(frame3, text="Fonction de température:\n a*x + b*y + c", bg='#7F7F7F', font=2)
label.pack(padx=5, pady=5)

fonct = StringVar()#fonction de temperature
entree = Entry(frame3, textvariable=fonct, width=15, font='Arial 16 italic').pack(padx=5, pady=10)
Button(frame3, text="appliquer", bg='#007980', command=fonctTemp).pack(padx=5,pady=5)

fonction = StringVar()
fonction.set("f(x,y)=")
labelFonct = Label(frame3, textvariable=fonction, font='Arial 16 italic', bg='#007980').pack(padx=5, pady=20)
framePane.add(frame3)

importBtn = Button(frame3, text="importer maillage", command=openFile, bg='#007980', width=15, font='Arial 16 italic').pack(padx=5, pady=10)

#frame2
frame2 = Frame(fenetre, borderwidth=1, relief=GROOVE)
frame2.pack(side=LEFT, padx=5, pady=10)


#ajout bouton de connexion/deconnexion au serveur
varBtnConnect = StringVar()
varBtnConnect.set("Connexion")
btnConnect = Button(frame2, textvariable=varBtnConnect, bg='#007980', command=fonctConnect)
btnConnect.pack(side=TOP,padx=0)

fig = plt.figure()
traceur = fig.add_subplot(111)

canvas = FigureCanvasTkAgg(fig, master=frame2)
canvas.get_tk_widget().pack()

#ajout de la barre de navigation
toolbar = NavigationToolbar2TkAgg(canvas, frame2)
toolbar.update()
canvas._tkcanvas.pack()


fenetre.update() # Suivant le WM. A faire dans tous les cas donc.
fenrw = fenetre.winfo_reqwidth()
fenrh = fenetre.winfo_reqheight()
sw = fenetre.winfo_screenwidth()
sh = fenetre.winfo_screenheight()
fenetre.geometry("%dx%d+%d+%d" % (fenrw, fenrh, (sw-fenrw)/2, (sh-fenrh)/2))


fenetre.protocol("WM_DELETE_WINDOW", on_closing) #action à la fermeture de la fenêtre
fenetre.mainloop()
