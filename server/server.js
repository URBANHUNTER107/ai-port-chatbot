//At last of this file you'll find a simple Node.js server that responds to requests with a message. Looks a bit messy.
//So we use Express.js to make it cleaner and easier to read.

require("dotenv").config();

// Load Express (our web server toolkit) and Node's built-in
// "child_process" tool, which lets us run other programs
// (like Python) from inside our JavaScript code.
const express = require("express");
const { exec } = require("child_process");
const connectDB = require("./db");
const Message = require("./models/Message");

// Actually connect to MongoDB when the server starts
connectDB();

// Create the app - this represents our whole server.
const app = express();

// Middleware: teaches Express how to read JSON data sent to it.
// Needed so request.body actually contains something.
app.use(express.json());

// This tells Express: "any file inside the public folder should be automatically available to visitors." 
// So public/index.html becomes accessible just by visiting the homepage.
app.use(express.static("public"));

// Simple test route - just to confirm the server is alive.
app.get("/", (request, response) => {
    response.send("Hello Farhan, Express server is alive!");
});


// The main route. This is what the frontend will call whenever
// someone asks a question in the chat.
app.post("/ask", (request, response) => {

    const question = request.body.question;

    if (!question) {
        return response.status(400).json({ error: "No question provided." });
    }

    const command = `uv run python back.py "${question}"`;

    exec(command, { cwd: "C:\\Users\\HP\\Desktop\\AI Course\\aiportfolio_project" }, async (error, stdout, stderr) => {
        // NOTE: this callback is now "async" - required because we use
        // "await" inside it to save to MongoDB below.

        if (error) {
            console.error("Error running Python:", error);
            return response.status(500).json({ error: "Something went wrong." });
        }

        const answer = stdout.trim();

        // Save this question+answer pair to MongoDB
        try {
            await Message.create({
                question: question,
                answer: answer
            });

            console.log("Saved to MongoDB!");

        } catch (dbError) {
            // if saving fails, we still want to reply to the user -
            // just log the error instead of breaking the whole request
            console.error("Failed to save message:", dbError.message);
        }

        response.json({ reply: answer });
    });
});


//Route to read chat history from MongoDB. This is a GET route, meaning it just fetches data without changing anything.
// GET route to fetch all past messages, oldest first
app.get("/history", async (request, response) => {

    try {
        // .find({}) with no filters means "get everything"
        // .sort({ createdAt: 1 }) means oldest first (1 = ascending)
        const messages = await Message.find({}).sort({ createdAt: 1 });

        response.json(messages);

    } catch (error) {
        console.error("Failed to fetch history:", error.message);
        response.status(500).json({ error: "Could not load chat history." });
    }
});


// Start the server - open port 3000 and wait for requests.
app.listen(3000, () => {
    console.log("Express server running! Visit http://localhost:3000");
});





// First Code Snippet: A simple Node.js server without Express.js

// // "require" is how Node.js loads built-in tools.
// // "http" is a tool that's built into Node itself - no installing needed -
// // it lets us create a basic web server.
// const http = require("http");

// // This creates the server. The function inside runs every single time
// // someone sends a request to this server.
// const server = http.createServer((request, response) => {

//     // "request" = info about what the visitor is asking for
//     // "response" = our tool to send something back to them

//     console.log("Someone visited the server!");

//     // response.end() sends text back and finishes the response
//     response.end("Hello Farhan, your server is alive!");
// });

// // This tells the server: "start listening on port 3000"
// // A "port" is just a numbered doorway on your computer - like an
// // apartment number. Port 3000 is a common choice for local testing.
// server.listen(3000, () => {
//     console.log("Server is running! Visit http://localhost:3000");
// });




// Second Code Snippet: A simple Node.js server using Express.js

//Here, we just modified the above Node.js server to use Express.js, which is a popular library that makes it easier to write servers. 
// The code is cleaner and more readable, and we can easily add more routes (URLs) in the future.

// // Load Express (the library we just installed)
// const express = require("express");

// // Create an "app" - this represents our whole server.
// // Every route (URL) and rule we define attaches to this "app" object.
// const app = express();

// // Define what happens when someone visits "/" (the homepage)
// // using a GET request (GET = "just give me info", the normal
// // kind of request your browser makes when you visit a URL).
// app.get("/", (request, response) => {
//     response.send("Hello Farhan, Express server is alive!");
// });

// // Define a SECOND route - this is where Express shines.
// // Adding more URLs is just... adding more of these blocks.
// app.get("/about", (request, response) => {
//     response.send("This is Farhan's AI portfolio backend.");
// });

// // Start the server, same idea as before - listen on port 3000
// app.listen(3000, () => {
//     console.log("Express server running! Visit http://localhost:3000");
// });




//Third Code Snippet: A more advanced Express.js server that can handle POST requests and read JSON data.

//Here's a more advanced version of the Express server that can handle POST requests and read JSON data sent to it. 
// This is useful for when the frontend sends data (like a user's question) to the backend.

// const express = require("express");
// const app = express();

// // This is "middleware" - a setup step that runs on EVERY request,
// // before your route functions run. This specific one teaches
// // Express how to read JSON data that gets sent to it.
// // Without this line, request.body would be empty/undefined.
// app.use(express.json());

// // Existing routes, unchanged
// app.get("/", (request, response) => {
//     response.send("Hello Farhan, Express server is alive!");
// });

// app.get("/about", (request, response) => {
//     response.send("This is Farhan's AI portfolio backend.");
// });

// // NEW: a POST route. This is where the user's question will
// // eventually be sent from the frontend.
// app.post("/ask", (request, response) => {

//     // request.body contains whatever data was sent to us.
//     // Right now we're just testing, so we'll manually check
//     // for a field called "question".
//     const question = request.body.question;

//     console.log("Received a question:", question);

//     // send a reply back, echoing what we received - just to prove
//     // the data made it through correctly
//     response.json({
//         reply: "You asked: " + question
//     });
// });

// app.listen(3000, () => {
//     console.log("Express server running! Visit http://localhost:3000");
// });
