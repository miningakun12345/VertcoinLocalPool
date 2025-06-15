# P2Pool Vertcoin

A complete P2Pool implementation for Vertcoin cryptocurrency mining with local node functionality.

## Features

- **Local P2Pool Node**: Complete P2Pool protocol implementation for Vertcoin
- **Blockchain Integration**: Direct connection to Vertcoin Core via JSON-RPC
- **Share Chain Management**: Efficient share validation and chain management
- **Network Discovery**: Peer-to-peer network with automatic peer discovery
- **Web Interface**: Real-time monitoring dashboard with WebSocket updates
- **Database Storage**: SQLite-based persistence for shares, blocks, and statistics
- **Mining Support**: Work generation and share submission for miners

## Prerequisites

### Required Software

1. **Vertcoin Core**: Download and install Vertcoin Core from [vertcoin.org](https://vertcoin.org)
2. **Python 3.8+**: Required for running the P2Pool node

### System Requirements

- **Memory**: Minimum 2GB RAM (4GB recommended)
- **Storage**: At least 10GB free space for blockchain and P2Pool data
- **Network**: Stable internet connection with opened ports
- **CPU**: Any modern CPU (mining performance depends on connected miners)

## Installation

### 1. Install Vertcoin Core

Download and install Vertcoin Core, then configure it with the following settings in `vertcoin.conf`:

```ini
# RPC Settings
rpcuser=vertcoinrpc
rpcpassword=your_secure_password_here
rpcallowip=127.0.0.1
rpcport=5888

# Network Settings
port=5889
listen=1

# Mining Settings (optional)
server=1
