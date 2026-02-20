from app.vision.scene_classifier import SceneClassifier
from PIL import Image


def test_scene_classifier_without_refs():
    classifier = SceneClassifier({"scenes": {}}, 0.85)
    img = Image.new("RGB", (10, 10), color="black")
    assert classifier.classify(img) == "transitioning"
