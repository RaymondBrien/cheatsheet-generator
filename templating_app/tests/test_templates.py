# import pytest
import pytest
from pathlib import Path
# def test_render_image_in_template(iter_image_types, image_in_md):
#     image_file = image_in_md(iter_image_types)
#     assert image_file.exists()
#     with open(image_file, 'r') as f:
#         content = f.read()
#         assert str(iter_image_types) in content
#     f.close()


images_path = Path("templating_app/tests/images")
png_image = Path(f"{images_path}/a.png")
jpeg_image = Path(f"{images_path}/b.jpeg")

@pytest.mark.parametrize("image", [png_image, jpeg_image], ids=['png', 'jpeg'])
def test_render_image_in_template(image, tmp_path):
    template_path: Path = Path(f"{tmp_path}/template.md")
    with open(template_path, 'w') as f:
        f.write(f"![{image.__repr__}]({Path(image)})")
    f.close()
    assert template_path.exists()
    with open(template_path, 'r') as f:
        content = f.read()
        assert str(image) in content
    f.close()

def test_svg_returned_from_note_object(generated_note_svg):
    assert generated_note_svg.startswith('<svg')