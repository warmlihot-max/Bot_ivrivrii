import telebot
from telebot import types

TOKEN = "8923256604:AAEagZg0oyEh-rVrAFlSVjyY8_XXgZMCzqI"
bot = telebot.TeleBot(TOKEN)

# --- MENU DU RESTAURANT ---
MENU_PRODUITS = {
    "🍔 Plat Principal": "Plats locaux et burgers maison - 3 500 FCFA",
    "🍹 Boisson Fraîche": "Jus locaux, sodas et cocktails - 1 000 FCFA",
    "🍰 Dessert Gourmand": "Douceurs du jour - 1 500 FCFA"
}

# --- CLAVIER PRINCIPAL ---
def menu_principal_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_menu = types.KeyboardButton("📖 Voir le Menu")
    btn_infos = types.KeyboardButton("ℹ️ Horaires & Contact")
    btn_commander = types.KeyboardButton("🛒 Passer une commande")
    markup.add(btn_menu, btn_infos)
    markup.add(btn_commander)
    return markup

# --- COMMANDE /START ---
@bot.message_handler(commands=['start'])
def send_welcome(message):
    prenom = message.from_user.first_name
    texte = (
        f"Bienvenue chez **IVRIVRII** ! 🍽️✨\n\n"
        f"Salut {prenom}, installe-toi confortablement. "
        "Que puis-je faire pour toi aujourd'hui ? Utilise les boutons ci-dessous pour explorer !"
    )
    bot.send_message(message.chat.id, texte, reply_markup=menu_principal_markup(), parse_mode="Markdown")

# --- GESTION DES BOUTONS TEXTES ---
@bot.message_handler(func=lambda message: True)
def handle_messages(message):
    if message.text == "📖 Voir le Menu":
        texte_menu = "✨ **LE MENU IVRIVRII** ✨\n\n"
        for item, detail in MENU_PRODUITS.items():
            texte_menu += f"• **{item}**\n  └ {detail}\n\n"
        texte_menu += "💡 _Pour commander, clique sur le bouton correspondant en bas !_"
        bot.send_message(message.chat.id, texte_menu, parse_mode="Markdown")

    elif message.text == "ℹ️ Horaires & Contact":
        # On ajoute l'adresse et le lien de localisation ici
        infos = (
            "📍 **Notre Adresse :**\n"
            "Quartier Hedzranawoé, Boulevard du 13 Janvier, Lomé, Togo 🇹🇬\n"
            "_(Juste à côté de la grande pharmacie)_\n\n"
            "🕒 **Nos Horaires :**\n"
            "Du Lundi au Samedi : 11h30 - 22h00\n"
            "Dimanche : Fermé\n\n"
            "📞 **Contact & Réservations :**\n"
            "Appelle-nous au +228 XX XX XX XX !"
        )
        
        # Petit bonus : un bouton cliquable qui ouvre Google Maps
        markup_maps = types.InlineKeyboardMarkup()
        # Remplace ce lien par le vrai lien Google Maps de ton resto plus tard !
        btn_maps = types.InlineKeyboardButton("🗺️ Ouvrir dans Google Maps", url="https://maps.google.com")
        markup_maps.add(btn_maps)
        
        bot.send_message(message.chat.id, infos, reply_markup=markup_maps, parse_mode="Markdown")

    elif message.text == "🛒 Passer une commande":
        markup_inline = types.InlineKeyboardMarkup()
        for item in MENU_PRODUITS.keys():
            btn = types.InlineKeyboardButton(item, callback_data=f"cmd_{item}")
            markup_inline.add(btn)
        bot.send_message(message.chat.id, "🛒 **Qu'est-ce qui te fait envie ?** Choisis ton article :", reply_markup=markup_inline, parse_mode="Markdown")
    
    else:
        bot.reply_to(message, "Je n'ai pas bien compris. Utilise les boutons en bas pour naviguer ! 😊")

# --- GESTION DES CLICS SUR LES BOUTONS DE COMMANDE ---
@bot.callback_query_handler(func=lambda call: call.data.startswith("cmd_"))
def callback_commande(call):
    article = call.data.replace("cmd_", "")
    confirmation = (
        f"✅ **Commande enregistrée !**\n\n"
        f"Tu as choisi : **{article}**\n"
        f"Notre équipe prépare ton plat. Merci de ta confiance chez IVRIVRII ! 🎉"
    )
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=confirmation, parse_mode="Markdown")
    bot.answer_callback_query(call.id, text="Commande reçue !")

# Lancement du serveur
if __name__ == "__main__":
    print("🤖 Le bot Restaurant IVRIVRII est en ligne...")
    bot.infinity_polling()
