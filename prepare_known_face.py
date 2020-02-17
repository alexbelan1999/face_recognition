import image_to_recognition
import dump_and_load_pickle as dalp

def prepare(encodings : str, names : str):
    known_face_encodings = []
    known_face_names = []

    image_to_recognition.images(known_face_encodings, known_face_names)
    dalp.dump(known_face_encodings,encodings)
    dalp.dump(known_face_names,names)

prepare("encodings2","names2")
