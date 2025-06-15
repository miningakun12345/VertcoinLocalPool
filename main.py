#!/usr/bin/env python3
"""
P2Pool Vertcoin Implementation
Main entry point for the P2Pool node
"""

import sys
import logging
import argparse
from twisted.internet import reactor
from twisted.python import log
from p2pool.node import P2PoolNode
from web.server import WebServer
from config import Config

def setup_logging(debug=False):
    """Setup logging configuration"""
    level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('p2pool.log'),
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    # Bridge Twisted logs to Python logging
    observer = log.PythonLoggingObserver()
    observer.start()

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description='P2Pool Vertcoin Node')
    parser.add_argument('--config', default='config.json', help='Configuration file path')
    parser.add_argument('--debug', action='store_true', help='Enable debug logging')
    parser.add_argument('--web-port', type=int, default=5000, help='Web interface port')
    parser.add_argument('--p2p-port', type=int, default=9346, help='P2P network port')
    
    args = parser.parse_args()
    
    setup_logging(args.debug)
    logger = logging.getLogger(__name__)
    
    try:
        # Load configuration
        config = Config(args.config)
        config.web_port = args.web_port
        config.p2p_port = args.p2p_port
        
        logger.info("Starting P2Pool Vertcoin Node")
        logger.info(f"Web interface will be available at http://localhost:{config.web_port}")
        logger.info(f"P2P network listening on port {config.p2p_port}")
        
        # Create and start P2Pool node
        p2pool_node = P2PoolNode(config)
        
        # Create and start web server
        web_server = WebServer(config, p2pool_node)
        
        # Start the node
        p2pool_node.start()
        web_server.start()
        
        logger.info("P2Pool node started successfully")
        logger.info("Press Ctrl+C to stop")
        
        # Run the reactor
        reactor.run()
        
    except KeyboardInterrupt:
        logger.info("Shutting down P2Pool node...")
    except Exception as e:
        logger.error(f"Failed to start P2Pool node: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
