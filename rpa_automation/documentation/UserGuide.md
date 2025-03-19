# User Guide for RPA Automation Solution

## Table of Contents
1. [Introduction](#introduction)
2. [Getting Started](#getting-started)
3. [Operating the Workflows](#operating-the-workflows)
   - [Running Workflows](#running-workflows)
   - [Input Parameters](#input-parameters)
   - [Output Results](#output-results)
4. [Troubleshooting](#troubleshooting)
5. [Best Practices](#best-practices)
6. [Additional Resources](#additional-resources)
7. [Contact Information](#contact-information)

## Introduction

This user guide provides detailed instructions for operating the RPA Automation Solution. The solution is designed to automate various business processes, including data extraction, data entry, and error handling. This guide will help you understand how to set up, run, and troubleshoot the workflows.

## Getting Started

### Prerequisites
Before you begin, ensure you have the following installed:
- [UiPath Studio](https://www.uipath.com/platform/trial) (version 2021.10 or later)
- .NET Framework (version 4.6.1 or later)
- Access to the necessary data sources and applications

### Installation
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/KOSASIH/stable-pi-core.git
   cd stable-pi-core/rpa-automation-project
   ```

2. **Open the Project in UiPath Studio**:
   - Launch UiPath Studio.
   - Click on "Open" and navigate to the cloned project directory.
   - Select the main `.xaml` file you want to work on.

3. **Configure Settings**:
   - Open the `Config.xlsx` file and update the configuration parameters as needed.
   - Update the `Credentials.json` file with your sensitive credentials (ensure this file is kept secure).

## Operating the Workflows

### Running Workflows
1. **Select the Workflow**: In UiPath Studio, navigate to the workflow you want to run (e.g., `DataExtraction.xaml`, `DataEntry.xaml`).
2. **Run the Workflow**: Click on the "Run" button in UiPath Studio to start the automation process.
3. **Monitor Progress**: Watch the output panel for logs and messages indicating the progress of the workflow.

### Input Parameters
- Each workflow may require specific input parameters. Ensure you provide the necessary values in the workflow properties before running.
- Common input parameters include:
  - **SourceType**: The type of data source for extraction.
  - **DataToEnter**: The data that needs to be entered into the target application.

### Output Results
- After the workflow completes, check the output results in the designated output files (e.g., `output.xlsx`).
- Review the logs in the `logs/` directory for detailed information about the execution.

## Troubleshooting

### Common Issues
- **Workflow Fails to Start**: Ensure that all prerequisites are installed and that the project is opened correctly in UiPath Studio.
- **Data Extraction Errors**: Verify that the data source is accessible and that the query parameters are correct.
- **Data Entry Issues**: Ensure that the target application is open and that the fields are correctly mapped in the workflow.

### Logging
- Check the log files in the `logs/` directory for detailed error messages and stack traces.
- Use the `error_log_YYYYMMDD_HHMM.log` file to identify specific issues encountered during execution.

## Best Practices

- **Regularly Update Credentials**: Ensure that sensitive credentials are updated and stored securely.
- **Test Workflows**: Use the provided unit and integration tests to validate workflows before deploying them in a production environment.
- **Backup Configuration Files**: Regularly back up `Config.xlsx` and `Credentials.json` to prevent data loss.

## Additional Resources

- [UiPath Documentation](https://docs.uipath.com/)
- [UiPath Community Forum](https://forum.uipath.com/)
- [GitHub Repository](https://github.com/KOSASIH/stable-pi-core)

## Contact Information

For any questions or support, please contact:

- **GitHub**: [KOSASIH](https://github.com/KOSASIH)
