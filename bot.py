# bot.py
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from puzzle_generator import WordSearch
import config

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# Example words to include in the puzzle
DEFAULT_WORDS = ['PYTHON', 'TELEGRAM', 'BOT', 'WORD', 'SEARCH', 'PUZZLE', 'CODE']

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome to the Wordseek Telegram Bot!\n"
        "Use /puzzle to get a new word search puzzle.\n"
        "You can also add your own words separated by commas:\n"
        "/puzzle python,bot,code"
    )

async def puzzle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    words = DEFAULT_WORDS
    if context.args:
        # parse user words, split by commas, strip spaces and uppercase
        user_input = ' '.join(context.args)
        words = [w.strip().upper() for w in user_input.split(',') if w.strip()]
        if not words:
            words = DEFAULT_WORDS

    # Limit words to max 10 to avoid overly big puzzle
    words = words[:10]

    ws = WordSearch(size=15, words=words)
    grid, placed_words = ws.generate()

    puzzle_text = ws.grid_to_str()
    word_list_text = ', '.join(placed_words)

    message = f"🧩 Word Search Puzzle:\n\n{puzzle_text}\n\nWords:\n{word_list_text}"
    await update.message.reply_text(message)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Commands:\n"
        "/start - Welcome message\n"
        "/puzzle - Generate a puzzle\n"
        "/puzzle word1,word2,... - Generate puzzle with your own words\n"
        "/help - Show this help message"
    )

def main():
    application = ApplicationBuilder().token(config.BOT_TOKEN).build()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('puzzle', puzzle))
    application.add_handler(CommandHandler('help', help_command))

    logger.info("Starting bot...")
    application.run_polling()

if __name__ == '__main__':
    main()

