const express = require("express");
const multer = require("multer");
const pdfParse = require("pdf-parse");
const axios = require("axios");

const router = express.Router();
const upload = multer();

router.post("/", upload.single("resume"), async (req, res) => {
  try {
    const pdfData = await pdfParse(req.file.buffer);
    const text = pdfData.text;

    const mlApiUrl = process.env.ML_API_URL || "http://127.0.0.1:8000/analyze";
    const response = await axios.post(mlApiUrl, {
      resume_text: text
    });

    res.json(response.data);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

module.exports = router;