#Zelda_BlenderGame [Mise à jour du 17-02-2016]

Voici un zelda fan make sur le Blender Game Engine. Une majorité du développement à été fait avec du Python.

A zelda fan made with Blender Game Engine. I used more 80% python. This game is in development and you can help.
##Video

Video dated August 16, 2014 : [Zelda Awakening in Blender Game](https://www.youtube.com/watch?v=BOBg3g-WLesZelda)

Video dated January 18, 2016 : [Zelda In Blender game - Fight test](https://www.youtube.com/watch?v=ndbULJvf4Bo)

Video dated February 17, 2016 : [Zelda in blender game Update 17-03-2016](https://www.youtube.com/watch?v=ndbULJvf4Bo)

##Environnement de travail

LINUX/UNIX - XUbuntu 64 bits

##Outils

- Graphisme2D/Texture : Gimp
- Modélisation, Texturage, Animations : Blender 3D
- Moteur de jeu : BGE
- Langage de programmation : Python

##Notice

###Pygame

You must install pygame into your Blender version if you want play with joystick. For me i have Blender 2.76 and i set pygame module at :
```
blender_2.76
  \2.76
    \python
      \lib
        \python3.4
```

You download, build and install pygame for python3.x, and after copy the pygame librairie which are on this folder
```
/usr/local/include/python3.x/pygame
```

Paste into
```
blender_2.76/2.76/python/lib/python3.4/pygame
```

Help Links:

[Ask Ubuntu - Install pygame 3.0](http://askubuntu.com/questions/401342/how-to-download-pygame-in-python3-3)

###Others

I haven't packed textures and other files in blends files. If blends can't find ressources, please check into File menu "External Data > Missing Files".

##Concept du développement sur le BGE
On utilise le dictionnaire globalDict pour stocker les valeurs pendant le fonctionnement du jeu et pour sauvegarder des parties. Lors du premier lancement d'une partie, on initialise le dictionnaire.

Le dictionnaire est utilisé pour l'inventaire, le status du joueur, les enclencheurs dans les niveaux, etc.

`Quand je parle d'enclencheur, il sagit bien entendu des objets interactifs tel que les coffres, les portes, etc.`

##Gamepad

Les contrôles peuvent s'effectuer à partir d'une manette ou d'un clavier. Afin de pouvoir utiliser la manette veuillez être sûr d'avoir pygame intégré dans le BGE.

####Pour ce qui n'ont pas pygame importé sur Blender

Afin de pouvoir jouer sans pygame, un fichier conf.txt situé à la racine de projet contient les configuration du jeu.
Veuillez preciser l'utilisation du joystick (pygame)

`0 pour desactiver et 1 pour activer`

- Deplacements : Arrow Keys | Joystick analogique
- Z Button (Targeting mode) : W | R2
- A Button : X | Left Button
- Attack Button : C | Bottom Button

##Gestionnaire du projet

Le repertoire `dx_ge` contient les scripts python nécessaire au fonctionnement du gestionnaire.
Il suffit à partir du script `manager.py` de renseigner la commande à utiliser.

###Doc du gestionnaire
####Convention dans les nommages
Un etat commence par une majuscule, chaque syllabe commence par une majuscule
`Exemple: MonEtat`

Les fonctionnalités des etats commence par une miniscule, chaque syllabe qui suit la premère devront commencer par une majuscule
`Exemple: maFonction`

####Fonctionnement du gestionnaire
- Ajouter un état au joueur : `create_player_state MonEtat`
- Ajouter une fonctionnalité à un etat au joueur : `player_state:add:MonEtat:maFonction`

Exemple:
`python manager.py create_player_state Ledge`
`python manager.py player_state:add:Ledge:grapLedge`

##Fonctionnement
###Coffres
Les coffres sont des objets groupés linké dans les niveaux. Afin de déterminer l'attribut 'objectID' et key' d'un coffre, on l'ajoute à partir d'un Empty object a l'aide `leCoffre = scene.addObject('monCoffre', own)`. Etant donné que cette fonction retourne l'object instancié il suffit juste de le récuperer comme montré précedement et lui affecter les attributs tel que:
`leCoffre['objectID'] = monId`

Graçe a cette méthode on peut assigner l'id d'un objet à partir de constantes qu'on aura définie à l'initialisation du jeu.

`Note: L'attribut 'objectID' référence l'objet qu'il contient et 'key' permet d'identifier si le coffre à déjà été ouvert`

###Les portes
Il sagit de la même méthode que pour les coffres, on ajoute les portes l'aide de `scene.addObject`, ainsi il est possible de déterminer quelle clef permet d'ouvrir la porte instancié (si il sagit bien d'une porte verrouillé)

`Remarque: Graçe a cette méthode, on peut aussi savoir si la porte à déjà été ouverte a l'aide d'un attribut 'key' (comme pour le coffre)`

##08 Janvier 2016

- Path Follow (Suit un chemin, comme pour changer de map)
- Système de dialogue
- Système de menu
- Gestion de logic.globalDict pour charger les données à chaque transition de map
- Intégration pygame.joystick pour detecter les manettes

###09 Janvier 2016

- Rotation de joueur adapté au joystick et à la camera
- Rotation caméra libre avec le joystick droit
- Début du Z-Targeting
- Amélioration de l'armature du joueur et certaines animations on été améliorés (il en reste encore) par luky que je remerci sur la passage
- Sort de l'eau à partir d'un corniche ou du sol
- Re-Développement de la gestion des steps sounds (Bruitage des pieds au sol)
- Interaction avec des pancartes (Affiche une messageBox)

###12 Janvier 2016

- Curseur du viseur ajouter, situé sur la scene HUD, position adapté aux coordonnées de l'objet ciblé dans la scene du joueur. (Utilisation de la methode getScreenPosition(monObjet) de la class KX_Camera)

###18 Janvier 2016

- Système d'attaque
- Système Hits
- Strike Effect
- MiniMap (premier test)

###17 Fevrier 2016

- Fichier de configuration (Desactiver l'utilisation de pygame par exemple)
- Système d'équipement (Boucliers, Epees)
- Système Push des blocs
- Coffre au trésor
- Amélioration du GrapLedge
- Système d'esquive
- Génération d'objet sur les herbes coupées
- GameOver
- Gestionnaire du projet developpé en python [Bêta]

###A faire (en priorité)
- Le fall down lorsque le joueur est coincé
- Finir/Refaire les animations courantes du personnage

###Bugs reconnues

- Pendant l'etat de fall, il se peut que le personnage reste coinçé dans le sol ou un mur
- Pendant la visée, le joueur ne detecte pas l'eau
- Je n'ai pas encore gerer le TAP dans les bouttons du joystick
- Pendant la jump attack, comme pour fall risque d'être coincée
Notes:

Il y a des animations à refaire (Suite à la modification de l'armature)

##Credits

- Schartier Isaac (Project Master - Developer - Texture - Animations - Modelisation - Scenario)
- Henri Nourel (Collaborateur)
- Lucky (Animations 3D)
- Derys Onapin (Dessinateur, Scenario)

##Copyright

All contained owned by Nintendo (Characters, Story, etc.) reserved to it
