# Use the official Node.js image as the base image
FROM node:18-alpine AS build

# Set the working directory
WORKDIR /usr/src/app

# Copy package.json and package-lock.json
COPY package*.json ./

# Install dependencies
RUN npm install --production

# Copy the rest of the application code
COPY . .

# Build the application (if applicable)
# RUN npm run build

# Use a smaller image for the production environment
FROM node:18-alpine AS production

# Set the working directory
WORKDIR /usr/src/app

# Copy only the necessary files from the build stage
COPY --from=build /usr/src/app .

# Expose the application port
EXPOSE 3000

# Set environment variables (optional)
ENV NODE_ENV=production

# Start the application
CMD ["node", "index.js"]
