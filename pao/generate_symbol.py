import ollama
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument('--char', type=str, help='For example, --char=A')
parser.add_argument('--exclude', type=str, default='',
    help='For example, when --char=H, --exclude=hero,halfling excludes hero and halfling')
parser.add_argument('--describe', type=bool, default=False)
args = parser.parse_args()

prompt = (
    'You are to assign a well-known and impressive type of imagined'
    f' character in literatures started by "{args.char}". For example,'
    ' elf for "E", wizard for "W". Only return the result.'
)

if args.exclude:
    prompt += f' You shall exclude {", ".join(args.exclude.split(","))}.'

if args.describe:
    prompt += (
        ' Then show an example of the type of character, and introduce'
        ' where this characeter comes from.'
    )
result = ollama.generate('llama3', prompt)
print(result['response'])

