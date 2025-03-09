from flask import Flask, request, jsonify
import boto3
import os

app = Flask(__name__)

# AWS S3 Bilgileri
S3_BUCKET = "eqpredictionworkgroup"
AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")

s3_client = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY
)

@app.route('/upload', methods=['PUT'])
def upload_csv():
    if 'file' not in request.files:
        return jsonify({"error": "Dosya gönderilmedi"}), 400

    file = request.files['file']
    file_name = file.filename

    # Dosyayı geçici olarak kaydet
    temp_path = f"/tmp/{file_name}"
    file.save(temp_path)

    s3_key = f"eqprediction2025/{file_name}" 

    # S3'e yükle
    s3_client.upload_file(temp_path, S3_BUCKET, s3_key)

    # Geçici dosyayı sil
    os.remove(temp_path)

    return jsonify({"message": "Dosya başarıyla yüklendi", "s3_path": f"s3://{S3_BUCKET}/{s3_key}"}), 200

@app.route('/health', methods=['GET'])
def health_check():
    print("AWS_ACCESS_KEY_ID:", os.getenv("AWS_ACCESS_KEY_ID"))
    print("AWS_SECRET_ACCESS_KEY:", os.getenv("AWS_SECRET_ACCESS_KEY"))
    return jsonify({"status": "ok"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)