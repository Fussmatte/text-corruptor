# -*- coding: iso-8859-15 -*-

# Text Corruptor
# v0.3.0

# Copyright 2019-2020 Fußmatte

# Permission is hereby granted, free of charge, to any person obtaining a copy of this software
# and associated documentation files (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge, publish, distribute,
# sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all copies or
# substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT
# NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NON-
# INFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES
# OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR
# IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

# -------------------------------------------------------------------------------------------------

from googletrans import Translator # Make sure you pip install googletrans and babel
from configparser import ConfigParser
import googletrans, random, os.path, gettext, babel
from glob import glob
from os import path, listdir

config = ConfigParser()
progver = "v1.0.1"

def _(message): return message

if not path.exists("config.ini"):
    uilang = "en"
    config.read('config.ini')
    config.add_section('main')
    config.set('main', 'lang', uilang)
    config.set('main', 'outputlang', outputlang)
    
    with open('config.ini', 'w') as f:
        config.write(f)
else:
    config.read('config.ini')
    uilang = config.get('main', 'lang')
    outputlang = config.get('main', 'outputlang')

def available_langs():
    return os.listdir("locale")

langs = available_langs()

def set_uilang(lang):
    global _
    locale = babel.Locale.parse(lang)
    if lang == "en":
        _ = lambda s: s
    else:
        if lang in langs:
            del _
            uilangset = gettext.translation('tc', 'locale/', [lang])
            uilangset.install()
        else:
            lang="en"
            _ = lambda s: s
    config.read('config.ini')
    config.set('main', 'lang', lang)
    
    with open('config.ini', 'w') as f:
        config.write(f)
    return _("Set language to %s") % (locale.get_display_name())

set_uilang(uilang)

translator = Translator() # Making a new translator instance

nostring = _("ERROR: Please enter a string.")
dummymode = False

def corrupt(text,langnum,endlang): # This function will corrupt any text fed into it
    if text.isspace() or text == "":
        return nostring
    # text = string var, the text to be corrupted
    # langnum = the amount of languages to put it through, randomly chosen
    # endlang = code for the final language to translate to ("en" for English)
    # print("Corrupting...")
    alllangs = googletrans.LANGUAGES # loads a table of all language codes
    lastlang = endlang # lastlang = the previous language in each corruption cycle
    langsforthiscall = [] # a table that will contain all the languages to
                          # translate through
    for x in range(langnum - 1):
        addedlang = random.choice(list(alllangs)) #picks a random lang from alllangs
        langsforthiscall.append(addedlang) #adds the above to langsforthiscall

    langsforthiscall.append(endlang) # adds the end language to langsforthiscall
    lasttext = text # lasttext = the previous text in each corruption cycle

    for lang in langsforthiscall:
        if not dummymode:
            try:
                lasttext = translator.translate(lasttext, dest=lang).text #the actual translate command
                lastlang = lang # so that the next cycle knows what language to translate from
            except: # If an error occurs while trying to grab output, throw message
                print(_("FATAL: Server returned an error, try again later."))
                return 0
                break
    if dummymode:
        lasttext = _("<Dummy output>")
    return lasttext # here's your final corrupted text!

def launch_text():
    print(_("Text Corruptor") + " " + progver)
    print(_("Type /h and press ENTER for instructions."))

oldcorruption = "!NO_OLD_CORRUPTION" # failsafe in case someone tries to call 'cycle' at the beginning of runtime
oldtobetranslated = "!NO_OLD_TBT" # and same for 'redo'

launch_text()

while True:
    # prompts for text, which goes into tobetranslated
    tobetranslated = input(">> ")

    if tobetranslated == "!NO_OLD_CORRUPTION" or tobetranslated == "!NO_OLD_TBT":
        tobetranslated = ""
        print(_("Nice try!"))
        continue
    elif tobetranslated == "/q":
        break
    elif tobetranslated == "/h":
        spacing = "  "
        print(_("Type in what you want to be badly translated and press ENTER."))
        print(_("Commands:"))
        print(spacing+_("/c    - Re-corrupt the previous translation"))
        print(spacing+_("/r    - Try to corrupt the previous input differently"))
        print(spacing+_("/h    - Show this help screen"))
        print(spacing+_("/q    - Quit the program"))
        print(spacing+_("/l=xx - Sets interface language to xx, where xx is an ISO language code"))
        print(spacing+_("/e=xx - Sets corruption output language to xx"))
        continue
    elif tobetranslated == "/r":
        if oldtobetranslated != "!NO_OLD_TBT":
            tobetranslated = oldtobetranslated # will retry for a new corruption with old text
        else:
            oldtobetranslated = nostring
            print(nostring)
            continue
    elif tobetranslated == "/c":
        if oldcorruption != "!NO_OLD_CORRUPTION":
            tobetranslated = oldcorruption # will corrupt the old corruption
        else:
            oldcorruption = nostring
            print(nostring)
            continue
    elif tobetranslated == "/d":
        if not dummymode:
            print(_("Dummy mode active. Use command again to disable."))
            dummymode = True
        else:
            print(_("Dummy mode inactive."))
            dummymode = False
        continue
    elif tobetranslated.startswith('/l='):
        if uilang != tobetranslated.replace('/l=',''):
            uilang = tobetranslated.replace('/l=','')
            print(set_uilang(uilang))
            launch_text()
        else:
            locale = babel.Locale.parse(uilang)
            print(_("Language is already %s") % (locale.get_display_name()))
        continue
    elif tobetranslated.startswith('/e='):
        newoutputlang = tobetranslated.replace('/e=','')
        if outputlang != newoutputlang and newoutputlang in googletrans.LANGUAGES:
            outputlang = newoutputlang
            config.read('config.ini')
            config.set('main', 'outputlang', outputlang)
    
            with open('config.ini', 'w') as f:
                config.write(f)
        else:
            print(_("Language not found or is already set."))
        continue
    elif tobetranslated == "" or tobetranslated.isspace():
        print(nostring)
        continue

    oldtobetranslated = tobetranslated
    # this command will do the honours, and store it into oldcorruption
    # for future use by the cycle command
    oldcorruption = corrupt(tobetranslated,9,outputlang)
    if not oldcorruption==0:
        print("  -> " + oldcorruption) #prints the corruption