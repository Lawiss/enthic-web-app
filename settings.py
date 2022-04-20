DATA_PATH = "https://entropeak-public-data.s3.eu-west-3.amazonaws.com/enthic/indicateurs_2020_full_20220412.csv"

CODES_APE = {
    "Supermarchés et Hypermarchés": ["^47\.11D", "^47\.11F"],
    "Cultures permanentes": ["^01\.2"],
    "Restauration": ["^56"],
    "Activités liées au sport": ["^93.1"],
    "Industrie automobile": ["^29"],
    "Construction aéronautique et spatiale": ["^30.3"],
}

FEATURES_NAME_MAPPING = {
    "exploitation_share": "Part du résultat d'exploitation distribuée en participation et impôts",
    "overall_wages_weight": "Part de la masse salariale dans le total des charges d'exploitation",
    "wage_quality": "Ratio entre les cotisations sociales et les salaires",
    "average_wage": "Salaire moyen",
    "profit_sharing": "Part des 3 résultats (exploitation, financier et exceptionnel) distribuée en participation et impôts",
    "exploitation_part": "Part de la partie 'exploitation' dans le total du compte de résultat",
    "data_availability": "Indicateur de bon remplissage de la déclaration comptable",
}

FEATURES_COLUMNS = [
    "exploitation_share",
    "overall_wages_weight",
    "wage_quality",
    "average_wage",
    "profit_sharing",
    "exploitation_part",
]

NON_VARIABLES_COLUMNS = [
    "SIREN",
    "Code postal",
    "Commune",
    "code_ape",
    "code_ape_complete",
    "nom",
    "description",
]
