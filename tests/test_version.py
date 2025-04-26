import unittest
from unittest.mock import patch
import importlib
from awslogs._version import __version__

class TestVersion(unittest.TestCase):
    def test_version_is_string(self):
        self.assertIsInstance(__version__, str)
        
    def test_version_is_not_empty(self):
        self.assertTrue(__version__)
    
    @patch('importlib.metadata.version')
    def test_version_from_metadata(self, mock_version):
        """Test version detection using importlib.metadata"""
        # Mock the metadata version call
        mock_version.return_value = "1.2.3"
        
        # Reload the _version module
        import awslogs._version
        importlib.reload(awslogs._version)
        
        # Check the version was set correctly
        self.assertEqual(awslogs._version.__version__, "1.2.3")
        mock_version.assert_called_once_with("awslogs")
    
    @patch('importlib.metadata.version', side_effect=ImportError)
    @patch('pkg_resources.get_distribution')
    def test_version_fallback(self, mock_get_distribution, mock_version):
        """Test version fallback using pkg_resources"""
        # Mock the pkg_resources distribution
        mock_dist = unittest.mock.MagicMock()
        mock_dist.version = "4.5.6"
        mock_get_distribution.return_value = mock_dist
        
        # Reload the _version module
        import awslogs._version
        importlib.reload(awslogs._version)
        
        # Check the version was set correctly
        self.assertEqual(awslogs._version.__version__, "4.5.6")
        mock_version.assert_called_once()
        mock_get_distribution.assert_called_once_with("awslogs")
        
if __name__ == '__main__':
    unittest.main() import unittest
from unittest.mock import patch
import importlib
from awslogs._version import __version__

class TestVersion(unittest.TestCase):
    def test_version_is_string(self):
        self.assertIsInstance(__version__, str)
        
    def test_version_is_not_empty(self):
        self.assertTrue(__version__)
    
    @patch('importlib.metadata.version')
    def test_version_from_metadata(self, mock_version):
        """Test version detection using importlib.metadata"""
        # Mock the metadata version call
        mock_version.return_value = "1.2.3"
        
        # Reload the _version module
        import awslogs._version
        importlib.reload(awslogs._version)
        
        # Check the version was set correctly
        self.assertEqual(awslogs._version.__version__, "1.2.3")
        mock_version.assert_called_once_with("awslogs")
    
    @patch('importlib.metadata.version', side_effect=ImportError)
    @patch('pkg_resources.get_distribution')
    def test_version_fallback(self, mock_get_distribution, mock_version):
        """Test version fallback using pkg_resources"""
        # Mock the pkg_resources distribution
        mock_dist = unittest.mock.MagicMock()
        mock_dist.version = "4.5.6"
        mock_get_distribution.return_value = mock_dist
        
        # Reload the _version module
        import awslogs._version
        importlib.reload(awslogs._version)
        
        # Check the version was set correctly
        self.assertEqual(awslogs._version.__version__, "4.5.6")
        mock_version.assert_called_once()
        mock_get_distribution.assert_called_once_with("awslogs")
        
if __name__ == '__main__':
    unittest.main() 