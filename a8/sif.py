from functools import reduce


class SIFImage:
    def __init__(self, data, width, height):
        self.data = data
        self.width = width
        self.height = height

        self.layers = self._split_layers(data, width, height)

    @staticmethod
    def _split_layers(data, width, height):
        layer_size = width * height
        assert len(data) % layer_size == 0

        return [
            data[ii * layer_size : (ii + 1) * layer_size]
            for ii in range(len(data) // layer_size)
        ]

    @property
    def layer_with_fewest_0s(self):
        return min(self.layers, key=lambda layer: layer.count("0"))

    def part1(self):
        layer = self.layer_with_fewest_0s
        return layer.count("1") * layer.count("2")

    @property
    def composed_image(self,):
        return reduce(self._merge_layers, self.layers)

    @staticmethod
    def _merge_layers(layer1, layer2):
        return [p2 if p1 == "2" else p1 for p1, p2 in zip(layer1, layer2)]

    def __repr__(self):
        image = [" " if pixel is "0" else "X" for pixel in self.composed_image]

        return "\n".join(
            [
                "".join(image[ii * self.width : (ii + 1) * self.width])
                for ii in range(len(image) // self.width)
            ]
        )


if __name__ == "__main__":
    with open("input_a8") as fp:
        print(SIFImage(fp.read().strip(), width=25, height=6))  # HFYAK
