with dates as (

    {{ dbt_utils.date_spine(
        datepart="day",
        start_date="cast('2020-01-01' as date)",
        end_date="cast('2031-01-01' as date)"
    ) }}

)

select
    cast(to_char(date_day, 'YYYYMMDD') as integer)      as date_key,
    cast(date_day as date)                              as date_complete,

    cast(extract(year from date_day) as integer)        as annee,
    cast(extract(quarter from date_day) as integer)     as trimestre,
    cast(extract(month from date_day) as integer)       as mois,
    to_char(date_day, 'YYYY-MM')                        as annee_mois,
    cast(extract(day from date_day) as integer)         as jour,
    cast(extract(week from date_day) as integer)        as semaine_iso,
    cast(extract(isodow from date_day) as integer)      as jour_semaine, -- different de dow qui commence la semaine par 0 (dimanche)

    case extract(month from date_day)
        when 1 then 'Janvier'
        when 2 then 'Février'
        when 3 then 'Mars'
        when 4 then 'Avril'
        when 5 then 'Mai'
        when 6 then 'Juin'
        when 7 then 'Juillet'
        when 8 then 'Août'
        when 9 then 'Septembre'
        when 10 then 'Octobre'
        when 11 then 'Novembre'
        when 12 then 'Décembre'
    end                                                 as mois_libelle,

    case extract(isodow from date_day)
        when 1 then 'Lundi'
        when 2 then 'Mardi'
        when 3 then 'Mercredi'
        when 4 then 'Jeudi'
        when 5 then 'Vendredi'
        when 6 then 'Samedi'
        when 7 then 'Dimanche'
    end                                                 as jour_semaine_libelle,

    extract(isodow from date_day) in (6, 7)             as est_weekend

from dates