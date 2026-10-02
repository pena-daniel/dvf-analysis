select distinct 
    {{ dbt_utils.generate_surrogate_key(["coalesce(nature_mutation, 'Non renseigné')"]) }} as nature_mutation_key, 
    coalesce(nature_mutation, 'Non renseigné') as nature_mutation
from {{ ref('dvf') }}