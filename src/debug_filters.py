from filters import filter_by_min_genes, filter_by_type

regulon = {
    "CRP": {
        "genes": ["lacZ", "cyaA"],
        "activados": 1,
        "reprimidos": 1,
    },
    "FNR": {
        "genes": ["narG"],
        "activados": 0,
        "reprimidos": 1,
    },
}

print(filter_by_min_genes(regulon, 2))
print(filter_by_type(regulon, "dual"))