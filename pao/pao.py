import re
import ollama
from typing import Union


class LanguageModel:
    """A unified API for large language models employed for PAO."""

    def __init__(self, model_name: str):
        self.model_name = model_name
    
    def __call__(self, prompt: str) -> str:
        try:
            raw_result = ollama.generate(self.model_name, prompt)
            result = raw_result['response']
            return result
        except ollama.ResponseError as e:
            if e.status_code == 404:
                print(f'The pretrained language model "{self.model_name}" is '
                      'absent locally. Pulling from remote......')
                ollama.pull(self.model_name)
            else:
                raise e

class PAO:

    MAX_NUM_TRIALS = 3
    _language_model = LanguageModel('llama3')  # default language model.

    def __init__(self, person: str, action: str, object: str,
                 text: str = None):
        self.person = person
        self.action = action
        self.object = object

        self.text = self._generate_text()
    
    @classmethod
    def set_language_model(cls, model: Union[LanguageModel, str]):
        """Reset the language model which is universal to the class."""
        if isinstance(model, LanguageModel):
            cls._language_model = model
        elif isinstance(model, str):
            cls._language_model = LanguageModel(model)
        else:
            raise ValueError()

    def _generate_text(self):
        prompt = (
            'Now the task is generating a sentence based on a person, '
            'an action, and an object. '

            f'The person is {self.person}, the action is {self.action}, '
            f'and the object is {self.object}. '

            'The sentence is strange, graphic, impressive, but not long. '
            'You shall use plain English in the sentence. '

            'Only one person appears in the sentence. '
            'The action is dramatic. '
            'The object looks impressive. '

            'Only return the sentence, wrapped in a bracket, like [sentence].'
        )
        for _ in range(PAO.MAX_NUM_TRIALS):
            raw_result = self._language_model(prompt)
            # Parse the result wrapped in the bracket.
            parts = re.findall('\[(.*?)\]', raw_result)
            if len(parts) == 1:
                return parts[0]
            else:
                print('ERROR: The result obtained from language model is:\n\n'
                      + raw_result)
        raise ValueError(
            f'Generation fails after {self.MAX_NUM_TRIALS} trials.')


x1 = PAO('Harry Potter', 'giving lecture', 'football')
x1.text
x2 = PAO('Superman', 'eating', 'computer')
x2.text

# Translate the following English text into Chinese. The translation shall be accurate and plain. The English text is: "With wand flashing and eyes ablaze, Harry Potter delivers a lecture on the art of Quidditch to a packed stadium, where a gleaming football floats in mid-air, awaiting its fate." So, the translation is:
