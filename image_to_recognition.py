import glob
import os
import face_recognition

known_face_encodings = []
known_face_names = []
def images(known_face_encodings ,known_face_names ):
    for file in glob.glob("person/*"):
        image = face_recognition.load_image_file(file)
        known_face_encodings.append(face_recognition.face_encodings(image)[0])
        known_face_names.append(os.path.splitext(os.path.basename(file))[0])
    pass
