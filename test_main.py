import unittest
import tempfile
import os
import json
from unittest.mock import patch, MagicMock
from main import check_required_files, create_subtitle_file, format_srt_time

class TestMediaMerger(unittest.TestCase):
    
    def test_format_srt_time(self):
        """Test SRT time formatting"""
        self.assertEqual(format_srt_time(0), "00:00:00,000")
        self.assertEqual(format_srt_time(65), "00:01:05,000")
        self.assertEqual(format_srt_time(3661.5), "01:01:01,500")
    
    def test_create_subtitle_file(self):
        """Test subtitle file creation"""
        with tempfile.TemporaryDirectory() as temp_dir:
            subtitle_path = os.path.join(temp_dir, "test_subtitle.srt")
            description = "This is a test description for the video content."
            
            create_subtitle_file(subtitle_path, description)
            
            # Check if file was created
            self.assertTrue(os.path.exists(subtitle_path))
            
            # Check file content
            with open(subtitle_path, 'r', encoding='utf-8') as f:
                content = f.read()
                self.assertIn("This is a test description", content)
                self.assertIn("00:00:00,000", content)
    
    @patch('main.storage_client')
    def test_check_required_files_all_present(self, mock_storage_client):
        """Test checking for required files when all are present"""
        # Mock bucket and blobs
        mock_bucket = MagicMock()
        mock_storage_client.bucket.return_value = mock_bucket
        
        # Create mock blobs
        mock_blobs = [
            MagicMock(name="projectX_video.mp4"),
            MagicMock(name="projectX_audio.mp3"),
            MagicMock(name="projectX_description.json")
        ]
        mock_bucket.list_blobs.return_value = mock_blobs
        
        result = check_required_files("test-bucket", "projectX")
        
        self.assertTrue(result['all_present'])
        self.assertEqual(len(result['missing']), 0)
        self.assertIsNotNone(result['files']['video'])
        self.assertIsNotNone(result['files']['audio'])
        self.assertIsNotNone(result['files']['description'])
    
    @patch('main.storage_client')
    def test_check_required_files_missing(self, mock_storage_client):
        """Test checking for required files when some are missing"""
        # Mock bucket and blobs
        mock_bucket = MagicMock()
        mock_storage_client.bucket.return_value = mock_bucket
        
        # Create mock blobs (missing audio file)
        mock_blobs = [
            MagicMock(name="projectX_video.mp4"),
            MagicMock(name="projectX_description.json")
        ]
        mock_bucket.list_blobs.return_value = mock_blobs
        
        result = check_required_files("test-bucket", "projectX")
        
        self.assertFalse(result['all_present'])
        self.assertIn('audio', result['missing'])
        self.assertIsNotNone(result['files']['video'])
        self.assertIsNone(result['files']['audio'])
        self.assertIsNotNone(result['files']['description'])

if __name__ == '__main__':
    unittest.main()
