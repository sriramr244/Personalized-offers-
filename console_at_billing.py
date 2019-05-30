from tkinter import *
import mysql.connector
import cv2
import numpy as numpy
import os, time
import dlib
from imutils import face_utils
from imutils.face_utils import FaceAligner






#the product type is only of three:1.'electronics' 2.'grocery' 3. 'food'
#each product type consists of two attributes 1.Mnumber 2.count(how many times they have bought that)

mydb = mysql.connector.connect(
  host="sql12.freesqldatabase.com",
  user="sql12293211",
  passwd="limPmNk2cw",
  database="sql12293211"
)



mycursor = mydb.cursor()
Mnumber=0
def check():
	print('entered check')
	def newuser(Mnumber):
		detector = dlib.get_frontal_face_detector()
		shape_predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
		face_aligner = FaceAligner(shape_predictor, desiredFaceWidth=200)

		FACE_DIR = "dataset/"


		def create_folder(folder_name):
			if not os.path.exists(folder_name):
        			os.mkdir(folder_name)
		def captur():
			create_folder(FACE_DIR)
			while True:
				name='x'
				face_id = Mnumber
				try:
					face_id = int(face_id)
					face_folder = FACE_DIR + str(face_id) + "/"
					create_folder(face_folder)
					break
				except:
					print("Invalid input. id must be int")
					continue

    # get beginning image number
			

			img_no = 0
			cap = cv2.VideoCapture(0)
			total_imgs = 1
			while True:
				ret, img = cap.read()
				img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
				faces = detector(img_gray)
				if len(faces) == 1:
					face = faces[0]
					(x, y, w, h) = face_utils.rect_to_bb(face)
					face_img = img_gray[y-50:y + h+100, x-50:x + w+100]
					face_aligned = face_aligner.align(img, img_gray, face)

					face_img = face_aligned
					img_path = face_folder +name+ str(img_no) + ".jpg"
					cv2.imwrite(img_path, face_img)
					cv2.rectangle(img, (x, y), (x + w, y + h), (255, 255, 0), 3)
					img_no += 1

				cv2.imshow("Saving", img)
				cv2.waitKey(1)
				if img_no == total_imgs:
					cv2.destroyAllWindows()
					break

			cap.release()


		def upload():
			Name=EntryName.get()
			Number=Mnumber
			ProductType=EntryProductType.get()
			NOTV=1
			DOV=EntryDOV.get()
			Dbupload=(str(Name),str(Mnumber),str(NOTV),str(DOV))
			mycursor.execute("INSERT INTO MasterTable (name, Mnumber,NOTV,DOV) VALUES (%s,%s,%s,%s)",Dbupload)
			mydb.commit()
			a='INSERT INTO '
			b=str(ProductType)
			count=str(1)
			c=' (Mnumber,count) VALUES (%s,%s)'
			sql=a+b+c
			d=(str(Mnumber),count)
			mycursor.execute(sql,d)
			mydb.commit()
			SecondWindow.destroy()
			captur()
		SecondWindow=Tk()
		LabelName=Label(SecondWindow,text='NAME')
		LabelName.pack(side=LEFT)
		LabelName.place(relx=0.1,rely=0.05)
		LabelMnumber=Label(SecondWindow,text='MOBILE NUMBER')
		LabelMnumber.pack(side=LEFT)
		LabelMnumber.place(relx=0.1,rely=0.1)
		LabelProductType=Label(SecondWindow,text='PRODUCT TYPE')
		LabelProductType.pack(side=LEFT)
		LabelProductType.place(relx=0.1,rely=0.15)
		LabelDOV=Label(SecondWindow,text='DATE OF VISIT')
		LabelDOV.pack(side=LEFT)
		LabelDOV.place(relx=0.1,rely=0.2)
		EntryName=Entry(SecondWindow,bd=5)
		EntryName.pack(side=RIGHT)
		EntryName.place(relx=0.7,rely=0.05)
		EntryNumber=Label(SecondWindow,text=str(Mnumber))
		EntryNumber.pack(side=RIGHT)
		EntryNumber.place(relx=0.7,rely=0.1)
		EntryProductType=Entry(SecondWindow,bd=5)
		EntryProductType.pack(side=RIGHT)
		EntryProductType.place(relx=0.7,rely=0.15)
		EntryDOV=Entry(SecondWindow,bd=5)
		EntryDOV.pack(side=RIGHT)
		EntryDOV.place(relx=0.7,rely=0.2)
		ButtonUpload=Button(SecondWindow,text="UPLOAD",command=upload)
		ButtonUpload.place(relx=0.3,rely=0.25)

	def olduser(Mnumber,result1):
		def update():
			ProductType=EntryProductType.get()
			DOV=EntryDOV.get()
			n=result1[0]
			m=str(int(n[2])+1)
			Dbupload=(n[0],n[1],m,DOV)
			print('uploading the db with updated NOTV, and DOV')
			print(Dbupload)
			mycursor.execute("INSERT INTO MasterTable (name, Mnumber,NOTV,DOV) VALUES (%s,%s,%s,%s)",Dbupload)
			mydb.commit()
			print(ProductType)
			print('Searching in the above')
			a='SELECT * FROM '
			b=str(ProductType)
			c=' where Mnumber = %s'
			sql=a+b+c
			mycursor.execute(sql,(Mnumber,))
	
			result=mycursor.fetchall()
			if result!=[]:
				print('got the below result')
				print(result)
				a2='DELETE FROM '
				sql=a2+b+c
				print('Deleting it from the product type table')
				mycursor.execute(sql,(Mnumber,))
				mydb.commit()
				x=result[0]
				m=str(int(x[1])+1)
				print('inserting the updated version')
				a1='INSERT INTO '
				c1=' (Mnumber, count) VALUES (%s,%s)'
				sql=a1+b+c1
				d=(Mnumber,m)
				mycursor.execute(sql,d)
				mydb.commit()
				print('record updated in product table')
				SecondWindow.destroy()
					
			else:
				print('result not found so inserting count as one')
				m=str(1)
				a1='INSERT INTO '
				c1=' (Mnumber, count) VALUES (%s,%s)'
				sql=a1+b+c1
				d=(Mnumber,m)
				mycursor.execute(sql,d)
				mydb.commit()
				SecondWindow.destroy()
		SecondWindow=Tk()
		LabelProductType=Label(SecondWindow,text='PRODUCT TYPE')
		LabelProductType.pack(side=LEFT)
		LabelProductType.place(relx=0.1,rely=0.15)
		LabelDOV=Label(SecondWindow,text='DATE OF VISIT')
		LabelDOV.pack(side=LEFT)
		LabelDOV.place(relx=0.1,rely=0.2)
		EntryProductType=Entry(SecondWindow,bd=5)
		EntryProductType.pack(side=RIGHT)
		EntryProductType.place(relx=0.7,rely=0.15)
		EntryDOV=Entry(SecondWindow,bd=5)
		EntryDOV.pack(side=RIGHT)
		EntryDOV.place(relx=0.7,rely=0.2)
		ButtonUpdate=Button(SecondWindow,text="UPDATE",command=update)
		ButtonUpdate.place(relx=0.3,rely=0.25)
		




	Mnumber=EntryNumber.get()
	print(Mnumber)
	print('got the mobile number')
	EntryNumber.delete(0,END)
	mycursor.execute("""SELECT * FROM MasterTable where Mnumber = %s""",(Mnumber,))
	
	result=mycursor.fetchall()
	if result!=[]:
		print('resullt is found already existing user')
		print(result)
		mycursor.execute('DELETE FROM MasterTable where Mnumber = %s',(Mnumber,))
		mydb.commit()
		print('Deleted the entry and updating again')
		olduser(Mnumber,result)
		
	else:
		print('no record found')
		newuser(Mnumber)
#opening Window
top=Tk()
LabelNumber=Label(top,text="ENTER THE CUSTOMER MOBILE NUMBER")
LabelNumber.pack(side = LEFT)
LabelNumber.place(relx=0.1,rely=0.4)
EntryNumber=Entry(top,bd=5)
EntryNumber.pack(side=LEFT)
EntryNumber.place(relx=0.2,rely=0.45)
ButtonCheck=Button(top,text="Profile Check",command=check)
ButtonCheck.place(relx=0.2,rely=0.5)
top.mainloop()
