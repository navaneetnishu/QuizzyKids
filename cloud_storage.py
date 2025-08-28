#!/usr/bin/env python3
"""
Cloud storage integration for cost-effective PDF storage
Using Backblaze B2: $0.005/GB/month (much cheaper than AWS S3)
"""

import os
import b2sdk
from b2sdk.v2 import *
import tempfile
import hashlib
from datetime import datetime, timedelta
import logging

class CostEffectiveStorage:
    def __init__(self):
        self.application_key_id = os.getenv('B2_APPLICATION_KEY_ID')
        self.application_key = os.getenv('B2_APPLICATION_KEY')
        self.bucket_name = os.getenv('B2_BUCKET_NAME', 'kids-practice-pdfs')
        
        self.info = InMemoryAccountInfo()
        self.b2_api = B2Api(self.info)
        
        # Initialize connection
        try:
            self.b2_api.authorize_account("production", self.application_key_id, self.application_key)
            self.bucket = self.b2_api.get_bucket_by_name(self.bucket_name)
            self.storage_available = True
            logging.info("✅ Backblaze B2 storage initialized successfully")
        except Exception as e:
            self.storage_available = False
            logging.warning(f"⚠️ Backblaze B2 not available: {e}")
    
    def upload_pdf(self, file_path, user_id, subject, topic):
        """Upload PDF to Backblaze B2 with cost-effective organization"""
        if not self.storage_available:
            return None
        
        try:
            # Generate cost-effective file path
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            file_hash = self._get_file_hash(file_path)
            
            # Organize by date for cost optimization
            date_folder = datetime.now().strftime("%Y/%m")
            filename = f"{date_folder}/{subject}/{topic}/{user_id}_{timestamp}_{file_hash[:8]}.pdf"
            
            # Upload file
            with open(file_path, 'rb') as file:
                self.b2_api.upload_file(
                    bucket_id=self.bucket.id_,
                    file_name=filename,
                    data=file,
                    content_type='application/pdf'
                )
            
            # Generate download URL (free downloads)
            download_url = self.b2_api.get_download_url_for_file_name(
                bucket_name=self.bucket_name,
                file_name=filename
            )
            
            logging.info(f"✅ PDF uploaded: {filename}")
            return download_url
            
        except Exception as e:
            logging.error(f"❌ Failed to upload PDF: {e}")
            return None
    
    def _get_file_hash(self, file_path):
        """Generate file hash for deduplication"""
        hash_md5 = hashlib.md5()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    
    def cleanup_old_files(self, days=30):
        """Clean up old files to save storage costs"""
        if not self.storage_available:
            return
        
        try:
            cutoff_date = datetime.now() - timedelta(days=days)
            
            # List files older than cutoff date
            for file_info in self.b2_api.list_file_names(self.bucket.id_):
                file_date = datetime.fromtimestamp(file_info.upload_timestamp / 1000)
                
                if file_date < cutoff_date:
                    # Delete old file
                    self.b2_api.delete_file_version(
                        file_info.id_,
                        file_info.file_name
                    )
                    logging.info(f"🗑️ Deleted old file: {file_info.file_name}")
                    
        except Exception as e:
            logging.error(f"❌ Failed to cleanup old files: {e}")
    
    def get_storage_stats(self):
        """Get storage statistics for cost monitoring"""
        if not self.storage_available:
            return None
        
        try:
            total_size = 0
            file_count = 0
            
            for file_info in self.b2_api.list_file_names(self.bucket.id_):
                total_size += file_info.content_length
                file_count += 1
            
            # Calculate monthly cost (Backblaze B2 pricing)
            monthly_cost = (total_size / (1024**3)) * 0.005  # $0.005 per GB
            
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
storage = CostEffectiveStorage()

def upload_pdf_to_cloud(file_path, user_id, subject, topic):
    """Convenience function to upload PDF"""
    return storage.upload_pdf(file_path, user_id, subject, topic)

def get_storage_statistics():
    """Get storage statistics"""
    return storage.get_storage_stats()

def cleanup_old_pdfs(days=30):
    """Clean up old PDFs"""
    storage.cleanup_old_files(days)
