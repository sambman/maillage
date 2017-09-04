GROUPE 11 Mohamed SAMB et Mansour Baro DIOP

Designed by Mohamed SAMB

1)Idée du projet
	Ce projet est une simulation de la méthode de résolution itérative avec les calculs numériques. Il s'agit de mettre en oeuvre
	une application qui suit l'architecture client-serveur faisant le maillage des domaines triangulaire, rectangulaire et polygonal.
	Pour ce dernier, le travail n'a pas été totalement achevé à cause d'une contrainte temporel.

2)Fonctionnalités

	-Le serveur fournit un maillage à l'utilisateur qui se connecte. En effet, une connection au préalable avec le serveur doit être
	faite par le client.
	
	-L'utilisateur peut demander au serveur à ce qu'il stocke le maillage en local. Il peut aussi exporter le maillage au format ".png".
	Pour le maillage polygonal, tout le travail n'a pas été achevé
	
	-L'utilisateur peut, s'il le désire entrer une fonction de température qui calculera les intégrales au niveau de chaque maillon.
	Par la suite, on établit une correspondance entre une valeur d'intégrale et une couleur.
	
	-L'utilisateur peut aussi importer les fichiers de coordonnées et des numéros de sommets afin de tracer le maillage correspondant.
	Ces fichiers sont préalablement stockés en local par le serveur via un socket.
