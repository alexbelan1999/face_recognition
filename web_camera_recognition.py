import face_recognition
import numpy as np
import image_to_recognition
import cv2
import datetime
import glob

known_face_encodings = []
known_face_names = []
image_to_recognition.images(known_face_encodings, known_face_names)

video_capture = cv2.VideoCapture(0)

while True:
    ret, frame = video_capture.read()
    frame = cv2.flip(frame, 1)
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

    print("Person: ", names)
    basename = ""
    for i in names:
        basename += str(i) + '_'

    suffix = datetime.datetime.now().strftime("%H_%M_%S_%d_%m_%Y")
    filename = "".join([basename, suffix])
    path = "savephoto/" + filename + '.jpg'

    if len(names) > 0:
        cv2.imwrite(path, frame)

    cv2.imshow('Video', frame)
    key = cv2.waitKey(100)
    if key == 27:
        break

video_capture.release()
cv2.destroyAllWindows()
