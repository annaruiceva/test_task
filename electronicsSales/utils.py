import datetime

import qrcode


def create_qr_code(value):
    new_img = qrcode.make(value)
    filename = 'media/qr-code/QR-code' + str(datetime.datetime.now().strftime('%d-%m-%Y--%H-%M')) + '.png'
    try:
        new_img.save(filename)
    except:
        return ''
    return filename
