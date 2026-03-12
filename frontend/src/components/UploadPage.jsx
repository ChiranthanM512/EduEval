import React, { useEffect, useRef, useState } from "react";
import API from "../api";
import { motion } from "framer-motion";
import eduImg from "../assets/image3.png";

export default function UploadPage() {
  const [file, setFile] = useState(null);
  const [modelAnswers, setModelAnswers] = useState([]);
  const [selectedModelId, setSelectedModelId] = useState("");

  const [output, setOutput] = useState(null);
  const [loading, setLoading] = useState(false);

  // ✅ Refs for smooth scrolling
  const uploadRef = useRef(null);
  const outputRef = useRef(null);

  // -------------------------
  // Load model answers
  // -------------------------
  async function loadModelAnswers() {
    try {
      const res = await API.get("/model-answers/");
      setModelAnswers(res.data || []);
    } catch (err) {
      console.error(err);
      alert("Failed to load model answers.");
    }
  }

  useEffect(() => {
    loadModelAnswers();
  }, []);

  // -------------------------
  // Upload + Evaluate
  // -------------------------
  async function uploadAndEval() {
    if (!file) return alert("Please upload a file!");
    if (!selectedModelId) return alert("Please select a model answer!");

    try {
      setLoading(true);
      setOutput(null);

      // 1) Upload file
      const formData = new FormData();
      formData.append("file", file);

      const uploadRes = await API.post("/files/upload", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });

      // ✅ support both possible keys: path or file_path
      const filePath = uploadRes.data.path || uploadRes.data.file_path;

      if (!filePath) {
        alert("Upload succeeded but file path not returned!");
        return;
      }

      // 2) Evaluate
      const evalRes = await API.post("/eval/", {
        file_path: filePath,
        model_answer_id: Number(selectedModelId),
      });

      setOutput(evalRes.data);

      // ✅ scroll to output
      setTimeout(() => {
        if (outputRef.current) {
          outputRef.current.scrollIntoView({
            behavior: "smooth",
            block: "start",
          });
        }
      }, 250);
    } catch (err) {
      console.error(err);
      alert(err?.response?.data?.detail || "Evaluation failed. Check backend logs.");
    } finally {
      setLoading(false);
    }
  }

  // -------------------------
  // Helpers
  // -------------------------
  function handleScrollToUpload() {
    if (uploadRef.current) {
      uploadRef.current.scrollIntoView({
        behavior: "smooth",
        block: "start",
      });
    }
  }

  function resetForm() {
    setFile(null);
    setSelectedModelId("");
    setOutput(null);
  }

  return (
    <div className="container">
      {/* ✅ HERO SECTION */}
      <motion.div
        className="card"
        initial={{ opacity: 0, y: 18 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.45 }}
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          gap: "25px",
          padding: "35px",
        }}
      >
        {/* Left Side */}
        <div style={{ flex: 1 }}>
          <h1 style={{ fontSize: "42px", marginBottom: "10px" }}>
            Upload & Evaluate 📝
          </h1>

          <p style={{ fontSize: "15px", opacity: 0.85, maxWidth: "520px" }}>
            Upload student answer sheets (JPG / PNG / PDF), select a model answer,
            and get semantic scoring + keyword feedback + Explainable AI output.
          </p>

          <motion.button
            whileHover={{ y: -2, scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
            onClick={handleScrollToUpload}
            style={{ marginTop: "18px" }}
          >
            Evaluate Now ↓
          </motion.button>
        </div>

        {/* Right Side Image */}
        <motion.div
          initial={{ opacity: 0, scale: 0.96 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.5 }}
          style={{
            flex: 1,
            display: "flex",
            justifyContent: "flex-end",
          }}
        >
          <img
            src={eduImg}
            alt="Education"
            style={{
              width: "100%",
              maxWidth: "650px",
              height: "260px",
              objectFit: "cover",
              borderRadius: "18px",
              boxShadow: "0px 8px 22px rgba(0,0,0,0.15)",
            }}
          />
        </motion.div>
      </motion.div>

      {/* ✅ INFO CARD */}
      <motion.div
        className="card"
        initial={{ opacity: 0, y: 18 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.45, delay: 0.05 }}
        style={{
          borderLeft: "6px solid #0d6efd",
          background: "#f8fbff",
        }}
      >
        <h2 style={{ marginBottom: "10px" }}>How it works</h2>

        <div
          style={{
            background: "white",
            border: "1px solid #dfe7ff",
            borderRadius: "12px",
            padding: "15px",
            fontSize: "14px",
            lineHeight: "1.6",
          }}
        >
          <b>Step 1:</b> Upload student answer sheet <br />
          <b>Step 2:</b> Select model answer <br />
          <b>Step 3:</b> OCR extracts handwritten text <br />
          <b>Step 4:</b> SBERT calculates semantic similarity <br />
          <b>Step 5:</b> Missing keywords + feedback generated <br />
          <b>Step 6:</b> Explainable AI highlights matched + missing points
        </div>
      </motion.div>

      {/* ✅ UPLOAD FORM */}
      <motion.div
        ref={uploadRef}
        className="card"
        initial={{ opacity: 0, y: 18 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.45, delay: 0.07 }}
      >
        <h2>Upload & Evaluate</h2>

        <label>Upload Answer Sheet (JPG/PNG/PDF)</label>
        <input
          type="file"
          accept=".jpg,.jpeg,.png,.pdf"
          onChange={(e) => setFile(e.target.files[0])}
        />

        <label>Select Model Answer</label>
        <select
          value={selectedModelId}
          onChange={(e) => setSelectedModelId(e.target.value)}
        >
          <option value="">-- Select --</option>
          {modelAnswers.map((m) => (
            <option key={m.id} value={m.id}>
              {m.id} - {m.question_title}
            </option>
          ))}
        </select>

        <br />
        <br />

        <div style={{ display: "flex", gap: "12px", flexWrap: "wrap" }}>
          <motion.button
            whileHover={{ y: -2, scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
            onClick={uploadAndEval}
            disabled={loading}
          >
            {loading ? "Evaluating..." : "Evaluate"}
          </motion.button>

          <motion.button
            whileHover={{ y: -2, scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
            onClick={resetForm}
            style={{ backgroundColor: "#6c757d" }}
          >
            Reset
          </motion.button>
        </div>
      </motion.div>

      {/* ✅ OUTPUT */}
      {output && (
        <motion.div
          ref={outputRef}
          className="card"
          initial={{ opacity: 0, y: 18 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.45 }}
        >
          <h2>Evaluation Output</h2>

          <p>
            <b>OCR Engine:</b> {output.ocr_engine}
          </p>
          <p>
            <b>Language:</b> {output.language}
          </p>
          <p>
            <b>Score:</b> {output.score}
          </p>
          <p>
            <b>Feedback:</b> {output.feedback}
          </p>

          <hr />

          <h3>Extracted Text</h3>
          <div
            style={{
              background: "#f7f7f7",
              padding: "12px",
              borderRadius: "10px",
              whiteSpace: "pre-wrap",
            }}
          >
            {output.text}
          </div>

          <br />

          <h3>Missing Keywords</h3>
          {output.missing_keywords && output.missing_keywords.length > 0 ? (
            <ul>
              {output.missing_keywords.map((k, i) => (
                <li key={i}>{k}</li>
              ))}
            </ul>
          ) : (
            <p>No missing keywords 🎉</p>
          )}

          <hr />

          {/* ✅ Explainable AI */}
          <h3>Explainable AI</h3>

          {output.explainable_ai ? (
            <div style={{ fontSize: "14px", lineHeight: "1.7" }}>
              <p>
                <b>Similarity:</b> {output.explainable_ai.similarity}
              </p>
              <p>
                <b>Length Ratio:</b> {output.explainable_ai.length_ratio}
              </p>

              <p>
                <b>Explanation:</b>
              </p>
              <div
                style={{
                  background: "#f8fbff",
                  border: "1px solid #dfe7ff",
                  padding: "12px",
                  borderRadius: "12px",
                  whiteSpace: "pre-wrap",
                }}
              >
                {output.explainable_ai.explanation}
              </div>

            </div>
          ) : (
            <p style={{ opacity: 0.75 }}>
              Explainable AI not returned by backend.
            </p>
          )}
        </motion.div>
      )}
    </div>
  );
}
