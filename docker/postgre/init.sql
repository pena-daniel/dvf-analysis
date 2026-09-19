-- Exécuté uniquement au premier démarrage (volume dwh-data vide)

-- Couche bronze : données DVF brutes, tout en text.
-- Le typage est fait dans silver avec dbt.
CREATE SCHEMA IF NOT EXISTS bronze;

CREATE TABLE IF NOT EXISTS bronze.dvf (
    identifiant_de_document      text,
    reference_document           text,
    col_1_articles_cgi           text,
    col_2_articles_cgi           text,
    col_3_articles_cgi           text,
    col_4_articles_cgi           text,
    col_5_articles_cgi           text,
    no_disposition               text,
    date_mutation                text,
    nature_mutation              text,
    valeur_fonciere              text,
    no_voie                      text,
    b_t_q                        text,
    type_de_voie                 text,
    code_voie                    text,
    voie                         text,
    code_postal                  text,
    commune                      text,
    code_departement             text,
    code_commune                 text,
    prefixe_de_section           text,
    section                      text,
    no_plan                      text,
    no_volume                    text,
    col_1er_lot                  text,
    surface_carrez_du_1er_lot    text,
    col_2eme_lot                 text,
    surface_carrez_du_2eme_lot   text,
    col_3eme_lot                 text,
    surface_carrez_du_3eme_lot   text,
    col_4eme_lot                 text,
    surface_carrez_du_4eme_lot   text,
    col_5eme_lot                 text,
    surface_carrez_du_5eme_lot   text,
    nombre_de_lots               text,
    code_type_local              text,
    type_local                   text,
    identifiant_local            text,
    surface_reelle_bati          text,
    nombre_pieces_principales    text,
    nature_culture               text,
    nature_culture_speciale      text,
    surface_terrain              text,
    annee                        integer NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_bronze_dvf_annee ON bronze.dvf (annee);

-- Couche bronze : clean layer.
CREATE SCHEMA IF NOT EXISTS silver;

-- Couche gold : Bussiness layer.
CREATE SCHEMA IF NOT EXISTS gold;