# wx_utils

微信相关接口

---

## WeChat Access Token API

This project provides a FastAPI-based API to manage and retrieve the WeChat access token. The access token is automatically refreshed every 7000 seconds and can also be manually refreshed via a POST request. The API also includes logging to track access token retrieval and refresh operations.

### Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Logging](#logging)
- [Contributing](#contributing)
- [License](#license)

### Features

- Automatically refresh WeChat access token every 7000 seconds.
- Manually refresh access token via a POST request.
- Retrieve the current access token via a GET request.
- Logging of access token retrieval and refresh operations.
- Log files are rotated weekly.

### Prerequisites

- Python 3.7 or higher
- Pip (Python package installer)

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/Agent-Universe/wx_utils.git
   cd wx_utils
   ```

2. Install the required Python packages:
   ```bash
   pip install fastapi uvicorn requests python-dotenv apscheduler
   ```

### Configuration

1. Create a `.env` file in the root directory of the project and add your WeChat AppID and AppSecret:

   ```env
   APP_ID=your_app_id
   APP_SECRET=your_app_secret
   ```

2. Ensure that your server's IP address is added to the IP whitelist in the WeChat public platform settings.

### Usage

1. Start the FastAPI application:

   ```bash
   uvicorn getAccessToken:app --reload
   ```

2. The API will be available at `http://127.0.0.1:8000`.

### API Endpoints

#### Get Current Access Token

- **URL**: `/access_token`
- **Method**: `GET`
- **Response**:
  ```json
  {
    "access_token": "your_access_token"
  }
  ```

#### Manually Refresh Access Token

- **URL**: `/refresh_token`
- **Method**: `POST`
- **Response**:
  ```json
  {
    "message": "Access token refreshed successfully",
    "access_token": "your_new_access_token"
  }
  ```

### Logging

- Logs are stored in the `.log/` directory.
- Log files are named `access_token.log` and are rotated weekly.
- Log entries include timestamps, log levels, and messages.

### Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue.

### License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

For any questions or support, please contact [L4Walk](mailto:15@agent-universe.cn).
