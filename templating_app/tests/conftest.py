import os
from pathlib import Path
from tempfile import TemporaryDirectory
import pytest
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from music21_example_workflow import music21_to_svg

images_path = Path("templating_app/tests/images")
png = images_path.glob("*.png")
jpg = images_path.glob("*.jpg")


@pytest.fixture
def dynamic_music_xml_svg():
    with TemplporaryDirectory() as tmpdir:
        yield music21_to_svg('C4', output_path=os.path.join(tmpdir, "output.svg"))

@pytest.fixture(params=[png, jpg, dynamic_music_xml_svg])
def iter_image_types(request):
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

@pytest.fixture
def render_md() -> Path:
    with TemporaryDirectory() as tmpdir:
        template_path = Path(tmpdir) / "template.md"
        with open(template_path, 'w') as f:
            template_path.write(yaml_content)
        f.close()
        yield str(template_path)

@pytest.fixture
def mock_jinja_template(): -> Path:
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