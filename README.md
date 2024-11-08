# LoRa Chatbot Application

This project is a LoRa Chatbot that provides intelligent conversations for IoT networks using LoRa and LoRaWAN technologies. It consists of a backend built with FastAPI and a frontend built with React and TypeScript using Vite.

## Features

- **Backend**: FastAPI application with endpoints for chat functionality.
- **Frontend**: React application with a chat interface.
- **Docker Support**: Dockerfiles provided for easy deployment.
- **Environment Variables**: Uses `.env` files to manage secrets and configuration.
- **CORS Configuration**: Configured to allow requests from the frontend.

## Notebooks
The notebooks directory contains several Jupyter Notebooks used for data collection, model evaluation, and hyperparameter tuning:

- 01_data_articles_collection.ipynb: Collecting articles related to LoRaWAN.
- 02_data_faq_collection.ipynb: Collecting and cleaning FAQs about LoRaWAN.
- 05_evaluate_rag_llamaidx.ipynb: Evaluating models using llama_index.
- 06_anthropic_model.ipynb: Implementing models with the Anthropic API.
- 07_improve_hyperparameters.ipynb: Experimenting to improve hyperparameters.


## Deployment

The app is deployed using Docker. Now you can test the app navigating to `https://lorawan-chatbot-frontend.onrender.com` in your browser.

## Prerequisites

- **Docker**: To build and run Docker containers.
- **Node.js and npm**: For building and running the frontend.
- **Python 3.11**: If running the backend without Docker.
- **Poetry**: For managing dependencies. 
- **FastAPI**: For the backend.
- **React and TypeScript**: For the frontend.

## Project Structure

rag-app-lorawan/
├── app-llama/
│   ├── backend/
│   │   ├── main.py
│   │   ├── Dockerfile
│   │   ├── pyproject.toml
│   │   ├── poetry.lock
│   ├── frontend/
│   │   ├── src/
│   │   │   ├── App.tsx
│   │   │   ├── index.css
│   │   │   ├── main.tsx
│   │   ├── package.json
│   │   ├── index.html
│   │   ├── tsconfig.json
├── notebooks/
│   ├── 01_data_articles_collection.ipynb
│   ├── 02_data_faq_collection.ipynb
│   ├── 05_evaluate_rag_llamaidx.ipynb
│   ├── 06_anthropic_model.ipynb
│   ├── 07_improve_hyperparameters.ipynb

## API Endpoints

The FastAPI backend provides the following endpoints:

- POST `/chat`: The endpoint for sending chat messages.

### Sample Request

```json
POST /chat
Content-Type: application/json

{
  "query": "What is LoRaWAN?"
}
```

### Sample Response

```json
{
  "response": "LoRaWAN is a communication protocol for low-power wide-area networks (LPWAN) designed for IoT devices."
}
```

## License

This project is licensed under the MIT License. See the LICENSE file for details.


## Future Improvements
- Continuous Integration: Setting up CI/CD pipelines for automated testing and deployment.
- Authentication: Implementing user authentication and authorization.
- Internationalization: Adding support for multiple languages.
- Documentation: Expanding detailed API and development documentation.
  
## Additional Resources
- LoRaWAN Documentation: LoRa Alliance
- FastAPI Documentation: FastAPI
- React Documentation: React
- Vite Documentation: Vite
- Docker Documentation: Docker