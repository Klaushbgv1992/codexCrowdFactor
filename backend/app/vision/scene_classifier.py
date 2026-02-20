from __future__ import annotations

from pathlib import Path

import imagehash
from PIL import Image


class SceneClassifier:
    def __init__(self, scenes_cfg: dict, threshold: float = 0.85):
        self.threshold = threshold
        self.refs = {}
        for scene_id, scene_cfg in scenes_cfg.get("scenes", {}).items():
            hashes = []
            for ref in scene_cfg.get("reference_frames", []):
                p = Path(ref)
                if p.exists():
                    hashes.append(imagehash.phash(Image.open(p)))
            if hashes:
                self.refs[scene_id] = hashes

    def classify(self, frame_pil: Image.Image) -> str:
        if not self.refs:
            return "transitioning"
        frame_hash = imagehash.phash(frame_pil)
        best_scene = "transitioning"
        best_sim = 0.0
        for scene_id, hashes in self.refs.items():
            for h in hashes:
                sim = 1 - (frame_hash - h) / len(frame_hash.hash) ** 2
                if sim > best_sim:
                    best_sim = sim
                    best_scene = scene_id
        return best_scene if best_sim >= self.threshold else "transitioning"
