# Omni-Dimensional Nexus Converter (ODNC)

The **Omni-Dimensional Nexus Converter (ODNC)** is a cutting-edge application designed to identify, convert, and predict the extraction of various types of energy from multiple dimensions. Leveraging advanced machine learning algorithms and a user-friendly interface, ODNC provides a powerful tool for researchers, engineers, and enthusiasts in the field of energy conversion and resource extraction.

## Features

- **Energy Conversion**: Convert different types of energy (e.g., dimensional, quantum, dark) with high efficiency.
- **Resource Prediction**: Utilize AI-driven predictions to identify the most profitable resources to extract from other dimensions.
- **User -Friendly Interface**: A responsive and intuitive interface built with React and Material-UI.
- **Conversion History**: Keep track of previous conversions and predictions for easy reference.
- **Real-Time Feedback**: Loading indicators and error handling to enhance user experience.

## Installation

To set up the Omni-Dimensional Nexus Converter on your local machine, follow these steps:

### Prerequisites

- Node.js (v14 or higher)
- MongoDB (for data persistence)
- Git

### Clone the Repository

```bash
git clone https://github.com/KOSASIH/stable-pi-core.git
cd stable-pi-core/src/ODNC
```

### Install Dependencies

1. **Backend**: Navigate to the backend directory and install the required packages.

```bash
cd backend
npm install
```

2. **Frontend**: Navigate to the frontend directory and install the required packages.

```bash
cd frontend
npm install
```

### Configure Environment Variables

Create a `.env` file in the backend directory and add your MongoDB connection string:

```
MONGODB_URI=mongodb://<username>:<password>@localhost:27017/odnc
```

### Start the Application

1. **Start MongoDB**: Ensure your MongoDB server is running.

2. **Run the Backend**:

```bash
cd backend
node server.js
```

3. **Run the Frontend**:

```bash
cd frontend
npm start
```

The application should now be running at `http://localhost:3000`.

## Usage

1. Open your web browser and navigate to `http://localhost:3000`.
2. Enter the energy type and amount you wish to convert.
3. Click on "Convert Energy" to see the converted amount.
4. Click on "Predict Resource Extraction" to get predictions based on the entered energy data.
5. Review the conversion history and predicted resource extraction results displayed on the interface.

## API Documentation

### Convert Energy

- **Endpoint**: `POST /api/convert-energy`
- **Request Body**:
  ```json
  {
    "energyType": "string",
    "amount": "number"
  }
  ```
- **Response**:
  ```json
  {
    "success": true,
    "result": "number"
  }
  ```

### Predict Resource Extraction

- **Endpoint**: `POST /api/predict-extraction`
- **Request Body**:
  ```json
  {
    "energyData": [
      {
        "type": "string",
        "amount": "number"
      }
    ]
  }
  ```
- **Response**:
  ```json
  {
    "success": true,
    "prediction": [
      {
        "type": "string",
        "predictedValue": "number"
      }
    ]
  }
  ```

## Contributing

We welcome contributions to the Omni-Dimensional Nexus Converter! If you would like to contribute, please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/YourFeature`).
3. Make your changes and commit them (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature/YourFeature`).
5. Open a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [TensorFlow.js](https://www.tensorflow.org/js) for machine learning capabilities.
- [Material-UI](https://mui.com/) for the user interface components.
- [Express](https://expressjs.com/) for the backend server framework.

## Contact

For any inquiries or feedback, please reach out to the project maintainer.
