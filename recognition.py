import face_recognition
from PIL import Image, ImageDraw
import numpy as np
import image_to_recognition
import cv2

known_face_encodings = []
known_face_names = []
image_to_recognition.images(known_face_encodings, known_face_names)

unknown_image = face_recognition.load_image_file("testphoto/bill_elon_steve1.jpg")
img = cv2.imread("testphoto/bill_elon_steve1.jpg")
face_locations = face_recognition.face_locations(unknown_image)
face_encodings = face_recognition.face_encodings(unknown_image, face_locations)
print(face_locations)
for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
    matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
    name = "Unknown"
    face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
    best_match_index = np.argmin(face_distances)
    if matches[best_match_index]:
        name = known_face_names[best_match_index]
        print(name)

    cv2.rectangle(img, (left, top), (right, bottom), (0, 255, 0), 3)
    font = cv2.FONT_HERSHEY_SIMPLEX
    [(width, height), baseline] = cv2.getTextSize(name, font, 1.0, 3)
    cv2.rectangle(img, (left + 3, bottom - height - 8), (left + width + 5, bottom - 3), (0, 0, 0), cv2.FILLED)

    cv2.putText(img, name, (left + 5, bottom - 5), font, 1.0, (255, 255, 0), 3)

cv2.imwrite("savephoto/image_with_boxes.jpg", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
