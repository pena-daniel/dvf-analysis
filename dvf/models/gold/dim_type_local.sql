with types_local as (
    select 
        code_type_local,
        type_local
    from {{ ref('dvf') }}
    group by code_type_local,type_local
)

select 
    coalesce(code_type_local, -1) as type_local_key,
    coalesce(type_local, 'Non renseigné') as type_local,
    case
        when code_type_local in (1, 2) then 'Habitation'
        when code_type_local is null then 'Non renseigné'
        else 'Autre'
    end as categorie

 from types_local   