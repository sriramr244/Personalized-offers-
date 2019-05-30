import face_recognition
import cv2
import numpy as np
import os
import requests
import mysql.connector

#intialize previous variables
Previous_value=[]


#initialize the online database which is free upto 5mb
mydb = mysql.connector.connect(
  host="sql12.freesqldatabase.com",
  user="sql12293211",
  passwd="limPmNk2cw",
  database="sql12293211"
)


#initialize the cursor for the db
mycursor = mydb.cursor()


#function for checking if the offer is available for a person
def checkOffer(number): 
#if available sending sms using fast2sms which free upto 20 msgs
	def sendMsg(number,tableName):
		url = "https://www.fast2sms.com/dev/bulk"

		payload0= 'sender_id=FSTSMS&message='
		payload1='Hi user you have got an offer of 10% on your next purchase in'+str(tableName)
		payload2='&language=english&route=p&numbers='
		payload3=number
		payload=payload0+payload1+payload2+payload3
		headers = {
		'authorization': "UrqyvmP6N1Ap7MCWOdak09FtufxzYoQBVXnHlJs2EbwZjGiS54uwXrbSQzYGmTR34IyfalsEekpNUHdC",
		'Content-Type': "application/x-www-form-urlencoded",
		'Cache-Control': "no-cache",
		}

		response = requests.request("POST", url, data=payload, headers=headers)

		print(response.text)


	print('mobile number',name)			
	table=['grocery','electronics','food']
	for tableName in table:
		a='SELECT * FROM '
		b=str(tableName)
		c=' where Mnumber = %s'
		sql=a+b+c
		mycursor.execute(sql,(number,))
		result=mycursor.fetchall()
		if result!=[]:		
			n=result[0]
			i=int(n[1])
			if i>1: 
				sendMsg(number,tableName)
				print('mobile number',name)
		else:
			continue
	return			
#capture from the webcam
video_capture = cv2.VideoCapture(0)


known_face_encodings=[]
known_face_names=[]

#save the images in the dataset folder
path = "dataset"
folder_path = [os.path.join(path,f) for f in os.listdir(path)]
for folder_name in folder_path:
	folder = [os.path.join(folder_name,f) for f in os.listdir(folder_name)]
	known_face_names.append(folder_name.split('/')[1])
	for image_name in folder:
# Load a pictures and learn how to recognize it.
		image = face_recognition.load_image_file(image_name)
		face_encoding = face_recognition.face_encodings(image)[0]
		known_face_encodings.append(face_encoding)
		print(face_encoding)
print(known_face_encodings)




# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True
best_match_index=0
found=False

while True:
    # Grab a single frame of video
	ret, frame = video_capture.read()

    # Resize frame of video to 1/4 size for faster face recognition processing
	small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
	rgb_small_frame = small_frame[:, :, ::-1]

    # Only process every other frame of video to save time
	if process_this_frame:
        # Find all the faces and face encodings in the current frame of video
		face_locations = face_recognition.face_locations(rgb_small_frame)
		face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

	face_names = []
	for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
		matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
		print(matches)

		number = "Unknown"

		face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
		best_match_index = np.argmin(face_distances)
		print(best_match_index)
		if matches[best_match_index]:
			number = known_face_names[best_match_index]
			found=True

		face_names.append(number)

	process_this_frame = not process_this_frame


    # Display the results
	for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
		top *= 4
		right *= 4
		bottom *= 4
		left *= 4

        # Draw a box around the face
		cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with a name below the face
		cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
		font = cv2.FONT_HERSHEY_DUPLEX
		cv2.putText(frame, number, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

	cv2.imshow('frame',frame)
	if found:
		if number not in Previous_value:
			checkOffer(number)
			Previous_value.append(number)
		
	if cv2.waitKey(1)==ord('q'):
		break;

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()




