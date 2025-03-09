# RPA Automation Project

## Overview

This RPA (Robotic Process Automation) project is designed to automate various business processes, including data extraction, data entry, and error handling. The project leverages UiPath to create workflows that improve efficiency and reduce manual effort.

## Features

- **Data Extraction**: Extracts data from various sources, including web applications and databases.
- **Data Entry**: Automates the entry of data into applications and systems.
- **Error Handling**: Implements robust error handling to ensure smooth execution and logging of issues.
- **Integration Tests**: Validates end-to-end scenarios and error handling to ensure the reliability of the automation processes.

## Prerequisites

Before you begin, ensure you have the following installed:

- [UiPath Studio](https://www.uipath.com/platform/trial) (version X.X or later)
- .NET Framework (version X.X or later)
- Access to the necessary data sources and applications

## Setup Instructions

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/KOSASIH/stable-pi-core.git
   cd stable-pi-core/rpa-automation-project
   ```

2. **Open the Project in UiPath Studio**:
   - Launch UiPath Studio.
   - Click on "Open" and navigate to the cloned project directory.
   - Select the `.xaml` file you want to work on.

3. **Configure Settings**:
   - Open the `Config.xlsx` file and update the configuration parameters as needed.
   - Update the `Credentials.json` file with your sensitive credentials (ensure this file is kept secure).

4. **Run the Workflows**:
   - Select the main workflow you want to execute.
   - Click on the "Run" button in UiPath Studio to start the automation process.

## Testing

- Unit tests are located in the `tests/UnitTests/` directory.
- Integration tests are located in the `tests/IntegrationTests/` directory.
- To run the tests, open the respective `.xaml` files in UiPath Studio and execute them.

## Logging

- Logs are stored in the `logs/` directory.
- The log files include:
  - `log_YYYYMMDD_HHMM.log`: Tracks bot activities.
  - `error_log_YYYYMMDD_HHMM.log`: Tracks errors encountered during execution.

## Contributing

Contributions are welcome! If you have suggestions for improvements or new features, please create an issue or submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

For any questions or inquiries, please contact:

- **GitHub**: [KOSASIH](https://github.com/KOSASIH)
