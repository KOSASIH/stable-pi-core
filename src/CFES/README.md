# Cosmo-Fractal Evolution Synthesizer (CFES)

The **Cosmo-Fractal Evolution Synthesizer (CFES)** is an advanced application designed to generate, visualize, and evolve fractals using cutting-edge algorithms and user-defined parameters. Leveraging WebGL for rendering and a user-friendly interface, CFES provides a powerful tool for artists, mathematicians, and enthusiasts to explore the infinite beauty of fractals.

## Features

- **Fractal Generation**: Generate complex fractals such as Mandelbrot and Julia sets with customizable parameters.
- **Real-time Visualization**: Experience real-time rendering of fractals using WebGL for smooth and interactive graphics.
- **User  Customization**: Adjust fractal parameters, including width, height, maximum iterations, and color schemes.
- **Feedback Mechanism**: Provide user feedback to evolve fractals based on preferences and suggestions.
- **Responsive Design**: Fully responsive interface that works seamlessly on various devices.

## Installation

To set up the Cosmo-Fractal Evolution Synthesizer on your local machine, follow these steps:

### Prerequisites

- Node.js (v14 or higher)
- MongoDB (for data persistence)
- Git

### Clone the Repository

```bash
git clone https://github.com/KOSASIH/stable-pi-core.git
cd stable-pi-core/src/CFES
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
MONGODB_URI=mongodb://<username>:<password>@localhost:27017/cfes
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
2. Select the fractal type (Mandelbrot or Julia) and adjust the parameters.
3. Click on "Generate Fractal" to visualize the fractal.
4. Provide feedback to evolve the fractal based on your preferences.
5. Review the generated fractal displayed on the canvas.

## API Documentation

### Generate Fractal

- **Endpoint**: `POST /api/generate-fractal`
- **Request Body**:
  ```json
  {
    "type": "string",
    "width": "number",
    "height": "number",
    "maxIterations": "number",
    "cX": "number",
    "cY": "number"
  }
  ```
- **Response**:
  ```json
  {
    "success": true,
    "fractal": {
      "id": "string",
      "pattern": "array",
      "width": "number",
      "height": "number"
    }
  }
  ```

### Evolve Fractal

- **Endpoint**: `POST /api/evolve-fractal`
- **Request Body**:
  ```json
  {
    "fractalId": "string",
    "userFeedback": "string"
  }
  ```
- **Response**:
  ```json
  {
    "success": true,
    "evolvedFractal": {
      "id": "string",
      "pattern": "array",
      "width": "number",
      "height": "number"
    }
  }
  ```

## Contributing

We welcome contributions to the Cosmo-Fractal Evolution Synthesizer! If you would like to contribute, please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/YourFeature`).
3. Make your changes and commit them (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature/YourFeature`).
5. Open a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [React](https://reactjs.org/) for building the user interface.
- [Three.js](https://threejs.org/) for WebGL rendering capabilities.
- [Material-UI](https://mui.com/) for the user interface components.
- [Express](https://expressjs.com/) for the backend server framework.

## Contact

For any inquiries or feedback, please reach out to the project maintainer.
