import pandas as pd
from itertools import product
import dendropy

def make_pairs(species_csv_path, newick_path, output_csv_path, exclude_self_pairs=True, shuffle=True):
    # Load species and image paths
    df_species = pd.read_csv(species_csv_path)

    # Load the phylogenetic tree
    tree = dendropy.Tree.get(path=newick_path, schema="newick")
    pdm = tree.phylogenetic_distance_matrix()

    # Create all ordered species pairs
    all_pairs = list(product(df_species.iterrows(), repeat=2))
    records = []

    for (i1, row1), (i2, row2) in all_pairs:
        species1 = row1["species"]
        species2 = row2["species"]

        if exclude_self_pairs and species1 == species2:
            continue

        img1 = row1["image"]
        img2 = row2["image"]

        try:
            tax1 = tree.find_node_with_taxon_label(species1).taxon
            tax2 = tree.find_node_with_taxon_label(species2).taxon
            distance = pdm.distance(tax1, tax2)
        except Exception as e:
            print(f"Warning: Could not find distance between {species1} and {species2}: {e}")
            continue

        records.append({
            "species1": species1,
            "species2": species2,
            "image1": img1,
            "image2": img2,
            "distance": distance
        })

    df_pairs = pd.DataFrame(records)

    if shuffle:
        df_pairs = df_pairs.sample(frac=1).reset_index(drop=True)

    df_pairs.to_csv(output_csv_path, index=False)

# Example usage
if __name__ == "__main__":
    make_pairs(
        species_csv_path="species_images.csv",
        newick_path="tree_file.nwk",
        output_csv_path="species_pairs.csv",
        exclude_self_pairs=True,
        shuffle=True
    )
