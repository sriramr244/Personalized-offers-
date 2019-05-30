The personalized offers is  starting to be trend in this buzzing world. The retail players are seeking for customer loyalty and trying to retain it. This project mainly focusses on preserving the customer loyalty and giving away the offers privately to the customers who are deserving it. The powerpoint included talks about the scalablity and the implementation of the project. This project is implemented mainly with two technologies 1. IOT 2.Facial recognition. It contains two modules one module for the console at the billing which is used to record the customer details and their recent purchase, the count of how many times they have a purchased in the retail. Second module is for the console at certain checkpoints of the shop which recognizes the person and pulls their record from the database in the cloud. IOT is used to standardize the record and make it accessible from any part of the world.
	In this project the flow is the person comes buying a type of product if he is new a record is created for the user or else the record is updated if he is a old user. Once he/she is new user the camera takes up a single photo and stores in a folder/a local host and can be accessed from any part of the world. Once he/she is spotted in any of tyhe checkpoints in the retail market and if he is a frequent customer his mobile picks up a text message about the offer he/sheis eligible off. I have a used a free online database and a free texting web platform which gives us limited access. While scaling it a better database can be used.
 












How to run the file 

1. Install all the packages in the requirements text
2. run console_at_billing.py and enter the details in the db if you are using the mobile number (give a valid mobile number for checing the messaging service) for the first time at last an image of yours is taken and stored in the Dataset folder
										(I have given only 3 ProductTypes: 1.grocery 2.electronics 3.food (in producttype text box in the UI type as such i have mentioned previously))
3. Now that your Profile has been created open the Checkpoint_offer.py the camera opens if you have already purchased a same product type above 3 times an offer pops to your mobile phone number mentioned at the billing
4. Use a laptop with an webcam in it 
5. I have used a a system with ubuntu OS
6.download the model from the link http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2 for the detection
