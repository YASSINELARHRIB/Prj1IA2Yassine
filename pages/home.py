import streamlit as st
from database import *
import io
from PIL import Image
from rechercheImages import *

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

st.title("Page d'accueil")

st.write(f"Bienvenue , {st.session_state['user_info']['name']}")

st.write("Voici vos informations :")
st.write(f"Email : {st.session_state['user_email']}")

# effectuer la recherche sur de nombres d'images similaires a une photo entrer.
# charger une photo
photo = st.file_uploader("Téléchargez une photo", type=["png", "jpg", "jpeg"])




# Afficher l'image téléchargée
if photo is not None:


    image = Image.open(photo)
    st.image(image, caption="Image téléchargée", use_column_width=True)
    
    # Convertir l'image en tableau numpy
    image_np = np.array(image)
    gray_image = cv2.cvtColor(image_np, cv2.COLOR_RGB2GRAY)

    
    
    signatureGLCM = np.load('SignaturesGLCM.npy')
    signatureConcat = np.load('SignaturesConcat.npy')
    signatureBit = np.load('SignaturesBEATD.npy')
    signatureHaralick = np.load('SignaturesHARALICK.npy')


    carac_GLCM = glcm(gray_image)
    carac_Concat = concatenation(gray_image)
    carac_Beatd = bitdesc(gray_image)
    carac_Haralick = haralick_feat(gray_image)


    nombre_images = st.number_input("Combien d'images similaires voulez-vous ?", min_value=1, max_value=10, value=5)
    # on va lui demander de choisir le type de distance
    distances = st.selectbox("Choisissez le type de distance", ["euclidienne", "canberra", "manhattan", "chebyshev"])
    # on va lui demander de choisir le type de signature
    carac = st.selectbox("Choisissez le type de signature", ["GLCM", "Concaténation", "BEATD", "Haralick"])
    # on va lui demander de choisir le type de signature
    if carac == "GLCM":
        signature = signatureGLCM
        carac_imag_requete = carac_GLCM
    elif carac == "Concaténation":
        signature = signatureConcat
        carac_imag_requete = carac_Concat
    elif carac == "BEATD":
        signature = signatureBit
        carac_imag_requete = carac_Beatd
    elif carac == "Haralick":
        signature = signatureHaralick
        carac_imag_requete = carac_Haralick

    # maintenant on va lui donner la resultats du recherche sous forme de cadre contient les photos smilaires

    # if st.button("Rechercher"):
    #     resultat = rechercheImage(SignatureBase=signature, carac_imag_requete=carac, distance=distances, K = 10)
    #     # Afficher les résultats
    #     st.write("Résultats de la recherche :")
    #     # afficher en fonction de nombre d'images demandé
    #     for i, x in enumerate(resultat[:nombre_images]):
    #         img = cv2.imread(f'dataset/{x[0]}')
    #         # on va afficher les images dans un cadre
    #         st.image(img, caption=f'Image {i+1}', use_column_width=True)
    #         # on va afficher le nom de l'image
    #         st.write(f"Nom de l'image : {x[0]}")
    #         # on va afficher la distance
    #         st.write(f"Distance : {x[1]}")
    #         # on va afficher la signature
    #         st.write(f"Signature : {x[2]}")
    #         # on va afficher le type de signature
    #         st.write(f"Type de signature : {carac}")
    #         # on va afficher le type de distance
    #         st.write(f"Type de distance : {distances}")
    #         # on va afficher le nombre d'images similaires
    #         st.write(f"Nombre d'images similaires : {nombre_images}")
    if st.button("Rechercher"):
        # Ca c'est un esuggestion de chatgpt 
        with st.spinner("Recherche en cours..."):
            resultat = rechercheImage(SignatureBase=signature, carac_imag_requete=carac_imag_requete, distance=distances, K=nombre_images)

        st.success("Recherche terminée !")
        st.subheader("Résultats de la recherche :")
        seuil_distance = 1.5 # seuil de distance pour filtrer les résultats
        resultat_filtré = [x for x in resultat if x[1] <= seuil_distance]

        for i, (nom_image, dist, sig) in enumerate(resultat_filtré[:nombre_images]):
            img = cv2.imread(f'animalsCbir/{nom_image}')
            
            if img is not None:
                img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # pour affichage correct avec Streamlit
                st.image(img_rgb, caption=f'Image {i+1}', use_column_width=True)
                st.markdown(f"**Nom :** `{nom_image}`  \n**Distance :** `{dist:.4f}`  \n**Type de signature :** `{carac}`  \n**Type de distance :** `{distances}`")
            else :
                st.warning("Aucune image trouvée.")
    

