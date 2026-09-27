import unittest

from tools.ttf_to_halley import _apply_antialiasing


class TtfToHalleyTest(unittest.TestCase):
    def test_antialias_off_binarizes_glyph_mask(self) -> None:
        self.assertEqual(
            _apply_antialiasing(bytes((0, 127, 128, 255)), False),
            bytes((0, 0, 255, 255)),
        )

    def test_antialias_on_preserves_grayscale_mask(self) -> None:
        source = bytes((0, 63, 127, 255))
        self.assertEqual(_apply_antialiasing(source, True), source)

    def test_bitmap_gamma_sharpens_grayscale_edges(self) -> None:
        softened = _apply_antialiasing(bytes((64, 128, 192)), True, 1.5)
        self.assertLess(softened[1], 128)
        self.assertLess(softened[2], 192)


if __name__ == "__main__":
    unittest.main()
