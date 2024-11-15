#!/bin/bash

# Script to run all tests

# Run unit tests
echo "Running unit tests..."
pytest tests/unit_tests/ --maxfail=1 --disable-warnings -q

# Run integration tests
echo "Running integration tests..."
pytest tests/integration_tests/ --maxfail=1 --disable-warnings -q

# Run end-to-end tests
echo "Running end-to-end tests..."
pytest tests/end_to_end_tests/ --maxfail=1 --disable-warnings -q

echo "All tests completed successfully!"
