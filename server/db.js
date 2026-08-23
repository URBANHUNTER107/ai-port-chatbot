// This file's only job: connect to MongoDB and let other files
// know if it succeeded or failed.

const mongoose = require("mongoose");

// This function connects to MongoDB using the URI stored in .env
async function connectDB() {

    try {
        // process.env.MONGO_URI reads the value we put in .env
        await mongoose.connect(process.env.MONGO_URI);

        console.log("MongoDB connected successfully!");

    } catch (error) {
        console.error("MongoDB connection failed:", error.message);
    }
}

// Export this function so server.js can use it
module.exports = connectDB;