
1. Prompt
    - topic renders correctly
2. Environment setup
3. API call
    - contains prompt with right elements
4. Files:
    - save reponse locally
    - commit file and upload to repo


## Happy path:

1. ### Default Prompt with 'bash' topic
- set up environment
- make a default prompt instance
- call API with it
- expect a reponse back
- that saves the file correctly with the right topic name and path

2. #### Start states

*Default Prompt*
- starts with all the correct params, with nothing missing
- update role - has that changed
- topic with spaces (test topic) -> 'test_topic' or raises value error (decide on one design)
- instantiates with a set topic correctly (test_prompt = DefaultPrompt('topic'), assert test_prompt.topic = 'topic')
- if one key in the file is missing, it doesn't fail (or does? Do I want prompts to fail if there is no prompt file? NO. Design with this in mind. WHat will this entail?)
- does it match to a topic file correctly??
- does it start with the default role object?
- does the main text call the defalt method it has built in, which should contain main text, format instructions, additional reqs and output goal?
- default instance main text is of type string, and doesn't exceed the max tokens length


*Save response to file*
- no file -> fail
- yaml file syntax via re -> saves correctly
- multiple yaml files in single response just take the first?
- what if yaml is not in correct format?
- DESIGN: should the key of each be checked first?

- grab topic, make file of same name, ensure that file exists
- check the content of that file is actually the same as what was returned in the original response
- if fail, try writing file again?
- if file name already exists, runtime error - should be categorised by timestamp id
- in correct folder
- DESIGN: check what keys are already there? Yaml files are actually useful here. THen I just need yaml to markdown