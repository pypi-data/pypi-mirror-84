from typing import *
import re
import datetime
import telegram
import aiohttp
import royalnet.commands as rc
import royalnet.utils as ru
import royalnet.backpack.tables as rbt
import royalnet.serf.telegram as rst

from ..tables import *


async def to_imgur(imgur_api_key, photosizes: List[telegram.PhotoSize], caption="") -> str:
    # Select the largest photo
    largest_photo = sorted(photosizes, key=lambda p: p.width * p.height)[-1]
    # Get the photo url
    photo_file: telegram.File = await ru.asyncify(largest_photo.get_file)
    # Forward the url to imgur, as an upload
    async with aiohttp.request("post", "https://api.imgur.com/3/upload", data={
        "image": photo_file.file_path,
        "type": "URL",
        "title": "Diario image",
        "description": caption
    }, headers={
        "Authorization": f"Client-ID {imgur_api_key}"
    }) as request:
        response = await request.json()
        if not response["success"]:
            raise rc.CommandError(f"Imgur returned an error in the image upload: {response}")
        return response["data"]["link"]


class DiarioCommand(rc.Command):
    name: str = "diario"

    description: str = "Aggiungi una citazione al Diario."

    syntax = "[!] \"{testo}\" --[autore], [contesto]"

    async def run(self, args: rc.CommandArgs, data: rc.CommandData) -> None:
        async with data.session_acm() as session:
            if isinstance(self.serf, rst.TelegramSerf):
                message: telegram.Message = data.message
                reply: telegram.Message = message.reply_to_message
                creator = await data.find_author(session=session, required=True)
                # noinspection PyUnusedLocal
                quoted: Optional[str]
                # noinspection PyUnusedLocal
                text: Optional[str]
                # noinspection PyUnusedLocal
                context: Optional[str]
                # noinspection PyUnusedLocal
                timestamp: datetime.datetime
                # noinspection PyUnusedLocal
                media_url: Optional[str]
                # noinspection PyUnusedLocal
                spoiler: bool
                if creator is None:
                    await data.reply("⚠️ Devi essere registrato a Royalnet per usare questo comando!")
                    return
                if reply is not None:
                    # Get the message text
                    text = reply.text
                    # Check if there's an image associated with the reply
                    photosizes: Optional[List[telegram.PhotoSize]] = reply.photo
                    if photosizes:
                        # Text is a caption
                        text = reply.caption
                        media_url = await to_imgur(self.config["Imgur"]["token"],
                                                   photosizes, text if text is not None else "")
                    else:
                        media_url = None
                    # Ensure there is a text or an image
                    if not (text or media_url):
                        raise rc.InvalidInputError("Il messaggio a cui hai risposto non contiene testo o immagini.")
                    # Find the Royalnet account associated with the sender
                    quoted_tg = await ru.asyncify(session.query(self.alchemy.get(rbt.Telegram))
                                                  .filter_by(tg_id=reply.from_user.id)
                                                  .one_or_none)
                    quoted_account = quoted_tg.user if quoted_tg is not None else None
                    # Find the quoted name to assign
                    quoted_user: telegram.User = reply.from_user
                    quoted = quoted_user.full_name
                    # Get the timestamp
                    timestamp = reply.date
                    # Set the other properties
                    spoiler = False
                    context = None
                else:
                    # Get the current timestamp
                    timestamp = datetime.datetime.now()
                    # Get the message text
                    raw_text = " ".join(args)
                    # Check if there's an image associated with the reply
                    photosizes: Optional[List[telegram.PhotoSize]] = message.photo
                    if photosizes:
                        media_url = await to_imgur(self.config["Imgur"]["token"],
                                                   photosizes, raw_text if raw_text is not None else "")
                    else:
                        media_url = None
                    # Parse the text, if it exists
                    if raw_text:
                        # Pass the sentence through the diario regex
                        match = re.match(
                            r'(!)? *["«‘“‛‟❛❝〝＂`]([^"]+)["»’”❜❞〞＂`] *(?:(?:-{1,2}|—) *([^,]+))?(?:, *([^ ].*))?',
                            raw_text)
                        # Find the corresponding matches
                        if match is not None:
                            spoiler = bool(match.group(1))
                            text = match.group(2)
                            quoted = match.group(3)
                            context = match.group(4)
                        # Otherwise, consider everything part of the text
                        else:
                            spoiler = False
                            text = raw_text
                            quoted = None
                            context = None
                        # Ensure there's a quoted
                        if not quoted:
                            quoted = None
                        if not context:
                            context = None
                        # Find if there's a Royalnet account associated with the quoted name
                        if quoted is not None:
                            quoted_alias = await ru.asyncify(
                                session.query(self.alchemy.get(rbt.Alias))
                                       .filter_by(alias=quoted.lower()).one_or_none
                            )
                        else:
                            quoted_alias = None
                        quoted_account = quoted_alias.user if quoted_alias is not None else None
                    else:
                        text = None
                        quoted = None
                        quoted_account = None
                        spoiler = False
                        context = None
                    # Ensure there is a text or an image
                    if not (text or media_url):
                        raise rc.InvalidInputError("Manca il testo o l'immagine da inserire nel diario.")
                # Create the diario quote
                diario = self.alchemy.get(Diario)(creator=creator,
                                                  quoted_account=quoted_account,
                                                  quoted=quoted,
                                                  text=text,
                                                  context=context,
                                                  timestamp=timestamp,
                                                  media_url=media_url,
                                                  spoiler=spoiler)
                session.add(diario)
                await ru.asyncify(session.commit)
                await data.reply(f"✅ {str(diario)}")
            else:
                # Find the creator of the quotes
                creator = await data.find_author(session=session, required=True)
                # Recreate the full sentence
                raw_text = " ".join(args)
                # Pass the sentence through the diario regex
                match = re.match(r'(!)? *["«‘“‛‟❛❝〝＂`]([^"]+)["»’”❜❞〞＂`] *(?:(?:-{1,2}|—) *([^,]+))?(?:, *([^ ].*))?',
                                 raw_text)
                # Find the corresponding matches
                if match is not None:
                    spoiler = bool(match.group(1))
                    text = match.group(2)
                    quoted = match.group(3)
                    context = match.group(4)
                # Otherwise, consider everything part of the text
                else:
                    spoiler = False
                    text = raw_text
                    quoted = None
                    context = None
                timestamp = datetime.datetime.now()
                # Ensure there is some text
                if not text:
                    raise rc.InvalidInputError("Manca il testo o l'immagine da inserire nel diario.")
                # Or a quoted
                if not quoted:
                    quoted = None
                if not context:
                    context = None
                # Find if there's a Royalnet account associated with the quoted name
                if quoted is not None:
                    quoted_account = await rbt.User.find(self.alchemy, session, quoted)
                else:
                    quoted_account = None
                if quoted_account is None:
                    raise rc.UserError("Il nome dell'autore è ambiguo, quindi la riga non è stata aggiunta.\n"
                                       "Per piacere, ripeti il comando con un nome più specifico!")
                # Create the diario quote
                DiarioT = self.alchemy.get(Diario)
                diario = DiarioT(creator=creator,
                                 quoted_account=quoted_account,
                                 quoted=quoted,
                                 text=text,
                                 context=context,
                                 timestamp=timestamp,
                                 media_url=None,
                                 spoiler=spoiler)
                session.add(diario)
                await ru.asyncify(session.commit)
                await data.reply(f"✅ {str(diario)}")
