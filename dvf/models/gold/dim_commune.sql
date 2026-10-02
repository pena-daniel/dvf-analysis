 with libelles as (
 select code_insee , code_departement , code_commune , libelle_commune , count(*) as nb_transaction 
 from {{ref('dvf')}}
 group by 1 , 2, 3 ,4
 ), 
 classement as (
 select * , row_number() over (partition by code_insee order by nb_transaction desc ) as rang 
 from libelles 
 )
 select code_insee , code_departement , code_commune , libelle_commune from classement classement 
 where rang = 1