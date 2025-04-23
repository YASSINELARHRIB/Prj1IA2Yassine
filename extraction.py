import os
import numpy as np
from rechercheImages import glcm, concatenation, haralick_feat, bitdesc
 
 
def ExtractionSignatures(chemin_repertoire):
    list_carac=[]
    ##print(chemin_repertoire)
    for root,_,files in os.walk(chemin_repertoire):
        for file in files:
            if file.lower().endswith(('.png','.jpg','.jpeg','.bmp')):
                relative_path=os.path.relpath(os.path.join(root,file),chemin_repertoire)
                
                path=os.path.join(root,file)
                carac=bitdesc(path)
                print(carac)
                class_name=os.path.dirname(relative_path)
                list_carac.append(carac+[class_name,relative_path])
    signatures=np.array(list_carac)
    np.save('SignaturesBEATD.npy',signatures)
               
def main():
    
    ExtractionSignatures('./animalsCbir/')
 
 
if __name__=='__main__':
    main()