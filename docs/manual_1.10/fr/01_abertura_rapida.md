# Ouvrir le programme (écran de démarrage)

> Manuel de l'utilisateur → Chapitre « Installation et première exécution » → après « Ouvrir le programme ».

À l'ouverture de ROA, un petit écran apparaît avec le logo et une ligne de
signal qui se dessine. En dessous, en toutes lettres, le programme dit ce qu'il
est en train de faire (« Chargement des bibliothèques… », « Préparation de
l'écran d'accueil… »). Cet écran disparaît de lui-même dès que l'écran d'accueil
est prêt ; il n'y a rien à cliquer.

**Première ouverture après une installation ou une mise à jour.** Le programme
est préparé une seule fois (l'écran indique « Préparation du programme pour la
première fois… ») et garde le résultat dans le dossier `.roa_cache`, à côté du
programme. Les fois suivantes, l'ouverture est bien plus rapide. Si le dossier
du programme n'autorise pas l'écriture (par exemple dans `Programmes`), le cache
va dans le dossier de l'utilisateur (`%LOCALAPPDATA%\ROA\cache`). Effacer ce
dossier ne pose aucun problème : il est recréé à l'ouverture suivante.

**Si l'écran de démarrage gêne** (par exemple dans une automatisation ou sur un
ordinateur ayant un problème vidéo), ouvrez le programme avec l'option
`--sem-splash` ou définissez la variable d'environnement `ROA_SEM_SPLASH=1`.

**Mises à jour.** Dans *Aide → Vérifier les mises à jour*, le programme continue
à ne télécharger que son propre code, sans jamais envoyer vos données. À partir
de cette version, il peut aussi mettre à jour le lanceur
(`EEG_Data_Collector.py`) lorsque la mise à jour en apporte une nouvelle
version ; s'il n'y parvient pas, il prévient et le programme continue de
fonctionner avec le lanceur actuel.
