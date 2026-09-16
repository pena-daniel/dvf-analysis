reproduire stream estate avec power BI [https://stream.estate/fr/prix-immobilier/france/paris]

- techno : 
 - docker
 - python (extraction et chargement dans minio et dans la couche raw)
 - dbt (transformation)
 - postgres (wharehouse)
 - airflow
 - minio
 - power BI
 - git / github - gitlab




1- mettre en place minio avec Docker
2- mettre en place le script pour charger les données de raw vers minio
3- ajouter postgres dans docker
4- ajouter un script pour quitter de minio a pg

ajout de dep :  pip freeze > requirements.txt