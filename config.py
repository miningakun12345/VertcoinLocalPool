"""
Configuration management for P2Pool Vertcoin
"""

import json
import os
import logging

class Config:
    """Configuration manager"""
    
    def __init__(self, config_file='config.json'):
        self.config_file = config_file
        self.logger = logging.getLogger(__name__)
        
        # Default configuration
        self.defaults = {
            'vertcoin_rpc': {
                'host': '127.0.0.1',
                'port': 5888,
                'username': 'vertcoinrpc',
                'password': 'changeme'
            },
            'p2pool': {
                'network': 'mainnet',
                'donation_percentage': 0.5,
                'fee_percentage': 0.0,
                'block_max_size': 1000000,
                'min_difficulty': 1.0
            },
            'network': {
                'p2p_port': 9346,
                'max_peers': 10,
                'target_peers': 5
            },
            'web': {
                'port': 5000,
                'host': '0.0.0.0'
            },
            'mining': {
                'payout_address': '',
                'worker_name': 'default'
            },
            'database': {
                'path': 'p2pool.db'
            }
        }
        
        self.load_config()
    
    def load_config(self):
        """Load configuration from file"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    user_config = json.load(f)
                self._merge_config(self.defaults, user_config)
                self.logger.info(f"Configuration loaded from {self.config_file}")
            except Exception as e:
                self.logger.warning(f"Failed to load config file: {e}, using defaults")
        else:
            self.logger.info("No config file found, using defaults")
            self.save_config()
    
    def save_config(self):
        """Save current configuration to file"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.defaults, f, indent=2)
            self.logger.info(f"Configuration saved to {self.config_file}")
        except Exception as e:
            self.logger.error(f"Failed to save config: {e}")
    
    def _merge_config(self, default, user):
        """Recursively merge user config with defaults"""
        for key, value in user.items():
            if key in default:
                if isinstance(value, dict) and isinstance(default[key], dict):
                    self._merge_config(default[key], value)
                else:
                    default[key] = value
    
    def get(self, path, default=None):
        """Get configuration value by dot notation path"""
        keys = path.split('.')
        value = self.defaults
        
        try:
            for key in keys:
                value = value[key]
            return value
        except (KeyError, TypeError):
            return default
    
    def set(self, path, value):
        """Set configuration value by dot notation path"""
        keys = path.split('.')
        config = self.defaults
        
        for key in keys[:-1]:
            if key not in config:
                config[key] = {}
            config = config[key]
        
        config[keys[-1]] = value
    
    @property
    def vertcoin_rpc_url(self):
        """Get Vertcoin RPC URL"""
        rpc = self.defaults['vertcoin_rpc']
        return f"http://{rpc['username']}:{rpc['password']}@{rpc['host']}:{rpc['port']}"
    
    @property
    def web_port(self):
        """Get web server port"""
        return self.defaults['web']['port']
    
    @web_port.setter
    def web_port(self, value):
        """Set web server port"""
        self.defaults['web']['port'] = value
    
    @property
    def p2p_port(self):
        """Get P2P network port"""
        return self.defaults['network']['p2p_port']
    
    @p2p_port.setter
    def p2p_port(self, value):
        """Set P2P network port"""
        self.defaults['network']['p2p_port'] = value
