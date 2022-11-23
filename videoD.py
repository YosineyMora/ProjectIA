import cv2
import os




# Path of the folder where the dataset will be stored
dataResult = 'Results'
# dataPath = 'C:\\Users\\yosin\\Desktop\\ReconocimientoFacial\\MaterialReconocimientoFacial\\Data'
imagePaths = ["AlejandraJimenez", "Alison", "AliSuarez",
              "Brian", "Elison", "Emilio", "Harold", "Jean", "Yosiney"]



def get_frame(self):
    face_recognizer = cv2.face.LBPHFaceRecognizer_create()
    face_recognizer.read('models\modeloLBPHFace.xml')
    faceClassif = cv2.CascadeClassifier(
    cv2.data.haarcascades+'haarcascade_frontalface_default.xml')
    print(self)
    cap = cv2.VideoCapture(self)
    count = 0
    while True:
        ret, frame = cap.read()
        if ret == False:break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        auxFrame = gray.copy()
        faces = faceClassif.detectMultiScale(gray, 1.3, 5)

        if (len(faces) > 1):
            dataRe = dataResult+"\\Grupal\\"
        else:
            dataRe = dataResult+"\\Individual\\"

        for (x, y, w, h) in faces:

            rostro = auxFrame[y:y+h, x:x+w]
            rostro = cv2.resize(rostro, (150, 150),
                                interpolation=cv2.INTER_CUBIC)
            result = face_recognizer.predict(rostro)

            cv2.putText(frame, '{}'.format(result), (x, y-5),
                        1, 1.3, (255, 255, 0), 1, cv2.LINE_AA)

        # LBPHFace
            dataR = dataRe + '/' + '{}'.format(imagePaths[result[0]])
            personPath = dataR + '/' + '{}'.format(imagePaths[result[0]])
            personDPath = dataR + '/Desconocido'

            if not os.path.exists(dataR):
                print('Carpeta creada: ', dataR)
                os.makedirs(dataR)

            if not os.path.exists(personPath):
                print('Carpeta creada: ', personPath)
                os.makedirs(personPath)

            if not os.path.exists(personDPath):
                print('Carpeta creada: ', personDPath)
                os.makedirs(personDPath)
            count = count + 1
            if result[1] < 71:
                # If the folder does not exist, it is created
                cv2.putText(frame, '{}'.format(
                    imagePaths[result[0]]), (x, y-25), 2, 1.1, (0, 255, 0), 1, cv2.LINE_AA)
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                cv2.imwrite(
                    personPath+"/"+'{}'.format(imagePaths[result[0]])+'_rotro_{}'.format(count)+'.png', frame)
            else:
                cv2.putText(frame, 'Desconocido', (x, y-20), 2,
                            0.8, (0, 0, 255), 1, cv2.LINE_AA)
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)
                cv2.imwrite(personDPath+'/Desconocido' +
                            'rotro_{}'.format(count)+'.png', frame)

            
