# URL where data is located (currently on Entropeak's server)
DATA_PATH = "https://entropeak-public-data.s3.eu-west-3.amazonaws.com/enthic/indicateurs_2020_full_20220412.csv"

# list of APE codes to display and available in the application.
# The dictionnary keys are the value displayed on the front end
# and the values are regex to filter data in the dataset.
CODES_APE = {
    "Supermarchés et Hypermarchés": ["^47\.11D", "^47\.11F"],
    "Cultures permanentes": ["^01\.2"],
    "Restauration": ["^56"],
    "Activités liées au sport": ["^93.1"],
    "Industrie automobile": ["^29"],
    "Construction aéronautique et spatiale": ["^30.3"],
}

# Dictionnary use to renames Enthic features to more natural names
FEATURES_NAME_MAPPING = {
    "exploitation_share": "Part du résultat d'exploitation distribuée en participation et impôts",
    "overall_wages_weight": "Part de la masse salariale dans le total des charges d'exploitation",
    "wage_quality": "Ratio entre les cotisations sociales et les salaires",
    "average_wage": "Salaire moyen",
    "profit_sharing": "Part des 3 résultats (exploitation, financier et exceptionnel) distribuée en participation et impôts",
    "exploitation_part": "Part de la partie 'exploitation' dans le total du compte de résultat",
    "data_availability": "Indicateur de bon remplissage de la déclaration comptable",
}

# Enthic features that we'll keep in the data
FEATURES_COLUMNS = [
    "exploitation_share",
    "overall_wages_weight",
    "wage_quality",
    "average_wage",
    "profit_sharing",
    "exploitation_part",
]

# Columns that are not enthic features neither accounting data but that are important for the application
NON_VARIABLES_COLUMNS = [
    "SIREN",
    "Code postal",
    "Commune",
    "code_ape",
    "code_ape_complete",
    "nom",
    "description",
]

# Variables to keep in the dataset, other accounting related columns or Enthic's features will be filtered.
VARIABLES_TO_KEEP = [
    "Bénéfices ou perte (Total des produits ‐ Total des charges)",
    "Impôts sur les bénéfices",
    "Résultat d'exploitation",
    "Total des charges d’exploitation",
    "Salaires et traitements",
    "Charges sociales",
    "Impôts, taxes et versements assimilés",
    "Chiffres d’affaires nets",
    "Subventions d’exploitation",
    "Intérêts et charges assimilées",
    "Produits financiers de participations",
] + [FEATURES_NAME_MAPPING[e] for e in FEATURES_COLUMNS]
