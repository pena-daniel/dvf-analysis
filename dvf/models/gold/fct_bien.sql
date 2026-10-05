SELECT
    id as bien_key,
    {{ dbt_utils.generate_surrogate_key(['date_mutation', 'code_departement', 'code_commune', 'no_disposition', 'valeur_fonciere']) }} AS mutation_key,
    CAST(to_char(date_mutation, 'YYYYMMDD') AS INTEGER) AS date_key,
    COALESCE(code_type_local,-1) AS type_local_key,
    code_postal,
    code_insee,
    annee,
    surface_reelle_bati,
    nb_de_lots,
    nb_pieces_principales,
    surface_terrain,
    load_date
FROM
    {{ ref('silver_dvf') }}