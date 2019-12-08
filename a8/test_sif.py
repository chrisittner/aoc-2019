from .sif import SIFImage

test_img = SIFImage("123456789012", width=3, height=2)


def test_sifimage_layer_data():
    assert test_img.layers == ["123456", "789012"]
    assert test_img.layer_with_fewest_0s == "123456"
    assert test_img.part1() == 1


def test_part1():
    with open("input_a8") as fp:
        assert SIFImage(fp.read().strip(), width=25, height=6).part1() == 2048


def test_composed_image():
    img = SIFImage("0222112222120000", 2, 2)
    assert img.composed_image == list("0110")
