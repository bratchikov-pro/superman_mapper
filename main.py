from telegram.ext import MessageHandler, filters, Application
from telegram import Update
from dal.open_maps_broker.open_maps_broker import OpenMapsBroker
from dal.entities import Location

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

    application.run_polling()


if __name__ == '__main__':
    main()
