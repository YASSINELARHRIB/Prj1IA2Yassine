import streamlit as st
from PIL import Image
from database import *
from authlib.integrations.requests_client import OAuth2Session
import requests
from urllib.parse import urlencode

# Configuration OAuth Google & Facebook
GOOGLE_CLIENT_ID = "91793469193-9ktf4f04l8mhc9npnrg52nqsct0sojf1.apps.googleusercontent.com"
GOOGLE_CLIENT_SECRET = "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"
GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/auth"
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_USER_INFO = "https://www.googleapis.com/oauth2/v2/userinfo"
GOOGLE_REDIRECT_URI = "http://localhost:8501/"

FACEBOOK_CLIENT_ID = "3813930195603999"
FACEBOOK_CLIENT_SECRET = "8f6d7b1593b7b9c89c184874f52797b6"
FACEBOOK_AUTH_URL = "https://www.facebook.com/v12.0/dialog/oauth"
FACEBOOK_TOKEN_URL = "https://graph.facebook.com/v12.0/oauth/access_token"
FACEBOOK_USER_INFO = "https://graph.facebook.com/me?fields=id,name,email,picture"
FACEBOOK_REDIRECT_URI = "http://localhost:8501/"

# 📌 Initialisation de l'état de connexion
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False
if "user_email" not in st.session_state:
    st.session_state["user_email"] = None

# Fonction d'authentification Google
def authenticate_google():
    params = {
        "client_id": GOOGLE_CLIENT_ID,
        "redirect_uri": GOOGLE_REDIRECT_URI,
        "response_type": "code",
        "scope": "openid email profile",
        "access_type": "offline",
        "prompt": "consent"
    }
    auth_url = f"{GOOGLE_AUTH_URL}?{urlencode(params)}"
    conne = st.markdown(f"[Se connecter avec Google]({auth_url})")

# Récupération du token après redirection
def get_google_token(auth_code):
    data = {
        "client_id": GOOGLE_CLIENT_ID,
        "client_secret": GOOGLE_CLIENT_SECRET,
        "redirect_uri": GOOGLE_REDIRECT_URI,
        "grant_type": "authorization_code",
        "code": auth_code
    }
    response = requests.post(GOOGLE_TOKEN_URL, data=data)
    return response.json()

# Récupération des infos de l'utilisateur Google
def get_google_user_info(access_token):
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(GOOGLE_USER_INFO, headers=headers)
    return response.json()

# Vérifier si on a un "code" dans l'URL (retour OAuth)
query_params = st.query_params
if "code" in query_params and not st.session_state["authenticated"]:
    auth_code = query_params["code"]
    token_response = get_google_token(auth_code)
    
    if "access_token" in token_response:
        user_info = get_google_user_info(token_response["access_token"])
        st.session_state["authenticated"] = True
        st.session_state["user_info"] = user_info
        st.success(f"Bienvenue {user_info['name']} ! 🎉")

        # Forcer une redirection pour rafraîchir l’état
        st.rerun()





if st.session_state["authenticated"]:
    st.success(f"Bienvenue {st.session_state['user_info']['name']} ! 🎉")
    st.image(st.session_state['user_info']['picture'], width=100)
    st.switch_page("pages/home.py")  # Rediriger vers home seulement si connecté
else:
    authenticate_google()


# 📌 Interface Utilisateur
st.title("App : Your WebSite")
menu = st.sidebar.selectbox("Menu", ["Inscription", "Connexion"])

if menu == "Inscription":
    st.subheader(" Inscription")
    name = st.text_input("Nom")
    email = st.text_input("Email")
    password = st.text_input("Mot de passe", type="password")
    photo = st.file_uploader("Téléchargez une photo", type=["png", "jpg", "jpeg"])

    if st.button("S'inscrire"):
        if name and email and password and photo:
            if get_user(email):  
                st.error("Erreur : User Already exist !")
            else:
                image = Image.open(photo)
                photo_blob = convert_image_to_blob(image)
                save_user(name, email, password, photo_blob)
                st.success("Inscription réussie ! Vous pouvez vous connecter.")
        else:
            st.error("Veuillez remplir tous les champs.")

elif menu == "Connexion":
    st.subheader(" Connexion")
    
    st.write("Connexion via OAuth :")
    if st.button("Google"):
        authenticate_google()
    if st.button("Facebook"):
        authenticate_google()

    login_method = st.radio("Méthode de connexion", ["Email/Mot de passe", "Reconnaissance faciale"])

    if login_method == "Email/Mot de passe":
        email = st.text_input("Email")
        password = st.text_input("Mot de passe", type="password")

        if st.button("Se connecter"):
            user = get_user(email)
            if user and check_password(user[3], password):
                st.session_state["authenticated"] = True
                st.session_state["user_email"] = email
                st.success(f"Connexion réussie, {user[1]} ! 🚀")
                st.rerun()  # Recharge la page pour déclencher la redirection
            else:
                st.error("Identifiants incorrects.")

    elif login_method == "Reconnaissance faciale":
        st.subheader(" Connexion par reconnaissance faciale")
        if st.button("Se connecter avec la caméra"):
            facial_recognition_live()

    
