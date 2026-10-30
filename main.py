import boto3
from botocore.config import Config

# កំណត់ព័ត៌មានសម្ងាត់ដែលទទួលបានពី Cloudflare R2
ACCESS_KEY_ID = "4b53b9d48ac396214d95fea2e44e22de"
SECRET_ACCESS_KEY = "b91dee244ef9cdd3f26bda734c3dda8696370828a0495c87103961f2f5ef620f"
ENDPOINT_URL = "https://76131f15fc5b7b2ede75a5b0edd8fa5f.r2.cloudflarestorage.com"
BUCKET_NAME = "my-videos"

# ភ្ជាប់ទៅកាន់ R2 តាមរយៈ S3 API (ប្រើប្រាស់ Signature Version 4)
session = boto3.session.Session()
client = session.client(
    's3',
    endpoint_url=ENDPOINT_URL,
    aws_access_key_id=ACCESS_KEY_ID,
    aws_secret_access_key=SECRET_ACCESS_KEY,
    config=Config(signature_version='s3v4'),
    region_name='auto'  # Cloudflare R2 ប្រើតំបន់ auto
)

# ផ្លូវទៅកាន់ហ្វាលវីដេអូរបស់អ្នក (ឧទាហរណ៍: movie.mp4)
file_path = "movie.mp4"
object_name = "movie.mp4"

print("กำลัง Upload វីដេអូរបស់អ្នកចូលទៅកាន់ Cloudflare R2 (អាចចំណាយពេលបន្តិចតាមទំហំហ្វាល)...")

try:
    # ប្រើប្រាស់ប្រព័ន្ធ Upload បែប Multipart ដោយស្វ័យប្រវត្តសម្រាប់ហ្វាលធំ
    client.upload_file(file_path, BUCKET_NAME, object_name)
    print("✅ Upload វីដេអូបានដោយជោគជ័យ!")
    
    # បង្ហាញ Direct Link សម្រាប់យកទៅប្រើប្រាស់
    public_url = f"{ENDPOINT_URL}/{BUCKET_NAME}/{object_name}"
    print(f"🔗 Direct Link របស់អ្នកគឺ: {public_url}")

except Exception as e:
    print(f"❌ មានបញ្ហាในการ Upload: {e}")
