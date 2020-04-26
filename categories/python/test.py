import binascii
with open('fileContainer.php', 'r') as file:
    data = file.read()
data=data.strip()
data=data.replace(' ', '')
data=data.replace('\n', '')
data = binascii.a2b_hex(data)
with open('python/finger.jpg', 'wb') as image_file:
    image_file.write(data)