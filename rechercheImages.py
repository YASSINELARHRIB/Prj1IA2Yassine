from skimage.feature import graycomatrix, graycoprops as greycoprops
from mahotas.features import haralick
from BiT import bio_taxo
import numpy as np
import cv2
import numpy as np
from scipy.spatial import distance


def glcm(chemin) :
    
    coMatrix = graycomatrix(chemin,[1],[np.pi/2],None,symmetric=True,normed = False)
    contrast = float(greycoprops(coMatrix, 'contrast')[0,0])
    dissimilarity = float(greycoprops(coMatrix, 'dissimilarity')[0,0])
    homogeneity = float(greycoprops(coMatrix, 'homogeneity')[0,0])
    correlation = float(greycoprops(coMatrix, 'correlation')[0,0])
    Asm = float(greycoprops(coMatrix, 'ASM')[0,0])
    energy = float(greycoprops(coMatrix, 'energy')[0,0])
    
    return [contrast, dissimilarity, homogeneity, energy, correlation, Asm]


def haralick_feat(chemin):
    features = haralick(chemin).mean(0).tolist()
    features = [float(x) for x in features]
    return features

def bitdesc(chemin) :
    features = bio_taxo(chemin)
    return features

def concatenation(chemin):
    return glcm(chemin) + haralick_feat(chemin) + bitdesc(chemin)

 
def manhattan(v1,v2):
    v1=np.array(v1).astype('float')
    v2=np.array(v2).astype('float')
    dist=np.sum(np.abs(v1-v2))
    return dist
 
def euclidienne(v1,v2):
    v1=np.array(v1).astype('float')
    v2=np.array(v2).astype('float')
    dist = np.sqrt(np.sum((v1 - v2)**2))
    return dist
 
def chebyshev(v1,v2):
    v1=np.array(v1).astype('float')
    v2=np.array(v2).astype('float')
    dist=np.max(np.abs(v1-v2))
    return dist
 
def canberra (v1,v2):
    v1 = [float(i) for i in v1]
    v2 = [float(i) for i in v2]

    v1 = np.array(v1, dtype=np.float64)
    v2 = np.array(v2, dtype=np.float64)
    return distance.canberra(v1,v2)

def rechercheImage (SignatureBase, carac_imag_requete, distance, K) :
    listSimilaire = []
    for instance in SignatureBase:
        carac, label, imgChemin = instance[:-2], instance[-2], instance[-1]
        if distance == 'canberra':
            dist = canberra(carac, carac_imag_requete)
        if distance == 'euclidienne':
            dist = euclidienne(carac, carac_imag_requete)
        if distance == 'chebyshev':
            dist = chebyshev(carac, carac_imag_requete)
        if distance == 'manhattan':
            dist = manhattan(carac, carac_imag_requete)
        listSimilaire.append((imgChemin, dist, label))
    listSimilaire.sort(key=lambda x:x[1])
    return listSimilaire[:K]