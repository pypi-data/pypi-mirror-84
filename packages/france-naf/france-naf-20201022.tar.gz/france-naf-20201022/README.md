# python-fr-naf

Python accessors to NAF/APE codes.

From https://www.insee.fr/fr/information/2406147

## Installation

    pip install france-naf


## Usage

    from naf import DB
    # Get one NAF object
    my_naf = DB["02.30Z"]
    print(my_naf)
    # "Récolte de produits forestiers non ligneux poussant à l'état sauvage"
    "02.30Z" in DB
    # True
    print(my_naf.section)
    # A
    # Iter over NAF objects
    for naf in DB:
        do_something_with(naf)
    # Iter over code, description
    for code, description in DB.pairs():
        pass
    # Get the whole DB as a json string
    str(DB)
