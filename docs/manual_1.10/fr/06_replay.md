# Replay : voir l'enregistrement comme une animation

> Manuel de l'utilisateur → Chapitre « Revoir un enregistrement » → nouvelle section « Replay » (après « Rapport PDF »).

À l'ouverture d'un enregistrement de **muscles**, de **cœur** ou d'**yeux**, le
bouton **▶ Replay** devient disponible (il reste désactivé pour les
enregistrements du cerveau). Il ouvre une fenêtre avec un lecteur commun aux
trois examens : **▶ Lecture / ⏸ Pause**, **⏮ Début**, la ligne de temps que
l'on fait glisser et l'horloge « 0:05 / 0:30 ». Au niveau Complet s'ajoutent la
vitesse (de 0,25× à 4×) et *Répéter*.

> L'animation **simule** ce qui a été enregistré : ce n'est pas la vidéo de la
> personne, et ce n'est ni un compte rendu ni un diagnostic. Le bandeau en haut
> de la fenêtre le rappelle.

## Muscles

Une silhouette articulée vue de côté (tronc, épaule, coude, avant-bras,
poignet, main avec les doigts) refait le **mouvement marqué** sur la ligne de
temps, et chaque muscle s'allume avec l'intensité mesurée à cet instant.
Supination et pronation sont impossibles à confondre : la paume claire tournée
vers le haut ou le dos de la main tourné vers le bas, avec le texte « paume vers
le haut/le bas ».

La ligne de temps (2 à 4 pistes) naît des **marqueurs et des phases** de
l'enregistrement (« Flexion », « Extension », « Repos »…) ; sans marqueur, les
**contractions détectées** deviennent des segments « à définir ». Les pistes au
même instant s'**additionnent** (par exemple, fermer la main pendant que le
coude fléchit). Mouvements disponibles : flexion et extension du coude,
supination, pronation, flexion et extension du poignet, ouvrir et fermer la
main, pince, flexion et extension de l'épaule, repos.

Au niveau **Simple**, vous voyez le lecteur, la silhouette et la liste des
segments. Au niveau **Complet**, la ligne de temps est modifiable : faites
glisser un bloc pour le déplacer, tirez son bord pour l'étirer, cliquez avec le
bouton droit pour *Changer le mouvement*, *Scinder ici*, *Effacer*,
*Ajouter/Supprimer la piste* ; Ctrl+Z annule. *Tâche prête* insère, à partir du
curseur, une séquence avec l'objet tenu dans la main : **soulever l'haltère**,
**ouvrir/fermer la porte avec la clé**, **prendre le verre sur la table et le
porter à la bouche**. Quand les muscles actifs ne correspondent pas au
mouvement choisi (par exemple, triceps actif dans un segment de flexion), un
avertissement apparaît. *Sauvegarder* écrit `movimentos.json` à côté de
l'enregistrement ; à la fermeture, le programme demande s'il reste des marquages
non sauvegardés.

## Cœur

Un cœur dessiné **bat au rythme enregistré**, à côté du tracé avec le curseur
et des battements par minute. La bande du bas montre **tous** les battements :
le battement régulier est un trait fin ; le **battement en avance** est un
triangle orange ; la **pause plus longue** est un rectangle rouge évidé
(couleur et forme, pour qui ne distingue pas les couleurs). La liste en toutes
lettres (« 0:13 battement en avance », « 0:25 pause plus longue (1,7 s) ») est
cliquable et amène le lecteur à cet endroit. Les battements sont les mêmes que
dans le rapport PDF. Au niveau Complet, le bouton droit sur la bande permet de
**corriger** (supprimer le battement, ajouter un battement ici, marquer comme
régulier / en avance / pause plus longue) ; *Sauvegarder* écrit `batidas.json`.

## Yeux

Deux yeux dessinés **clignent aux clignements et regardent** là où les signaux
l'indiquent. *Inverser l'horizontal* et *Inverser le vertical* échangent les
côtés, au cas où les électrodes auraient été posées à l'envers. La ligne de
temps dit en toutes lettres ce qui s'est passé (« 0:03 a cligné des yeux »,
« 0:05 a regardé à droite ») et les compteurs additionnent les clignements et
les mouvements sur les côtés et en haut/en bas. Au niveau Complet, le bouton
droit sur la liste supprime un événement ou change la direction ; *Sauvegarder*
écrit `olhos.json`.
