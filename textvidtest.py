import cv2
import pytesseract

# Open the video file
cap = cv2.VideoCapture('egvideo.mp4')

# Configure pytesseract
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
    print(text)

    # Show the frame
    cv2.imshow('frame', frame)

    # Exit if 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture and destroy all windows
cap.release()
cv2.destroyAllWindows()