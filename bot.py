import os
import requests
import time
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Tokens
TELEGRAM_TOKEN = "8045140139:AAGrhy5PhTGByTUEKd7-nSj4QDjCz46JSUg"
REPLICATE_API_TOKEN = os.environ.get("REPLICATE_API_TOKEN")

# Modèle Replicate pour transformation
MODEL_VERSION = "stability-ai/stable-diffusion:db21e45d3f7023abc2a46ee38a23973f6dce16bb082a930b0c49861f96d1e5bf"

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
    # Message d'attente
    msg = await update.message.reply_text("⏳ Transformation en cours... (30-60 secondes)")
    
    try:
        # Télécharger la photo
        photo = await update.message.photo[-1].get_file()
        photo_url = photo.file_path
        
        # Appel à Replicate
        headers = {
            "Authorization": f"Token {REPLICATE_API_TOKEN}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "version": MODEL_VERSION,
            "input": {
                "prompt": "naked version of this person, realistic, high quality, detailed, photographic",
                "image": photo_url,
                "num_outputs": 1,
                "guidance_scale": 7.5,
                "num_inference_steps": 50
            }
        }
        
        # Démarrer la prédiction
        response = requests.post(
            "https://api.replicate.com/v1/predictions",
            headers=headers,
            json=payload
        )
        
        if response.status_code == 201:
            prediction = response.json()
            prediction_id = prediction["id"]
            
            # Attendre le résultat
            result_url = None
            attempts = 0
            max_attempts = 30
            
            while not result_url and attempts < max_attempts:
                status_response = requests.get(
                    f"https://api.replicate.com/v1/predictions/{prediction_id}",
                    headers=headers
                )
                status = status_response.json()
                
                if status["status"] == "succeeded":
                    result_url = status["output"][0]
                    break
                elif status["status"] == "failed":
                    await msg.edit_text("❌ Échec de la transformation. Réessaie.")
                    return
                
                attempts += 1
                time.sleep(2)
            
            if result_url:
                await msg.delete()
                await update.message.reply_photo(
                    photo=result_url, 
                    caption="✅ Voici ton résultat !\n\nPour des transformations illimitées, tape /premium"
                )
            else:
                await msg.edit_text("⏱ Délai dépassé. Réessaie dans quelques instants.")
        else:
            await msg.edit_text("❌ Erreur avec l'API. Réessaie plus tard.")
            
    except Exception as e:
        await msg.edit_text(f"❌ Erreur : {str(e)}")

def main():
    print("🤖 Bot démarré sur Render...")
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("premium", premium))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    print("✅ Bot prêt avec Replicate !")
    app.run_polling()

if __name__ == "__main__":
    main()
