from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import logging
import openai
import os

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Set your OpenAI API Key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Owner Info
OWNER_NAME = "K Sai Rao"
OWNER_USERNAME = "@X_sai_X"

# Define /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_text = (
        "👋 Welcome to the *Smart Career Assistant Bot*!\n\n"
        "📌 I can help you with:\n"
        "- Career guidance\n"
        "- Resume suggestions\n"
        "- Skill/course recommendations\n\n"
        "Type /career to get started!"
    )
    await update.message.reply_markdown(welcome_text)

# Define /owner
async def owner(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"👤 Owner: {OWNER_NAME} ({OWNER_USERNAME})")

# Define /career
async def career(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [['Engineering', 'Medical'], ['Design', 'Business'], ['Government Exams']]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text("What field are you interested in?", reply_markup=reply_markup)

# Handle text replies from keyboard
async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    interest = update.message.text
    suggestions = {
        "Engineering": ["AI Engineer", "Software Developer", "Data Scientist"],
        "Medical": ["MBBS", "Pharmacy", "Nursing"],
        "Design": ["UX Designer", "Graphic Designer", "Animator"],
        "Business": ["Marketing", "Finance Analyst", "Entrepreneur"],
        "Government Exams": ["UPSC", "SSC CGL", "Railway JE"]
    }

    if interest in suggestions:
        courses = "\n".join([f"- {career}" for career in suggestions[interest]])
        await update.message.reply_text(f"🌟 Based on your interest in *{interest}*, here are some career options:\n\n{courses}", parse_mode='Markdown')
    else:
        await update.message.reply_text("Please choose an option from the keyboard using /career.")

# Define /resume (simple AI-based resume tips)
async def resume(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📄 Please upload your resume as a text message or paste it directly.")

async def resume_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    prompt = f"Give 3 improvements or suggestions to improve this resume:\n{text}"

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        tips = response['choices'][0]['message']['content']
        await update.message.reply_text(f"🧠 Resume Tips:\n{tips}")
    except Exception as e:
        await update.message.reply_text("❌ Error generating suggestions. Please try again later.")
        print(e)

# Initialize App
app = ApplicationBuilder().token(os.getenv("BOT_TOKEN")).build()

# Register handlers
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("owner", owner))
app.add_handler(CommandHandler("career", career))
app.add_handler(CommandHandler("resume", resume))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, resume_text))

# Run the bot
app.run_polling()
