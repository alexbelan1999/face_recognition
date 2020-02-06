import face_recognition
import numpy as np
import image_to_recognition
import cv2
import datetime
import glob
import time

clock1 = time.time()
known_face_encodings = []
known_face_names = []
image_to_recognition.images(known_face_encodings, known_face_names)
print("Time 1:",time.time()-clock1)
for file in glob.glob("testphoto/*"):
    clock3 = time.time()
    unknown_image = face_recognition.load_image_file(file)
    img = cv2.imread(file)
    face_locations = face_recognition.face_locations(unknown_image)
    face_encodings = face_recognition.face_encodings(unknown_image, face_locations)
    names = []
    print("Time 2:",time.time()-clock3)
    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        clock4  = time.time()
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        name = "Unknown"

        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        best_match_index = np.argmin(face_distances)

        if matches[best_match_index]:
            name = known_face_names[best_match_index]
        names.append(name)

        cv2.rectangle(img, (left, top), (right, bottom), (0, 255, 0), 3)
        font = cv2.FONT_HERSHEY_SIMPLEX
        [(width, height), baseline] = cv2.getTextSize(name, font, 1.0, 3)
        cv2.rectangle(img, (left + 3, bottom - height - 8), (left + width + 5, bottom - 3), (0, 0, 0), cv2.FILLED)
        cv2.putText(img, name, (left + 5, bottom - 5), font, 1.0, (255, 255, 0), 3)
        print("Time 3:",time.time()-clock4)

    clock5 = time.time()
    print(file, " ", names)
    basename = ""
    for i in names:
        basename += str(i) + '_'

    suffix = datetime.datetime.now().strftime("%H_%M_%S_%d_%m_%Y")
    filename = "".join([basename, suffix])
    path = "savephoto/" + filename + '.jpg'

    if len(names) > 0:
        cv2.imwrite(path, img)
    print("Time 4:",time.time()-clock5)
    print("Time 5:", time.time() - clock3)


clock2 = time.time()
print("All time:", clock2 - clock1)
