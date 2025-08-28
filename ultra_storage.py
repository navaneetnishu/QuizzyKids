#!/usr/bin/env python3
"""
Ultra-cost-effective storage solution for £20/month budget
Using Cloudflare R2: £0.015/GB/month (cheaper than Backblaze B2)
"""

import os
import boto3
import tempfile
import hashlib
from datetime import datetime, timedelta
import logging
import gzip
import json

class UltraStorage:
    def __init__(self):
        self.access_key_id = os.getenv('R2_ACCESS_KEY_ID')
        self.secret_access_key = os.getenv('R2_SECRET_ACCESS_KEY')
        self.bucket_name = os.getenv('R2_BUCKET_NAME', 'kids-practice-pdfs')
        self.account_id = os.getenv('R2_ACCOUNT_ID')
        
        # Initialize S3-compatible client for Cloudflare R2
        try:
            self.s3_client = boto3.client(
                's3',
                endpoint_url=f'https://{self.account_id}.r2.cloudflarestorage.com',
                aws_access_key_id=self.access_key_id,
                aws_secret_access_key=self.secret_access_key,
                region_name='auto'
            )
            self.storage_available = True
            logging.info("✅ Cloudflare R2 storage initialized successfully")
        except Exception as e:
            self.storage_available = False
            logging.warning(f"⚠️ Cloudflare R2 not available: {e}")
        
        # Local cache for frequently accessed files
        self.local_cache_dir = '/tmp/pdf_cache'
        os.makedirs(self.local_cache_dir, exist_ok=True)
    
    def upload_pdf(self, file_path, user_id, subject, topic):
        """Upload PDF with ultra-cost-effective organization"""
        if not self.storage_available:
            return self._local_fallback(file_path, user_id)
        
        try:
            # Generate cost-effective file path
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            file_hash = self._get_file_hash(file_path)
            
            # Organize by month for cost optimization
            month_folder = datetime.now().strftime("%Y/%m")
            filename = f"{month_folder}/{subject}/{topic}/{user_id}_{timestamp}_{file_hash[:8]}.pdf"
            
            # Compress PDF before upload to save bandwidth
            compressed_path = self._compress_pdf(file_path)
            
            # Upload to Cloudflare R2
            with open(compressed_path, 'rb') as file:
                self.s3_client.upload_fileobj(
                    file,
                    self.bucket_name,
                    filename,
                    ExtraArgs={
                        'ContentType': 'application/pdf',
                        'ContentEncoding': 'gzip',
                        'CacheControl': 'max-age=3600'  # 1 hour cache
                    }
                )
            
            # Generate public URL
            download_url = f"https://{self.bucket_name}.r2.cloudflarestorage.com/{filename}"
            
            # Clean up compressed file
            os.remove(compressed_path)
            
            logging.info(f"✅ PDF uploaded to R2: {filename}")
            return download_url
            
        except Exception as e:
            logging.error(f"❌ Failed to upload PDF: {e}")
            return self._local_fallback(file_path, user_id)
    
    def _compress_pdf(self, file_path):
        """Compress PDF to save bandwidth and storage"""
        compressed_path = file_path + '.gz'
        
        with open(file_path, 'rb') as f_in:
            with gzip.open(compressed_path, 'wb') as f_out:
                f_out.writelines(f_in)
        
        return compressed_path
    
    def _local_fallback(self, file_path, user_id):
        """Local fallback when cloud storage is unavailable"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{user_id}_{timestamp}.pdf"
        local_path = os.path.join(self.local_cache_dir, filename)
        
        # Copy file to local cache
        import shutil
        shutil.copy2(file_path, local_path)
        
        return f"/download/local/{filename}"
    
    def _get_file_hash(self, file_path):
        """Generate file hash for deduplication"""
        hash_md5 = hashlib.md5()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    
    def cleanup_old_files(self, days=7):
        """Aggressive cleanup to save storage costs"""
        if not self.storage_available:
            return
        
        try:
            cutoff_date = datetime.now() - timedelta(days=days)
            
            # List objects older than cutoff date
            paginator = self.s3_client.get_paginator('list_objects_v2')
            pages = paginator.paginate(Bucket=self.bucket_name)
            
            for page in pages:
                if 'Contents' in page:
                    for obj in page['Contents']:
                        if obj['LastModified'].replace(tzinfo=None) < cutoff_date:
                            # Delete old file
                            self.s3_client.delete_object(
                                Bucket=self.bucket_name,
                                Key=obj['Key']
                            )
                            logging.info(f"🗑️ Deleted old file: {obj['Key']}")
                            
        except Exception as e:
            logging.error(f"❌ Failed to cleanup old files: {e}")
    
    def get_storage_stats(self):
        """Get storage statistics for cost monitoring"""
        if not self.storage_available:
            return {'storage_available': False}
        
        try:
            total_size = 0
            file_count = 0
            
            paginator = self.s3_client.get_paginator('list_objects_v2')
            pages = paginator.paginate(Bucket=self.bucket_name)
            
            for page in pages:
                if 'Contents' in page:
                    for obj in page['Contents']:
                        total_size += obj['Size']
                        file_count += 1
            
            # Calculate monthly cost (Cloudflare R2 pricing)
            monthly_cost = (total_size / (1024**3)) * 0.015  # £0.015 per GB
            
            return {
                'total_files': file_count,
                'total_size_gb': round(total_size / (1024**3), 2),
                'estimated_monthly_cost': round(monthly_cost, 2),
                'storage_available': True
            }
            
        except Exception as e:
            logging.error(f"❌ Failed to get storage stats: {e}")
            return {'storage_available': False}

# Global storage instance
ultra_storage = UltraStorage()

def upload_pdf_to_ultra_storage(file_path, user_id, subject, topic):
    """Convenience function to upload PDF"""
    return ultra_storage.upload_pdf(file_path, user_id, subject, topic)

def get_ultra_storage_statistics():
    """Get storage statistics"""
    return ultra_storage.get_storage_stats()

def cleanup_old_pdfs_ultra(days=7):
    """Aggressive cleanup of old PDFs"""
    ultra_storage.cleanup_old_files(days)
