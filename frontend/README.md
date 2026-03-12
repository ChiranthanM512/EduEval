# EduEval Frontend

This is the React-based frontend for the EduEval project, a handwritten text evaluation tool with multi-language support and AI-driven semantic analysis.

## 🚀 Getting Started

### Prerequisites

- **Node.js**: Ensure you have Node.js installed on your system.
- **npm**: Node Package Manager (comes with Node.js).

### Setup and Installation

1.  **Navigate to the frontend directory**:
    ```bash
    cd frontend
    ```

2.  **Install dependencies**:
    ```bash
    npm install
    ```
    *Note: If you have issues with `react-scripts`, we have fixed it in `package.json` to version `5.0.1`.*

3.  **Run the application**:
    ```bash
    npm start
    ```
    The application should open at [http://localhost:3000](http://localhost:3000).

---

## 🛠️ Key Features

- **Multi-language Support**: Interface for evaluating English, Hindi, Tamil, Telugu, and more.
- **AI Explanations**: Visual feedback and text-based explanations powered by Google Gemini.
- **Advanced Semantic Analysis**: Real-time scoring using SBERT and Gemini logic refinement.
- **Handwritten Image Upload**: Support for JPG, PNG, and multi-page PDF documents.

## 📖 Available Scripts

- `npm start`: Runs the app in development mode.
- `npm run build`: Builds the app for production.
- `npm test`: Launches the test runner.

## 🤝 Troubleshooting

If you encounter the error `'react-scripts' is not recognized`:
- Ensure you have run `npm install`.
- Check if `node_modules` exists in the `frontend` folder.
- Run `npm install react-scripts --save` to manually force the installation if needed.
