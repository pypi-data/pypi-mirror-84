import json
from pathlib import Path
from typing import Union, Optional

import torch


class CheckpointSaver:
    def __init__(self, path: Union[Path, str]):
        self.path = Path(path)
        self.path.mkdir(parents=True, exist_ok=True)

    def save(self, model, optimizer, scheduler, epoch):
        path = self.path.joinpath(f"epoch_{epoch:05d}.pth")
        print(f"saving model to {path}")
        torch.save(model.state_dict(), path)

        path = self.path.joinpath(f"epoch_{epoch:05d}.optimizer.pth")
        print(f"saving optimizer state to {path}")
        torch.save(optimizer.state_dict(), path)

        path = self.path.joinpath(f"epoch_{epoch:05d}.scheduler.pth")
        print(f"saving scheduler state to {path}")
        torch.save(scheduler.state_dict(), path)

        path = self.path.joinpath(f"epoch_{epoch:05d}.meta.json")
        print(f"saving meta data to {path}")
        with path.open("w") as f:
            json.dump({'epoch': epoch}, f)

    def load(self, model, optimizer, scheduler, epoch):
        path = self.path.joinpath(f"epoch_{epoch:05d}.pth")
        print(f"loading model from {path}")
        model_dict = model.state_dict()
        pretrained_dict = torch.load(path)
        pretrained_dict = {k: v for k, v in pretrained_dict.items() if k in model_dict}
        model_dict.update(pretrained_dict)
        model.load_state_dict(model_dict)

        path = self.path.joinpath(f"epoch_{epoch:05d}.optimizer.pth")
        if path.exists():
            print(f"loading optimizer state from {path}")
            optimizer_dict = torch.load(path)
            optimizer.load_state_dict(optimizer_dict)
        else:
            print("optimizer state not found")

        path = self.path.joinpath(f"epoch_{epoch:05d}.scheduler.pth")
        if path.exists():
            print(f"loading scheduler state from {path}")
            scheduler_dict = torch.load(path)
            scheduler.load_state_dict(scheduler_dict)
        else:
            print("scheduler state not found")

    def find_last(self, start_epoch, end_epoch) -> Optional[int]:
        for epoch in range(end_epoch, start_epoch - 1, -1):
            path = self.path.joinpath(f"epoch_{epoch:05d}.meta.json")
            if path.exists():
                return epoch
        return None
