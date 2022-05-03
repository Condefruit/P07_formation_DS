## Projet 07 du parcours Data Scientist (OpenClassrooms)

-------------------

### Implémentez un modèle de scoring

Data Scientist au sein de la société "Prêt à dépenser”, qui propose des crédits à la consommation pour des personnes ayant peu ou pas du tout d'historique de prêt, les objectifs sont de :

:one: Mettre en œuvre un outil de « scoring crédit » <br>
:two: Classifier la demande en crédit accordé ou refusé <br>
:three: Implémenter un tableau de bord intéractif pour les chargés de clientelle (avec données clients et transparence de la décision) <br>.
à partir de données clients ayant contracté des prêts bancaires et classifié en "bon client" (0) ou "mauvais client" (1 : retard ou défaut de paiement). <br>
Les données sont accessibles dans différentes base de données comprenants des : <br>
données comportementales <br>
données provenant d'autres institutions financières, <br>
etc <br>

--------------------------

#### Prétraitement:

Version simple utilisant uniquement la base de donnée principale (inspiré du script de [Will Koehrsen](https://www.kaggle.com/code/willkoehrsen/start-here-a-gentle-introduction/notebook)) sur KAGGLE ) <br>
Liens vers le [script](https://github.com/Condefruit/P07_formation_DS/blob/main/P7_Data_Analysis_main_database_only.ipynb)
Version plus avancée utilisant toutes les bases de données (inspiré du script d'[AGUIAR](https://www.kaggle.com/jsaguiar/lightgbm-with-simple-features) sur KAGGLE. <br>
Liens vers le [script](https://github.com/Condefruit/P07_formation_DS/blob/main/P7_Data_Analysis_full_database.ipynb) <br>

#### Modélisation

La base de donnée est très déséquilibrée en terme de cible, 91.2 % de bon clients, il faut donc prendre en compte se déséquilibrage en terme de choix de modèle et de score d'évaluation. <br>
Voir le script

---------------------------


<!-- Creation d'un score de perte en montant avec des valeurs arbitraires de pertes en fonction de l'erreur.
Voir fonction 'Loss Score'

Determination des seuils en se basant sur les valeurs de pertes. Rappel: n'étant pas banquier, je ne peux garantir que les seuils soient cohérents avec une vision métier, la fonction de perte ainsi que les seuils doivent être réalisés avec un expert bancaire
Voir le script

Dashboard
Le dashboard est réalisé avec le script dash_board.py qui fonctionne avec le framework streamlit. Streamlit lit le fichier via github. Ensuite, les données sont chargées en cache via AWS s3. Les prédictions et les explications du modèle sont générées via des requêtes POST vers une API hébergée sur heroku qui accède aux scripts et au modèle via github également.

Le dashboard présente donc le score prédit par le modèle et les variables les plus explicatives. Par ailleurs, on dispose aussi d'un histogramme permettant de visualiser la repartition d'une variable et la postition du client ciblé par rapport aux autres -->
