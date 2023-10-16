import cv2
import pytesseract
from gtts import gTTS
import os

# Open the video file
cap = cv2.VideoCapture('egvideo.mp4')

# Configure pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Loop through each frame in the video
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Convert the frame to grayscale and apply thresholding
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

    # Use pytesseract to extract the text from the thresholded image
    text = pytesseract.image_to_string(frame)

    # creating the bounding boxes
    imgH, imgW, _ = frame.shape
    x1, y1, w1, h1 = 0, 0, imgH, imgW
    imgboxes = pytesseract.image_to_boxes(frame)
    for boxes in imgboxes.splitlines():
        boxes = boxes.split(' ')
        x, y, w, h = int(boxes[1]), int(boxes[2]), int(boxes[3]), int(boxes[4])
        cv2.rectangle(frame, (x, imgH - y), (w, imgH - h), (0, 0, 255), 3)
        cv2.putText(frame, text, (x1 + int(w1 / 50), y1 + int(h1 / 50)), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 0, 255), 2)

        # converting the text into audio file
    language = 'en'

    if (text != ""):
        myobj = gTTS(text=text, lang=language, slow=False)

        # Saving the converted audio in a mp3 file named speech
        myobj.save("speech.mp3")

        # Playing the converted file
        os.system("mpg321 speech.mp3")

        # Print the extracted text
        print(text)

    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()