import os
from pathlib import Path
from tempfile import TemporaryDirectory
import pytest
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from music21_example_workflow.music21_to_svg import create_note_svg


@pytest.fixture
def images_path_fixture():
    return Path("templating_app/tests/images")


@pytest.fixture
def jpeg_image(images_path_fixture):
    return Path(f"{images_path}/b.jpeg")

@pytest.fixture
def png_image(images_path_fixture):
    return Path(f"{images_path}/a.png")



@pytest.fixture
def generated_note_svg() -> Path:
        yield create_note_svg('C4')

@pytest.fixture(params=[png_image, jpeg_image])
def iter_image_types(request):
    # if isinstance(Path, request.param):
    return request.param


yaml_content = """yaml
    ---
    title: Test Template
    {% if image %}
    image: {{ render_png(image) if image.suffix == '.png' else image }}
    {% endif %}
    description: This is a test template.
    ---
"""

# @pytest.fixture
# @pytest.mark.parametrize("image", [jpeg_image, png_image], ids=['jpeg', 'png', 'svg'])
# def image_in_md(tmp_path, image) -> Path:
#     """Yield a markdown file with the image embedded."""
#     template_path: Path = Path(f"{tmp_path}/template.md")
#     with open(template_path, 'w') as f:
#         f.write(f"[{image.__repr__}]({Path(image)})")
#     f.close()
#     yield template_path

@pytest.fixture
def mock_jinja_template() -> Path:
    with TemporaryDirectory() as tmpdir:
        template_path = Path(tmpdir) / "template.md"
        with open(template_path, 'w') as f:
            template_path.write(yaml_content)
        f.close()
        return str(template_path)

# MEI?  # TODO


# other variables:
#     - size
#     - resolution
#     - number of files
#     - duplicate names