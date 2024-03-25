const express = require("express");
const cors = require("cors");
const app = express();

app.use(cors({ origin: 'http://localhost:3000', credentials: true }));
app.use(express.json());

app.options('*', cors());

app.post('/checkPassword', (req, res) => {
  try {
    const userPassword = req.body.password;
    const hardcodedPassword = Buffer.from("Testing123").toString("base64");

    if (!userPassword) {
      return res.status(400).json({ success: false, error: "Password is required" });
    }

    const isPasswordCorrect = Buffer.from(userPassword).toString("base64") === hardcodedPassword;
    return res.status(200).json({ success: isPasswordCorrect });
  } catch (error) {
    console.error(error);
    return res.status(500).json({ success: false, error: "Internal Server Error" });
  }
});

// Expose Express API as a single Cloud Function:
exports.api = functions.https.onRequest(app);