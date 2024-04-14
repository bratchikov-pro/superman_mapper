from sre_constants import CATEGORY
from turtle import distance
from unicodedata import category
from telegram.ext import MessageHandler, filters, Application, ConversationHandler, CommandHandler
from telegram import Update
from dal.open_maps_broker.open_maps_broker import OpenMapsBroker
from dal.entities import Location
from dal.telegram_bot.menu import DISTANCE, LOCATION, cancel, location, start

# Токен вашего бота
TOKEN = "6718494729:AAHjrjU0YZau3RI0HaWNgwqWN8jHlkA9Iww"


async def location_handler(update, context) -> None:
    message = None

    if update.edited_message:
        message = update.edited_message
    else:
        message = update.message

    print((message.location.latitude, message.location.longitude))
    loc = Location(latitude=message.location.latitude, longitude=message.location.longitude, search_distance=500)
    broker = OpenMapsBroker()

    nodes = broker.get_nodes_by_amenity(amenity="cafe", user_location=loc)
    print(nodes)

    await context.bot.send_location(chat_id=message.chat_id, latitude=44.605329, longitude=40.105376)



def main() -> None:
    application = Application.builder().token(TOKEN).build()
    application.add_handler(MessageHandler(filters.LOCATION, location_handler))

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            LOCATION: [MessageHandler(filters.LOCATION, location)],
            DISTANCE: [MessageHandler(filters.Regex("^(Boy|Girl|Other)$"), distance)],
            CATEGORY: [MessageHandler(filters.PHOTO, category)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    application.add_handler(conv_handler)

    application.run_polling()


if __name__ == '__main__':
    main()
