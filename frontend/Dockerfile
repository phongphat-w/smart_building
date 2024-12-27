#========================
# Production Deployment 
#========================

# # Use a lightweight Node.js image
# FROM node:22.12-slim

# # Set the working directory
# WORKDIR /app

# # Install only the production server dependencies
# COPY COPY package.json package-lock.json ./
# RUN npm install --only=production

# # Copy the React build folder
# COPY ./build ./build

# # Copy the server.js file (Express server)
# COPY ./server.js ./server.js

# # Expose the port React app will run on
# EXPOSE 3000

# # Run the Express server to serve the build folder
# CMD ["node", "server.js"]


#========================
# Development Deployment 
#========================

# Use Node.js official image
FROM node:22.12-slim

# Set working directory
WORKDIR /app

# Copy package.json and package-lock.json to the container
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy all source code to the working directory
COPY . .

# Expose the port React uses (default is 3000)
EXPOSE 3000

# Start the development server
# CMD ["npm", "start"]
# Run the Express server to serve the build folder
CMD ["node", "server.js"]