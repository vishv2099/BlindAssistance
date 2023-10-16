import cv2
import pytesseract
from gtts import gTTS
import os

# Open the video file
cap = cv2.VideoCapture('egvideo.mp4')

# Configure pytesseract
extracted_text = ""
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Loop through each frame in the video
while cap.isOpened():
    # Read the current frame
    ret, frame = cap.read()
    if not ret:
        break

    # Convert the frame to grayscale and apply thresholding
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

    # Use pytesseract to extract the text from the thresholded image
    text = pytesseract.image_to_string(thresh)

    # Print the extracted text
    if (text not in extracted_text):
        extracted_text += text

    # Show the frame
    cv2.imshow('frame', frame)

    # Exit if 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

#print(text)
print(extracted_text)

language = 'en'
myobj = gTTS(text=extracted_text, lang=language, slow=False)

# Saving the converted audio in a mp3 file named speech
myobj.save("speech.mp3")

# Playing the converted file
os.system("mpg321 speech.mp3")
# Release the video capture and destroy all windows
cap.release()
cv2.destroyAllWindows()