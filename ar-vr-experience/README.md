# AR/VR Experience

## Overview

The **AR/VR Experience** project is designed to create an immersive augmented reality (AR) and virtual reality (VR) application that integrates market data. This project utilizes Unity for the AR/VR components and A-Frame for web-based experiences, along with a Node.js backend for data management.

## Features

- Fetch and display market data in AR/VR environments.
- Interactive AR and VR controllers for user engagement.
- Integration with blockchain technology using Web3.js.
- Responsive web interface using A-Frame.

## Technologies Used

- **Unity**: For building AR/VR applications.
- **A-Frame**: For creating web-based AR/VR experiences.
- **Node.js**: For the backend server.
- **Express**: For building the API.
- **Mongoose**: For MongoDB object modeling.
- **Web3.js**: For interacting with the Ethereum blockchain.
- **Jest**: For testing.

## Project Structure

```
ar-vr-experience/
│
├── unity/
│   ├── Assets/
│   │   ├── Scripts/
│   │   │   ├── MarketDataFetcher.cs
│   │   │   ├── ARController.cs
│   │   │   └── VRController.cs
│   │   ├── Prefabs/
│   │   │   ├── MarketItem.prefab
│   │   └── Scenes/
│   │       ├── MainScene.unity
│   │       └── ARScene.unity
│   ├── ProjectSettings/
│   │   └── ProjectSettings.asset
│   └── ar-vr-experience.unity
│
├── aframe/
│   ├── index.html
│   ├── js/
│   │   ├── marketDataFetcher.js
│   │   ├── arController.js
│   │   └── vrController.js
│   ├── assets/
│   │   ├── models/
│   │   └── images/
│   └── styles/
│       └── styles.css
│
├── api/
│   ├── marketDataAPI.js
│   └── userDataAPI.js
│
├── config/
│   ├── db.js
│   ├── web3.js
│   └── server.js
│
├── tests/
│   ├── marketDataFetcher.test.js
│   ├── arController.test.js
│   └── vrController.test.js
│
├── .env
├── package.json
└── README.md
```

## Installation

### Prerequisites

- Node.js (version 14 or higher)
- MongoDB (for local development)
- Unity (for AR/VR development)

### Steps

1. **Clone the repository**:

   ```bash
   git clone https://github.com/KOSASIH/stable-pi-core.git
   cd ar-vr-experience
   ```

2. **Install Node.js dependencies**:

   ```bash
   npm install
   ```

3. **Set up the environment variables**:

   Create a `.env` file in the root directory and add your configuration:

   ```plaintext
   MONGODB_URI=mongodb://localhost:27017/yourDatabaseName
   MARKET_DATA_API_URL=https://api.example.com/marketdata
   USER_DATA_API_URL=https://api.example.com/users
   INFURA_PROJECT_ID=your_infura_project_id_here
   ETHEREUM_NODE_URL=https://mainnet.infura.io/v3/${INFURA_PROJECT_ID}
   PORT=5000
   ```

4. **Run the server**:

   ```bash
   npm start
   ```

5. **For development mode** (with automatic restarts):

   ```bash
   npm run dev
   ```

6. **Run tests**:

   ```bash
   npm test
   ```

## Usage

- **Unity**: Open the Unity project file (`ar-vr-experience.unity`) in Unity Editor to develop and build the AR/VR application.
- **A-Frame**: Open `index.html` in a web browser to view the web-based AR/VR experience.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any suggestions or improvements.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Thanks to the developers of Unity, A-Frame, and all the libraries used in this project.
- Special thanks to the open-source community for their contributions.
