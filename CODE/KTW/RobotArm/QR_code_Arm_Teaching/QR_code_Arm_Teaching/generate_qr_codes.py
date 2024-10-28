import qrcode
import os

# QR 코드 데이터를 정의
qr_data_list = [
    "1-1",
    "2-1",
    "3-1",
    "4-1",
    "1-2",
    "2-2",
    "3-2",
    "4-2",
    "1-3",
    "2-3",
    "3-3",
    "4-3",
    "1-4",
    "2-4",
    "3-4",
    "4-4",
]

def generate_qr_codes(output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    for idx, data in enumerate(qr_data_list, start=1):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        img_path = os.path.join(output_dir, f"qr_code_{idx}.png")
        img.save(img_path)
        print(f"QR 코드 생성됨: {img_path}")

if __name__ == "__main__":
    output_directory = "image_path"  # QR 코드 이미지를 저장할 디렉토리
    generate_qr_codes(output_directory)