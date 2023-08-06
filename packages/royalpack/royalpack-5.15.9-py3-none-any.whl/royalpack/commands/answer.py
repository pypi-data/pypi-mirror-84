from typing import *
import royalnet
import royalnet.commands as rc
import random
import datetime


class AnswerCommand(rc.Command):
    name: str = "answer"

    description: str = "Fai una domanda al bot, che possa essere risposta con un sì o un no: lui ti risponderà!"

    syntax: str = ""

    _answers = [
        # Cerchiamo di tenere bilanciate le tre colonne, o almeno le prime due.
        # Se avete un'idea ma metterebbe troppe opzioni in un'unica categoria, mettetela sotto commento.

        # risposte "sì": 15
        "🔵 Sì.",
        "🔵 Decisamente sì!",
        "🔵 Uhm, secondo me sì.",
        "🔵 Sì! Sì! SÌ!",
        "🔵 Yup.",
        "🔵 Direi proprio di sì.",
        "🔵 Assolutamente sì.",
        "🔵 Ma certo!",
        "🔵 Esatto!",
        "🔵 Senz'altro!",
        "🔵 Ovviamente.",
        "🔵 Questa domanda ha risposta affermativa.",
        "🔵 Hell yeah.",
        "🔵 [url=https://www.youtube.com/watch?v=sq_Fm7qfRQk]YES! YES! YES![/url]",
        "🔵 yusssssss",

        # risposte "no": 15
        "❌ No.",
        "❌ Decisamente no!",
        "❌ Uhm, secondo me sì.",
        "❌ No, no, e ancora NO!",
        "❌ Nope.",
        "❌ Direi proprio di no.",
        "❌ Assolutamente no.",
        "❌ Certo che no!",
        "❌ Neanche per idea!",
        "❌ Neanche per sogno!",
        "❌ Niente affatto!",
        "❌ Questa domanda ha risposta negativa.",
        "❌ Hell no.",
        "❌ [url=https://www.youtube.com/watch?v=fKEZFRcuEqw]NO! NO! NO![/url]",
        "❌ lolno",

        # risposte "boh": 15
        "❔ Boh.",
        "❔ E io che ne so?!",
        "❔ Non so proprio rispondere.",
        "❔ Non lo so...",
        "❔ Mi avvalgo della facoltà di non rispondere.",
        "❔ Non parlerò senza il mio avvocato!",
        "❔ Dunno.",
        "❔ Perché lo chiedi a me?",
        "❔ Ah, non lo so io!",
        "❔ ¯\\_(ツ)_/¯",
        "❔ No idea.",
        "❔ Dunno.",
        "❔ Boooooh!",
        "❔ Non ne ho la più pallida idea.",
        "❔ No comment.",
        "❔ maibi",
    ]

    async def run(self, args: rc.CommandArgs, data: rc.CommandData) -> None:
        h = hash(datetime.datetime.now())

        r = random.Random(x=h)

        message = r.sample(self._answers, 1)[0]
        await data.reply(message)
