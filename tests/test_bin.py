import unittest
from unittest.mock import patch, MagicMock
import sys
import os
from awslogs.bin import main

class TestBin(unittest.TestCase):
    def test_main_help(self):
        # Test with no arguments (should display help)
        with patch('sys.stderr'), patch('sys.stdout'), patch('sys.argv', ['awslogs']):
            exit_code = main()
            self.assertEqual(exit_code, 1)  # Should exit with code 1
                
    def test_groups_command(self):
        # Test groups command
        with patch('sys.argv', ['awslogs', 'groups', '--aws-region', 'us-east-1']):
            with patch('awslogs.bin.AWSLogs') as mock_awslogs:
                mock_instance = MagicMock()
                mock_awslogs.return_value = mock_instance
                
                exit_code = main()
                
                # Check AWSLogs was instantiated correctly
                mock_awslogs.assert_called_once()
                kwargs = mock_awslogs.call_args[1]
                self.assertEqual(kwargs['aws_region'], 'us-east-1')
                self.assertEqual(kwargs['func'], 'list_groups')
                
                # Check the list_groups method was called
                mock_instance.list_groups.assert_called_once()
                self.assertEqual(exit_code, 0)  # Should exit with code 0
    
    def test_streams_command(self):
        # Test streams command
        with patch('sys.argv', ['awslogs', 'streams', 'my-log-group', '--aws-region', 'us-east-1']):
            with patch('awslogs.bin.AWSLogs') as mock_awslogs:
                mock_instance = MagicMock()
                mock_awslogs.return_value = mock_instance
                
                exit_code = main()
                
                # Check AWSLogs was instantiated correctly
                mock_awslogs.assert_called_once()
                kwargs = mock_awslogs.call_args[1]
                self.assertEqual(kwargs['aws_region'], 'us-east-1')
                self.assertEqual(kwargs['log_group_name'], 'my-log-group')
                self.assertEqual(kwargs['func'], 'list_streams')
                
                # Check the list_streams method was called
                mock_instance.list_streams.assert_called_once()
                self.assertEqual(exit_code, 0)  # Should exit with code 0
    
    def test_get_command(self):
        # Test get command with ALL wildcard
        with patch('sys.argv', ['awslogs', 'get', 'my-log-group', 'ALL', '--aws-region', 'us-east-1']):
            with patch('awslogs.bin.AWSLogs') as mock_awslogs:
                mock_instance = MagicMock()
                mock_awslogs.return_value = mock_instance
                
                exit_code = main()
                
                # Check AWSLogs was instantiated correctly
                mock_awslogs.assert_called_once()
                kwargs = mock_awslogs.call_args[1]
                self.assertEqual(kwargs['aws_region'], 'us-east-1')
                self.assertEqual(kwargs['log_group_name'], 'my-log-group')
                self.assertEqual(kwargs['log_stream_name'], 'ALL')
                self.assertEqual(kwargs['func'], 'list_logs')
                
                # Check the list_logs method was called
                mock_instance.list_logs.assert_called_once()
                self.assertEqual(exit_code, 0)  # Should exit with code 0
    
    def test_get_command_with_time_filtering(self):
        # Test get command with time filtering
        with patch('sys.argv', [
            'awslogs', 'get', 'my-log-group', 'my-stream', 
            '--start', '1h', '--end', '5m',
            '--aws-region', 'us-east-1'
        ]):
            with patch('awslogs.bin.AWSLogs') as mock_awslogs:
                mock_instance = MagicMock()
                mock_awslogs.return_value = mock_instance
                
                exit_code = main()
                
                # Check AWSLogs was instantiated correctly
                mock_awslogs.assert_called_once()
                kwargs = mock_awslogs.call_args[1]
                self.assertEqual(kwargs['aws_region'], 'us-east-1')
                self.assertEqual(kwargs['log_group_name'], 'my-log-group')
                self.assertEqual(kwargs['log_stream_name'], 'my-stream')
                self.assertEqual(kwargs['start'], '1h')
                self.assertEqual(kwargs['end'], '5m')
                self.assertEqual(kwargs['func'], 'list_logs')
                
                # Check the list_logs method was called
                mock_instance.list_logs.assert_called_once()
                self.assertEqual(exit_code, 0)  # Should exit with code 0
    
    def test_environment_variables(self):
        # Test environment variables are used
        original_env = os.environ.copy()
        try:
            os.environ['AWS_REGION'] = 'eu-west-1'
            os.environ['AWS_PROFILE'] = 'test-profile'
            
            with patch('sys.argv', ['awslogs', 'groups']):
                with patch('awslogs.bin.AWSLogs') as mock_awslogs:
                    mock_instance = MagicMock()
                    mock_awslogs.return_value = mock_instance
                    
                    exit_code = main()
                    
                    # Check AWSLogs was instantiated with env var values
                    mock_awslogs.assert_called_once()
                    kwargs = mock_awslogs.call_args[1]
                    self.assertEqual(kwargs['aws_region'], 'eu-west-1')
                    self.assertEqual(kwargs['aws_profile'], 'test-profile')
                    
                    # Check the list_groups method was called
                    mock_instance.list_groups.assert_called_once()
                    self.assertEqual(exit_code, 0)  # Should exit with code 0
        finally:
            # Restore environment
            os.environ.clear()
            os.environ.update(original_env)

if __name__ == '__main__':
    unittest.main() 