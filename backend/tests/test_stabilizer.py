from app.vision.stabilizer import CountStabilizer


def test_stabilizer_median():
    s = CountStabilizer(180)
    s.add_reading("beach", 100, 2)
    s.add_reading("beach", 101, 20)
    s.add_reading("beach", 102, 6)
    assert s.get_stable_count("beach") == 6
