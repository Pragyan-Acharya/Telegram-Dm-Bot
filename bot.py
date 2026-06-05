import os
import asyncio
import nest_asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from telegram.error import TelegramError
from dotenv import load_dotenv

# Apply nest_asyncio to handle nested event loops
nest_asyncio.apply()

# Load environment variables from credentials.env file
load_dotenv(dotenv_path="credentials.env")

# Retrieve and validate environment variables
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_CHAT_ID = os.getenv("ADMIN_CHAT_ID")

# Validate BOT_TOKEN
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN is not set in credentials.env. Please provide a valid token.")
if not ADMIN_CHAT_ID:
    print("Warning: ADMIN_CHAT_ID is not set in credentials.env. Admin features may not work.")

# Error handler
async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle errors and notify the user."""
    try:
        raise context.error
    except TelegramError as e:
        error_message = f"An error occurred: {str(e)}"
        print(error_message)
        if update and update.message:
            await update.message.reply_text("Sorry, something went wrong. Please try again later.")
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        if update and update.message:
            await update.message.reply_text("Sorry, an unexpected error occurred.")

# Handler for the /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.message.from_user
    user_id = user.id
    first_name = user.first_name
    # Welcome message with clickable user mention
    welcome_message = (
        f"𝗛𝗲𝘆 𝘁𝗵𝗲𝗿𝗲 <a href=\"tg://user?id={user_id}\">{first_name}</a>, "
        "𝘁𝗵𝗶𝘀 𝗶𝘀 𝗨𝗹𝘁𝗿𝗼𝗶𝗱 𝗔𝘀𝘀𝗶𝘀𝘁𝗮𝗻𝘁 𝗼𝗳 𝗛𝗲𝗶𝘀𝗲𝗻𝗯𝗲𝗿𝗴 (@Heisenberg_Encrypted)\n"
        "𝗬𝗼𝘂 𝗰𝗮𝗻 𝗰𝗼𝗻𝘁𝗮𝗰𝘁 𝗺𝘆 𝗺𝗮𝘀𝘁𝗲𝗿 𝘂𝘀𝗶𝗻𝗴 𝘁𝗵𝗶𝘀 𝗯𝗼𝘁!!\n\n"
        "𝗦𝗲𝗻𝗱 𝘆𝗼𝘂𝗿 𝗠𝗲𝘀𝘀𝗮𝗴𝗲. 𝗜 𝘄𝗶𝗹𝗹 𝗗𝗲𝗹𝗶𝘃𝗲𝗿 𝗶𝘁 𝗧𝗼 𝗠𝗮𝘀𝘁𝗲𝗿."
    )
    await update.message.reply_text(welcome_message, parse_mode="HTML")

# Handler for all message types (text, photo, video, sticker, document, etc.)
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.message.from_user
    chat_id = update.message.chat_id
    message = update.message

    if not ADMIN_CHAT_ID:
        await update.message.reply_text("Error: Admin not configured. Please try again later.")
        return

    try:
        # Prepare user info for forwarding
        user_info = f"Message from {user.first_name} (ID: {chat_id}):\n"

        # Handle different message types
        if message.text:
            await context.bot.send_message(
                chat_id=int(ADMIN_CHAT_ID),
                text=f"{user_info}{message.text}"
            )
        elif message.photo:
            # Send the highest resolution photo with caption
            await context.bot.send_photo(
                chat_id=int(ADMIN_CHAT_ID),
                photo=message.photo[-1].file_id,
                caption=user_info + (message.caption or "Photo")
            )
        elif message.video:
            await context.bot.send_video(
                chat_id=int(ADMIN_CHAT_ID),
                video=message.video.file_id,
                caption=user_info + (message.caption or "Video")
            )
        elif message.sticker:
            # Send sticker + sender name
            await context.bot.send_sticker(
                chat_id=int(ADMIN_CHAT_ID),
                sticker=message.sticker.file_id
            )
            await context.bot.send_message(
                chat_id=int(ADMIN_CHAT_ID),
                text=f"Sticker from {user.first_name}"
            )
        elif message.document:
            await context.bot.send_document(
                chat_id=int(ADMIN_CHAT_ID),
                document=message.document.file_id,
                caption=user_info + (message.caption or message.document.file_name or "Document")
            )
        elif message.audio:
            await context.bot.send_audio(
                chat_id=int(ADMIN_CHAT_ID),
                audio=message.audio.file_id,
                caption=user_info + (message.caption or "Audio")
            )
        elif message.voice:
            await context.bot.send_voice(
                chat_id=int(ADMIN_CHAT_ID),
                voice=message.voice.file_id,
                caption=user_info + "Voice message"
            )
        else:
            await context.bot.send_message(
                chat_id=int(ADMIN_CHAT_ID),
                text=user_info + "Unsupported message type"
            )

        # Log the message for debugging
        print(f"User {user.first_name} (ID: {chat_id}) sent: {message}")
    except Exception as e:
        await update.message.reply_text(f"Error forwarding message: {str(e)}")
        print(f"Error forwarding message from {user.first_name} (ID: {chat_id}): {str(e)}")

# Handler for admin to reply with text
async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Ensure only the admin can use this command
    if str(update.message.chat_id) != ADMIN_CHAT_ID:
        await update.message.reply_text("This command is only for the master!")
        return
    
    args = context.args
    if len(args) < 2:
        await update.message.reply_text("Usage: /reply <chat_id> <message>")
        return
    
    try:
        chat_id = int(args[0])
        message = " ".join(args[1:])
        await context.bot.send_message(chat_id=chat_id, text=message)
        await update.message.reply_text(f"Message sent to user {chat_id}!")
    except Exception as e:
        await update.message.reply_text(f"Error sending message: {str(e)}")

# Handler for admin to send files
async def sendfile(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Ensure only the admin can use this command
    if str(update.message.chat_id) != ADMIN_CHAT_ID:
        await update.message.reply_text("This command is only for the master!")
        return

    if not context.args:
        await update.message.reply_text("Usage: /sendfile <chat_id> (then reply with a file)")
        return

    try:
        chat_id = int(context.args[0])
        if not update.message.reply_to_message:
            await update.message.reply_text("Please reply to a message containing a file (photo, video, sticker, document, etc.)")
            return

        reply_msg = update.message.reply_to_message
        # Handle different file types
        if reply_msg.photo:
            await context.bot.send_photo(
                chat_id=chat_id,
                photo=reply_msg.photo[-1].file_id,
                caption=reply_msg.caption or "Photo"
            )
        elif reply_msg.video:
            await context.bot.send_video(
                chat_id=chat_id,
                video=reply_msg.video.file_id,
                caption=reply_msg.caption or "Video"
            )
        elif reply_msg.sticker:
            await context.bot.send_sticker(
                chat_id=chat_id,
                sticker=reply_msg.sticker.file_id
            )
        elif reply_msg.document:
            await context.bot.send_document(
                chat_id=chat_id,
                document=reply_msg.document.file_id,
                caption=reply_msg.caption or reply_msg.document.file_name or "Document"
            )
        elif reply_msg.audio:
            await context.bot.send_audio(
                chat_id=chat_id,
                audio=reply_msg.audio.file_id,
                caption=reply_msg.caption or "Audio"
            )
        elif reply_msg.voice:
            await context.bot.send_voice(
                chat_id=chat_id,
                voice=reply_msg.voice.file_id,
                caption="Voice message"
            )
        else:
            await update.message.reply_text("Unsupported file type. Please reply to a photo, video, sticker, document, or audio.")
            return

        await update.message.reply_text(f"File sent to user {chat_id}!")
    except Exception as e:
        await update.message.reply_text(f"Error sending file: {str(e)}")

# Main function to set up and run the bot
async def main() -> None:
    # Initialize the bot with the token
    try:
        app = Application.builder().token(BOT_TOKEN).build()
    except Exception as e:
        print(f"Failed to initialize bot: {str(e)}")
        raise

    # Add handlers for commands, messages, and errors
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("reply", reply))
    app.add_handler(CommandHandler("sendfile", sendfile))
    app.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND, handle_message))
    app.add_error_handler(error_handler)

    # Start the bot in polling mode
    print("Bot started successfully!")
    try:
        await app.initialize()
        await app.start()
        await app.updater.start_polling()
        # Keep the bot running until stopped
        await asyncio.Event().wait()
    except Exception as e:
        print(f"Error running bot: {str(e)}")
        raise
    finally:
        # Ensure proper shutdown
        try:
            await app.updater.stop()
            await app.stop()
            await app.shutdown()
        except Exception as e:
            print(f"Error during shutdown: {str(e)}")

if __name__ == "__main__":
    # Run the bot in the current event loop
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        if not loop.is_closed():
            loop.close()