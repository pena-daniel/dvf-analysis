with base as (
    SELECT
        {{ dbt_utils.generate_surrogate_key(['date_mutation', 'code_departement', 'code_commune', 'no_disposition', 'valeur_fonciere']) }} AS mutation_key,
        COALESCE(nature_mutation,'Non renseigné') AS nature_mutation,
        CAST(to_char(date_mutation, 'YYYYMMDD') AS INTEGER) as date_key,
        code_insee,
        annee,
        code_postal,
        valeur_fonciere,
        code_type_local,
        surface_reelle_bati,
        surface_terrain,
        nb_de_lots,
        load_date
    FROM {{ ref('silver_dvf') }}
)

select     
    mutation_key,
    {{ dbt_utils.generate_surrogate_key(['MIN(nature_mutation)']) }} AS nature_mutation_key,
    MIN(nature_mutation) AS nature_mutation,
    date_key,
    code_insee,
    annee,
    MIN(code_postal) AS code_postal,
    MAX(valeur_fonciere) AS valeur_fonciere,
    COUNT(*) AS nb_biens,
    (COUNT(*) filter (WHERE code_type_local IN (1, 2))) AS nb_logements,
    SUM(surface_reelle_bati) AS surface_bati_total,
    SUM(surface_terrain) AS surface_terrain_total,
    SUM(nb_de_lots) AS nb_lots_total,
    MAX(load_date) as load_date
From base
GROUP BY mutation_key,date_key,code_insee,annee