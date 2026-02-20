from app.vision.boat_suppression import keep_car


def test_keep_car_filters_horizon():
    assert not keep_car({"bbox": [10, 10, 100, 40], "center_in_roi": True}, 100, (1, 4), (100, 10000))
