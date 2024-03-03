const functions = require("firebase-functions");
const express = require("express");
const cors = require("cors");

const app = express();
app.use(cors({origin: true}));

exports.callMLModel = functions.https.onRequest((req, res) => {
  const userPassword = req.body.password;
  const hardcodedPassword = Buffer.from("Testing123").toString("base64");
  if (Buffer.from(userPassword).toString("base64") !== hardcodedPassword) {
    res.status(403).send("Incorrect password");
    return;
  }

  res.status(200).send("Password correct!");
});
