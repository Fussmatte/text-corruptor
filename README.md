# text-corruptor
Puts text through a translator several times 'til it's just bad

## what you need
- Python 3 or greater
- the `googletrans` thing that you gotta install with pip

## how to use this thing
so just like run it in terminal, and it'll prompt you for your text.
- `/h` - Display the help page
- `/q` or `/e` - Exit the program
- `/c` - Recorrupt the last corruption
- `/r` - Retry for a new corruption of the last input
- `/l=xx` - Set interface language to xx (see below)
- `/e=xx` - Set corruption output language to xx (see below)

## available languages for the interface (`/l=`)
- `en` - English
- `eo` - Esperanto

See [here](https://github.com/ssut/py-googletrans/blob/master/googletrans/constants.py) for a list of languages to be used with `/e=`.