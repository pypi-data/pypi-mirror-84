import json
import os

import torch
from bentoml.exceptions import InvalidArgument
from bentoml.service import BentoServiceArtifact

from torchmoji.model_def import torchmoji_emojis


class TorchmojiModelArtifact(BentoServiceArtifact):

    def __init__(self, name):
        super(TorchmojiModelArtifact, self).__init__(name)
        self._model = None

    def _file_path(self, base_path):
        return os.path.join(base_path, self.name)
    
    def _load_from_directory(self, path):
        emoji_list = []
        with open(os.path.join(path, 'emoji_list.txt'), 'r') as f:
            for line in f:
                emoji_list.append(line.strip())

        pax_list = []
        with open(os.path.join(path, 'pax_list.txt'), 'r') as f:
            for line in f:
                pax_list.append(line.strip())
        
        with open(os.path.join(path, 'vocabulary.json'), 'r') as f:
            vocabulary = json.load(f)

        model = torchmoji_emojis(os.path.join(path, 'pytorch_model.bin'))
        self._model = {
            'model': model,
            'emoji_list': emoji_list,
            'pax_list': pax_list,
            'vocabulary': vocabulary,
        }

    def pack(self, model):
        if isinstance(model, str):
            if os.path.isdir(model):
                self._load_from_directory(model)
        
        if self._model is None:
            raise InvalidArgument('Expecting a path')

        return self
    
    def load(self, path):
        path = self._file_path(path)
        return self.pack(path)
    
    def save(self, dest):
        path = self._file_path(dest)
        os.makedirs(path, exist_ok=True)

        with open(os.path.join(path, 'vocabulary.json'), 'w') as f:
            json.dump(self._model['vocabulary'], f)

        with open(os.path.join(path, 'pax_list.txt'), 'w') as f:
            for line in self._model['pax_list']:
                f.write('%s\n' % line)

        with open(os.path.join(path, 'emoji_list.txt'), 'w') as f:
            for line in self._model['emoji_list']:
                f.write('%s\n' % line)

        torch.save(self._model['model'].state_dict(), os.path.join(path, 'pytorch_model.bin'))

    def get(self):
        return self._model
