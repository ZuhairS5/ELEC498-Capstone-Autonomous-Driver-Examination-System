const functions = require("firebase-functions");
const express = require("express");
const cors = require("cors");

const app = express();


app.use(cors({ origin: true })); // Reflects the request origin, as long as it's a valid CORS request
app.use(express.json()); // Parses incoming requests with JSON payloads


app.post('/checkPassword', (req, res) => {
  try {
    const userPassword = req.body.password;
    const hardcodedPassword = Buffer.from("Testing123").toString("base64");

    if (!userPassword) {
      res.status(400).send({ error: "Password is required" });
      return;
    }

    if (Buffer.from(userPassword).toString("base64") !== hardcodedPassword) {
      res.status(403).send({ error: "Incorrect password" });
      return;
    }

    // Assuming the password is correct, proceed with your operation
    // Replace this with the actual operation you want to perform
    res.status(200).json({ message: "Password correct!", data: {/* Your data here */} });
  } catch (error) {
    console.error(error);
    res.status(500).send({ error: "Internal Server Error" });
  }
});

// Expose Express API as a single Cloud Function:
exports.api = functions.https.onRequest(app);