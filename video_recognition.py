import face_recognition
import numpy as np
import image_to_recognition
import cv2
import datetime
import time
import postgresql as pg
import dump_and_load_pickle as dalp

clock1 = time.time()
input_movie = cv2.VideoCapture("Bill.mp4")
length = int(input_movie.get(cv2.CAP_PROP_FRAME_COUNT))

# known_face_encodings = []
# known_face_names = []

# image_to_recognition.images(known_face_encodings, known_face_names)
# dalp.dump(known_face_encodings,"encodings1")
# dalp.dump(known_face_names,"names1")
known_face_encodings = dalp.load("encodings1")
known_face_names = dalp.load("names1")
frame_number = 0

seconds = 1
fps = input_movie.get(cv2.CAP_PROP_FPS)
multiplier = round(fps * seconds)

while True:
    ret, frame = input_movie.read()
    frame_number += 1

    if not ret:
        break
    if frame_number % multiplier == 0:
        rgb_frame = frame[:, :, ::-1]

        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        names = []

        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"

            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)

            if matches[best_match_index]:
                name = known_face_names[best_match_index]
            names.append(name)

            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 3)
            font = cv2.FONT_HERSHEY_SIMPLEX
            [(width, height), baseline] = cv2.getTextSize(name, font, 1.0, 3)
            cv2.rectangle(frame, (left + 3, bottom - height - 8), (left + width + 5, bottom - 3), (0, 0, 0), cv2.FILLED)
            cv2.putText(frame, name, (left + 5, bottom - 5), font, 1.0, (255, 255, 0), 3)

        if len(names) == 0:
            continue

        print("Person: ", names)
        basename = ""
        persons = []

        suffix = datetime.datetime.now().strftime("%H_%M_%S_%d_%m_%Y")
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        for i in names:
            basename += str(i) + '_'
            persons.append([str(i), timestamp])

        filename = "".join([basename, suffix])
        path = "savephoto/" + filename + '.jpg'

        if len(names) > 0:
            cv2.imwrite(path, frame)
            pg.insert(persons)

    print("Обработка  {} / {}".format(frame_number, length))

input_movie.release()
cv2.destroyAllWindows()
print("Time:", time.time() - clock1)
