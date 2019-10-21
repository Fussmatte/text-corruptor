from googletrans import Translator # Make sure you pip install googletrans
import googletrans, random
translator = Translator() # Making a new translator instance

def corrupt(text,langnum,endlang): # This function will corrupt any text fed into it
    # text = string var, the text to be corrupted
    # langnum = the amount of languages to put it through, randomly chosen
    # endlang = code for the final language to translate to ("en" for English)
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
        lasttext = translator.translate(lasttext, dest=lang).text #the actual translate command
        lastlang = lang # so that the next cycle knows what language to translate from
        
    return lasttext # here's your final corrupted text!

oldcorruption = "" # failsafe in case someone tries to call 'cycle' at the beginning of runtime

while True:
    # prompts for text, which goes into tobetranslated
    tobetranslated = input("Corrupt ('exit' to exit or 'cycle' to repeat)>> ")

    if tobetranslated == "exit":
        break
    elif tobetranslated == "cycle":
        tobetranslated = oldcorruption # will corrupt the old corruption

    # this command will do the honours, and store it into oldcorruption
    # for future use by the cycle command
    oldcorruption = corrupt(tobetranslated,9,"en")
    print("\n" + oldcorruption) #prints the corruption