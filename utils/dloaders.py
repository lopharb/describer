import random
from torch.utils.data import DataLoader
import os
import pandas as pd
from PIL import Image


class TextLoader(DataLoader):
    pass


class PairLoader(DataLoader):
    def __init__(self, dataset_folder: str, *args, **kwargs):
        super(PairLoader, self).__init__(*args, **kwargs)
        self.source = dataset_folder
        self.image_dir = os.path.join(self.source, 'flickr30k_images')
        self.image_list = list(os.listdir(self.image_dir))
        self.captions = pd.read_csv(os.path.join(self.source, 'results.csv'))
        self.captions = self.captions.rename(columns={' comment': 'comment'})
        self.captions = self.captions.rename(
            columns={' comment_number': 'comment_number'})

    def __getitem__(self, index):
        filename = self.image_list[index]
        image = Image.open(os.path.join(self.image_dir, filename))
        mask = self.captions['image_name'] == filename
        rand_num = random.randint(1, 100)
        description = self.captions[mask]
        tokens = self._split_tokens(description)
        # TODO

    def _split_tokens(self, text: str) -> list[str]:
        return ['<START>'] + text.split() + ['<EOS>']
