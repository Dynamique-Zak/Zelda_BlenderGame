#Zelda_BlenderGame

A zelda fan made with Blender Game Engine. I used more 80% python. This game is in development and you can help.
##Video

Video dated August 16, 2014 : [Zelda Awakening in Blender Game](https://www.youtube.com/watch?v=BOBg3g-WLesZelda)

[Zelda In Blender game - Fight test](https://www.youtube.com/watch?v=ndbULJvf4Bo)

##Environnement Work

LINUX/UNIX - XUbuntu 64 bits

##Notice

###Pygame

You must install pygame into your Blender version. For me i have Blender 2.76 and i set pygame module at :
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

##Gamepad

	Deplacements : Arrow Keys | Joystick analogique
	Z Button (Targeting mode) : W | R2
	A Button : X | Left Button
	Attack Button : C | Bottom Button


##Updates

	Mouvements sur la vidéo, mais depuis j'ai enlevé les mouvements suivants pour les re-développer:
	Push sur les bloc
	La montée sur les bloc
	Transition entre map

##08 Janvier 2016

	Path Follow (Suit un chemin, comme pour changer de map)
	Système de dialogue
	Système de menu
	Gestion de logic.globalDict pour charger les données à chaque transition de map
	Intégration pygame.joystick pour detecter les manettes

###09 Janvier 2016

	Rotation de joueur adapté au joystick et à la camera
	Rotation caméra libre avec le joystick droit
	Début du Z-Targeting
	Amélioration de l'armature du joueur et certaines animations on été améliorés (il en reste encore) par luky que je remerci sur la passage
	Sort de l'eau à partir d'un corniche ou du sol
	Re-Développement de la gestion des steps sounds (Bruitage des pieds au sol)
	Interaction avec des pancartes (Affiche une messageBox)

###12 Janvier 2016

	Debut des applications des méthodes avec callback ou décorateur. Exemple:
```
    def respectGroundRule(self, function):
      from link_scripts.StarterState import start_fallState

          if (self.physic.detectGround()):
              return True
          else:
              # call function
              function(self)
              # go to fall
              start_fallState(self)
              return False
```
	Curseur du viseur ajouter, situé sur la scene HUD, position adapté aux coordonnées de l'objet ciblé dans la scene du joueur. (Utilisation de la methode getScreenPosition(monObjet) de la class KX_Camera)

###18 Janvier 2016
	Système d'attaque
	Système Hits
	Strike Effect
	MiniMap (premier test)

###A faire (en priorité)
	Gestion d'une caméra intélligente (Obstacle, etc)
	Le fall down lorsque le joueur est coincé
	Finir/Refaire les animations courantes du personnage

###Bugs reconnues

    Pendant l'etat de fall, il se peut que le personnage reste coinçé dans le sol ou un mur
    Detection de l'eau non compléte (lorsque le joueur tombe asser rapidement, le rayCast ne detect pas l'eau). Solution envisagée, detecter l'eau au dessus de perso pour gerer le cas précédent.
    Pendant la visée, le joueur ne detecte pas l'eau
    Je n'ai pas encore gerer le TAP dans les bouttons du joystick
    Pendant la jump attack, comme pour fall risque d'être coincée
Notes

    Il y a des animations à refaire (Suite à la modification de l'armature)

##Copyright

All contained owned by Nintendo (Characters, Story, etc.) reserved to it
