"""
Cloud storage utilities for uploading receipts and files
Supports Firebase Storage, AWS S3, and local storage
"""
import os
from datetime import datetime

def upload_receipt(file, user_id):
    """
    Upload receipt file to cloud storage
    Supports Firebase Storage, AWS S3, or local storage
    
    Args:
        file: File object from request
        user_id: User ID for organizing storage
    
    Returns:
        URL of uploaded file
    """
    storage_type = os.getenv('STORAGE_TYPE', 'local')
    
    if storage_type == 'firebase':
        return upload_to_firebase(file, user_id)
    elif storage_type == 's3':
        return upload_to_s3(file, user_id)
    else:
        return upload_to_local(file, user_id)

def upload_to_firebase(file, user_id):
    """Upload to Firebase Storage"""
    try:
        import firebase_admin
        from firebase_admin import storage
        
        bucket = storage.bucket()
        filename = f"receipts/{user_id}/{datetime.utcnow().timestamp()}_{file.filename}"
        blob = bucket.blob(filename)
        
        blob.upload_from_string(
            file.read(),
            content_type=file.content_type
        )
        
        return f"gs://{bucket.name}/{filename}"
    except Exception as e:
        print(f"Error uploading to Firebase: {e}")
        return None

def upload_to_s3(file, user_id):
    """Upload to AWS S3"""
    try:
        import boto3
        
        s3 = boto3.client(
            's3',
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
            region_name=os.getenv('AWS_REGION', 'us-east-1')
        )
        
        bucket_name = os.getenv('AWS_S3_BUCKET')
        key = f"receipts/{user_id}/{datetime.utcnow().timestamp()}_{file.filename}"
        
        s3.upload_fileobj(
            file,
            bucket_name,
            key,
            ExtraArgs={'ContentType': file.content_type}
        )
        
        return f"https://{bucket_name}.s3.amazonaws.com/{key}"
    except Exception as e:
        print(f"Error uploading to S3: {e}")
        return None

def upload_to_local(file, user_id):
    """Upload to local storage"""
    try:
        upload_dir = f"app/static/uploads/receipts/{user_id}"
        os.makedirs(upload_dir, exist_ok=True)
        
        filename = f"{datetime.utcnow().timestamp()}_{file.filename}"
        filepath = os.path.join(upload_dir, filename)
        
        file.save(filepath)
        
        return f"/static/uploads/receipts/{user_id}/{filename}"
    except Exception as e:
        print(f"Error uploading to local storage: {e}")
        return None
