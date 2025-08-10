import os
import pytest
import anthropic
from pathlib import Path

from prompt_templates.prompt_config import Role
from prompt_templates.default_prompt import DefaultPrompt
from config.API_CONFIG import MAX_TOKENS

# Skip tests that require API initialization
pytestmark = pytest.mark.skip_api


def test_default_starts_with_matched_topic_file(dict_to_yaml):
    topic = 'mock_topic'
    mock_topic_file_path = Path(f'topics/{topic}.yml')  # topic file name should match topic string on DefaultPrompt init
    yaml_content = {
        'Topic': topic,
        'Subtopics': ['subtopic1', 'subtopic2'],
        'Docs': ['doc1', 'doc2']
    }
    dict_to_yaml(yaml_content, mock_topic_file_path)

    default_prompt = DefaultPrompt(topic=topic)  # topic file should be found automatically  # TODO is this stable or should user specify path?
    assert default_prompt.topic_file == mock_topic_file_path

def test_update_role_in_default_prompt():
    """
    Default prompt should update role when changed.
    """
    default_prompt = DefaultPrompt(topic='test topic')
    assert default_prompt.role == Role().default

    new_role = "new custom role"
    default_prompt.update_role(new_role)
    assert default_prompt.role == new_role

@pytest.mark.parametrize("topic", ['test topic', '1', 'A REALLY LONG TEST TOPIC', '123 abc', 'language', '', '  '])
def test_default_topic_sanitisation(topic):
    """
    Default prompt should init with a sanatized specified topic name,
    even if a file doesn't exist for it.
    Empty strings should raise a value error
    """
    if topic == ' ' or topic.strip() == '':
        with pytest.raises(ValueError):
            DefaultPrompt(topic=topic)
        return  # continue testing the other values

    default_prompt = DefaultPrompt(topic=topic)
    assert default_prompt.topic == str(topic.lower().replace(" ", "_"))
    print(f"Default topic file: {default_prompt.topic_file}")
    assert default_prompt.topic_file is None  # No file should be matched if it doesn't exist

def test_default_prompt_initialization():
    default_prompt = DefaultPrompt(topic='test topic')
    assert isinstance(default_prompt.main_text, str)
    assert default_prompt.role == Role().default

def test_default_prompt_length():
    default_prompt = DefaultPrompt(topic='test topic')
    assert len(default_prompt.main_text) < MAX_TOKENS

def test_default_prompt_contains_main_text_components():
    default_prompt = DefaultPrompt(topic='test topic')
    default_text = default_prompt.default()
    assert default_prompt.main_text is not None
    assert isinstance(default_prompt.main_text, str)
    assert len(default_prompt.main_text) > 0
    assert default_prompt.output_goal in default_text
    assert default_prompt.additional_reqs in default_text
    assert default_prompt.format_instructions in default_text


def test_default_prompt_contains_voiceover_prompt():
    """Test that the voiceover prompt is included in the main text."""
    default_prompt = DefaultPrompt(topic='test topic')
    default_text = default_prompt.default()
    
    # Check that voiceover prompt is included
    assert default_prompt.voiceover_prompt in default_text, "Voiceover prompt should be included in main text"
    
    # Check that voiceover prompt contains expected content
    voiceover_text = default_prompt.voiceover_prompt
    assert "voiceover script" in voiceover_text.lower(), "Voiceover prompt should mention voiceover script"
    assert "professional/aspiring software engineers" in voiceover_text, "Voiceover prompt should target developers"
    assert "2-3 minutes max" in voiceover_text, "Voiceover prompt should specify duration"
    assert "use cases and tips/tricks" in voiceover_text, "Voiceover prompt should mention use cases"
    assert "conversational, engaging language" in voiceover_text, "Voiceover prompt should specify language style"
    assert "test_topic" in voiceover_text, "Voiceover prompt should include the topic name"


def test_voiceover_prompt_formatting():
    """Test that the voiceover prompt includes proper formatting instructions."""
    default_prompt = DefaultPrompt(topic='bash')
    voiceover_text = default_prompt.voiceover_prompt
    
    # Check for proper formatting instructions
    assert "```yaml" in voiceover_text, "Voiceover prompt should include YAML formatting"
    assert "```voiceover" in voiceover_text, "Voiceover prompt should include voiceover formatting"
    assert "[cheatsheet content]" in voiceover_text, "Voiceover prompt should show cheatsheet placeholder"
    assert "[voiceover script content]" in voiceover_text, "Voiceover prompt should show voiceover placeholder"


def test_voiceover_prompt_topic_specific():
    """Test that the voiceover prompt is topic-specific."""
    bash_prompt = DefaultPrompt(topic='bash')
    python_prompt = DefaultPrompt(topic='python')
    
    # Check that each prompt includes its specific topic
    assert "bash" in bash_prompt.voiceover_prompt, "Bash prompt should include 'bash' topic"
    assert "python" in python_prompt.voiceover_prompt, "Python prompt should include 'python' topic"
    
    # Check that the prompts are different (topic-specific)
    assert bash_prompt.voiceover_prompt != python_prompt.voiceover_prompt, "Prompts should be topic-specific"


@pytest.mark.api_test
@pytest.mark.skip
def test_api_connection_returns_text():
    """Should not be 401"""
    # TODO other test cases: prompt should never exceed limit, should catch before api call is ever sent. (num chars?)
    # assert all prompt class values are populated before being used in an API call

    # assert APi key exists
    key = os.getenv("ANTHROPIC_API_KEY") is not None

    client = anthropic.Anthropic()

    # create message
    message = client.messages.create(
        model="claude-opus-4-20250514",
        max_tokens=20,
        temperature=1,
        system="Only respond with a single letter",
        messages=[  # TODO make abstract
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Tell me a joke"
                    }
                ]
            }
        ]
    )
    response = message.content
    assert response is not None
    assert isinstance(response, list)  # expect [TextBlock(citations=None, text='...', type='text')]

    # load env api key
    # check still valid and http request (curl) does not fail

