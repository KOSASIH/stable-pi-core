# orbital-data-marketplace (ODM)

## Description
The **Orbital Data Marketplace (ODM)** is an advanced platform designed to facilitate the buying and selling of space-based data. This marketplace allows satellites, space stations, and terrestrial users to trade various types of space data, such as star images, climate data, and telemetry, using the Stable-Pi-Core token. 

The ODM leverages a **Space-Based Node Network** and smart contracts to ensure secure and efficient transactions, while utilizing **Probabilistic Quantum Polynomial Networks (PQPN)** for rapid data analysis.

## Features
- **Decentralized Marketplace**: A secure platform for trading space data using blockchain technology.
- **Smart Contracts**: Automated contracts that facilitate transactions between buyers and sellers without intermediaries.
- **Space-Based Node Network**: A network of nodes that collect, process, and distribute space data.
- **Rapid Data Analysis**: Utilizes PQPN for quick and efficient data analysis, enabling users to make informed decisions.
- **User -Friendly Interface**: An intuitive web interface for users to browse, buy, and sell data listings.

## Architecture
The ODM is built using the following components:
- **Backend**: Python with Flask for the API and business logic.
- **Smart Contracts**: Written in Solidity for deployment on Ethereum or compatible blockchains.
- **Database**: SQLite for local development and testing, with options for other databases in production.
- **Frontend**: HTML/CSS/JavaScript for the user interface, utilizing Flask templates.

## Installation

### Prerequisites
- Python 3.7 or higher
- Node.js and npm (for smart contract development)
- Ganache or another Ethereum test network (for testing smart contracts)
- A web browser

### Clone the Repository
```bash
git clone https://github.com/KOSASIH/stable-pi-core.git
cd stable-pi-core/odm
```

### Set Up the Backend
1. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up the database**:
   ```bash
   python -c "from odm import db; db.create_all()"
   ```

### Set Up the Smart Contracts
1. **Navigate to the contracts directory**:
   ```bash
   cd odm/contracts
   ```

2. **Install Truffle** (if not already installed):
   ```bash
   npm install -g truffle
   ```

3. **Compile and migrate the smart contracts**:
   ```bash
   truffle compile
   truffle migrate --network development
   ```

### Run the Application
1. **Start the Flask server**:
   ```bash
   python -m odm.user_interface.app
   ```

2. **Open your web browser** and navigate to `http://localhost:5000`.

## Usage
- **Register**: Create an account to start buying and selling data.
- **Browse Listings**: View available data listings in the marketplace.
- **Submit Data**: List your own data for sale by providing the necessary details.
- **Purchase Data**: Buy data using the Stable-Pi-Core token.

## Testing
To run the unit tests for the ODM components, use the following command:
```bash
python -m unittest discover -s tests
```

## Contributing
Contributions are welcome! Please follow these steps:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature/YourFeature`).
3. Make your changes and commit them (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature/YourFeature`).
5. Open a pull request.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments
- Special thanks to the contributors and the open-source community for their support and resources.
- Inspired by the potential of space exploration and data utilization.

## Contact
For inquiries, please contact [KOSASIH](https://github.com/KOSASIH).
