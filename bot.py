import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Token depuis les variables d'environnement (plus sécurisé)
TOKEN = os.environ.get("BOT_TOKEN", "8045140139:AAGrhy5PhTGByTUEKd7-nSj4QDjCz46JSUg")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_text(
        f"🔞 Bienvenue {user.first_name} sur AI MAGIC PHOTO EDITOR !\n\n"
        "Envoie une photo, je la transforme en version nue.\n\n"
        "/premium - Illimité (Wave 5000 FCFA)\n/help - Aide"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📘 Envoie une photo, je la transforme !\n"
        "Pour des transformations illimitées, tape /premium"
    )

async def premium(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🏆 **PREMIUM - 5000 FCFA/mois** 🏆\n\n"
        "📲 **Paiement Wave :**\n"
        "1️⃣ Envoie **5000 FCFA** au : **0141418815**\n"
        "2️⃣ Prends la capture d'écran\n"
        "3️⃣ Envoie-la ici\n\n"
        "⏱ Activation sous 5 minutes !"
    )

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = await update.message.reply_text("⏳ Transformation en cours...")
    # Ici on ajoutera l'API plus tard
    await msg.edit_text("✅ Bientôt disponible ! Mode démo")

def main():
    print("🤖 Bot démarré sur Render...")
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("premium", premium))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    print("✅ Bot prêt !")
    app.run_polling()

if __name__ == "__main__":
    main()