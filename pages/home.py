import streamlit as st

# Vérifier si l'utilisateur est bien connecté
if "authenticated" not in st.session_state or not st.session_state["authenticated"]:
    st.warning("Vous devez vous connecter pour accéder à cette page.")
    st.switch_page("app.py")

st.title("Page d'accueil")
st.write(f"Bienvenue {st.session_state['user_email']} !")

# Bouton de déconnexion
if st.button("Se déconnecter"):
    st.session_state["authenticated"] = False
    st.session_state["user_email"] = None
    st.switch_page("app.py")
