# Use Node.js official image
FROM node:22

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
CMD ["npm", "start"]
