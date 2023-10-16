import cv2
import pytesseract
from gtts import gTTS
import os

# Open the video file
cap = cv2.VideoCapture(0)

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

    # Use pytesseract to extract the bounding boxes of the text regions
    boxes = pytesseract.image_to_boxes(thresh)

    # Loop through each box and draw a rectangle around the text region
    for b in boxes.splitlines():
        b = b.split(' ')
        x, y, w, h = int(b[1]), int(b[2]), int(b[3]), int(b[4])
        cv2.rectangle(frame, (x, thresh.shape[0] - y), (w, thresh.shape[0] - h), (0, 0, 255), 2)

        # Extract the text inside the bounding box and add it to the extracted_text variable
        text = b[0]

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

original_text = '''Hey can you extract this'''

# Split the extracted text and the original text into words and characters
extracted_words = extracted_text.split()
original_words = original_text.split()
extracted_chars = list(extracted_text)
original_chars = list(original_text)

# Calculate the number of substitutions, deletions, and insertions
substitutions = sum(1 for i, j in zip(extracted_words, original_words) if i != j)
deletions = abs(len(original_words) - len(extracted_words))
insertions = abs(len(extracted_words) - len(original_words))

# Calculate the Word Error Rate (WER)
wer = (substitutions + deletions + insertions) / len(original_words)

# Calculate the number of substitutions, deletions, and insertions
substitutions = sum(1 for i, j in zip(extracted_chars, original_chars) if i != j)
deletions = abs(len(original_chars) - len(extracted_chars))
insertions = abs(len(extracted_chars) - len(original_chars))

# Calculate the Character Error Rate (CER)
cer = (substitutions + deletions + insertions) / len(original_chars)

print("Extracted text: ", extracted_text)
print("Original text: ", original_text)
print("Word Error Rate (WER): {:.2f}%".format(wer * 100))
print("Character Error Rate (CER): {:.2f}%".format(cer * 100))

language = 'en'
myobj = gTTS(text=extracted_text, lang=language, slow=False)

# Saving the converted audio in a mp3 file named speech
myobj.save("speech.mp3")

# Playing the converted file
os.system("mpg321 speech.mp3")
# Release the video capture and destroy all windows
cap.release()
cv2.destroyAllWindows()