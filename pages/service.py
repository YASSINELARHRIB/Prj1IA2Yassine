import streamlit as st

# Bouton de déconnexion
if st.button("Se déconnecter"):
    st.session_state["authenticated"] = False
    st.session_state["user_email"] = None
    st.switch_page("app.py")
                   
# Vérifier si l'utilisateur est bien connecté
if "authenticated" not in st.session_state or not st.session_state["authenticated"]:
    st.warning("Vous devez vous connecter pour accéder à cette page.")
    st.switch_page("app.py")


# Initialize session state
if "user_info" not in st.session_state:
    st.session_state["user_info"] = {"name": "Utilisateur inconnu"}

# Page de service
st.title("Page de service")
st.write("Bienvenue dans la page de service !")
st.write("Voici quelques fonctionnalités disponibles :")
st.write("- **Reconnaissance faciale** : Identifiez-vous rapidement et facilement.")
st.write("- **Gestion des utilisateurs** : Ajoutez, modifiez ou supprimez des utilisateurs.")
st.write("- **Gestion des données** : Accédez et gérez vos données personnelles.")
st.write("- **Sécurité** : Vos données sont protégées et sécurisées.")
st.write("- **Assistance** : Contactez-nous pour toute question ou problème dans la section Contact.")