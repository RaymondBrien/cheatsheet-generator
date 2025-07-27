import os
import pytest
import anthropic

from prompt_templates.main_prompt import Prompt
from API_CONFIG import MAX_TOKENS


def test_prompt_values():
    prompt = Prompt()
    default_text = prompt.default()
    assert isinstance(default_text, str)
    assert len(default_text) < MAX_TOKENS
    ...

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

