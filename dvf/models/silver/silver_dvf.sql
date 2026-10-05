with with_numerote as (
    select *,
           row_number() over (
               partition by date_mutation, code_departement, code_commune, no_disposition, valeur_fonciere
               order by section, no_plan, identifiant_local
           ) as rang
    from {{ source('bronze', 'dvf') }}
)
select 
    {{ dbt_utils.generate_surrogate_key(['date_mutation', 'code_departement', 'code_commune', 'no_disposition', 'valeur_fonciere', 'rang']) }} as id,

    {{ dbt_utils.generate_surrogate_key(['date_mutation', 'code_departement', 'code_commune', 'no_disposition', 'valeur_fonciere']) }} as mutation_key,

    to_date(nullif(date_mutation, ''), 'dd/mm/yyyy') as date_mutation,
    nullif(trim(nature_mutation), '') as nature_mutation,

    cast(nullif(no_disposition, '') as integer) as no_disposition,
    cast(nullif(replace(valeur_fonciere, ',', '.'), '') as numeric(14, 2)) as valeur_fonciere,
    cast(nullif(replace(surface_terrain, ',', '.'), '') as numeric(14, 2)) as surface_terrain,

    nullif(trim(code_departement), '') || lpad(nullif(trim(code_commune), ''), 3, '0') as code_insee,
    nullif(trim(code_departement), '') as code_departement,
    nullif(trim(code_commune), '') as code_commune,
    nullif(trim(commune), '') as libelle_commune,
    lpad(nullif(trim(code_postal), ''), 5, '0') as code_postal,

    cast(nullif(code_type_local, '') as integer) as code_type_local,
    nullif(trim(type_local), '') as type_local,
    
    cast(nullif(surface_reelle_bati, '') as integer) as surface_reelle_bati,
    cast(nullif(nombre_pieces_principales, '') as integer) as nb_pieces_principales,
    cast(nullif(nombre_de_lots, '') as integer) as nb_de_lots,

    annee,
    source_file,
    load_at as load_date

from with_numerote