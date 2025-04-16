import pandas as pd
from torch.utils.data import Dataset
from PIL import Image

class SpeciesPairDataset(Dataset):
    def __init__(self, csv_path, transform=None):
        self.pairs = pd.read_csv(csv_path)
        self.transform = transform

    def __len__(self):
        return len(self.pairs)

    def __getitem__(self, idx):
        row = self.pairs.iloc[idx]
        img1 = Image.open(row['image1']).convert("RGB")
        img2 = Image.open(row['image2']).convert("RGB")
        distance = float(row['distance'])
        species_names = (row['species1'], row['species2'])

        if self.transform:
            img1 = self.transform(img1)
            img2 = self.transform(img2)

        return (img1, img2), distance, species_names
