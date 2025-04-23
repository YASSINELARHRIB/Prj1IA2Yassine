

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

st.title("Page de contact")

# on met une page de contact professionnelle
st.write("Pour toute question ou suggestion, n'hésitez pas à nous contacter :")
# on laisse une formulaire de contact
st.write("Nom :")
name = st.text_input("Nom")
st.write("Email :")
email = st.text_input("Email")
st.write("Message :")
message = st.text_area("Message")
if st.button("Envoyer"):
    if name and email and message:
        st.success("Votre message a été envoyé avec succès !")
    else:
        st.error("Veuillez remplir tous les champs.")
# on laisse un lien de github 
st.write("Vous pouvez également consulter notre code source sur GitHub :")
st.write("https://github.com/YASSINELARHRIB/Prj1IA2Yassine.git")