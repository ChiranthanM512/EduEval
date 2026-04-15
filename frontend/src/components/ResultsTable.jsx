import React, { useEffect, useRef, useState } from "react";
import API from "../api";
import { motion, AnimatePresence } from "framer-motion";
import eduImg from "../assets/image6.jpg";

export default function ResultsTable() {
  const [rows, setRows] = useState([]);
  const [selectedRow, setSelectedRow] = useState(null);
  const [loading, setLoading] = useState(false);

  // ✅ Ref for smooth scrolling
  const tableRef = useRef(null);

  async function loadResults() {
    try {
      setLoading(true);
      const res = await API.get("/results/");
      setRows(res.data || []);
    } catch (err) {
      console.log(err);
      alert("Failed to load results");
    } finally {
      setLoading(false);
    }
  }

  async function handleDelete(id) {
    try {
      if (!window.confirm("Delete this result?")) return;

      await API.delete(`/results/${id}`);
      loadResults();
    } catch (err) {
      console.log(err);
      alert("Failed to delete");
    }
  }

  function safeParseExplainable(row) {
    // ✅ if backend already returns explainable_ai as object
    if (row?.explainable_ai && typeof row.explainable_ai === "object") {
      return row.explainable_ai;
    }

    // ✅ if backend returns explainable_output as string
    const raw = row?.explainable_output;

    if (!raw || typeof raw !== "string") return null;

    try {
      return JSON.parse(raw);
    } catch (e) {
      return null;
    }
  }

  function scrollToTable() {
    if (tableRef.current) {
      tableRef.current.scrollIntoView({
        behavior: "smooth",
        block: "start",
      });
    }
  }

  useEffect(() => {
    loadResults();
  }, []);

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
            Results History 📊
          </h1>

          <p style={{ fontSize: "15px", opacity: 0.85, maxWidth: "520px" }}>
            View all evaluated answer sheets, check score trends, and open full
            details including Explainable AI output.
          </p>

          <div style={{ display: "flex", gap: "12px", flexWrap: "wrap" }}>
            <motion.button
              whileHover={{ y: -2, scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
              onClick={scrollToTable}
              style={{ marginTop: "18px" }}
            >
              View Results ↓
            </motion.button>

            <motion.button
              whileHover={{ y: -2, scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
              onClick={loadResults}
              style={{
                marginTop: "18px",
                backgroundColor: "#6c757d",
              }}
            >
              {loading ? "Refreshing..." : "Refresh"}
            </motion.button>
          </div>
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
            alt="Results"
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

      {/* ✅ RESULTS TABLE CARD */}
      <motion.div
        ref={tableRef}
        className="card"
        initial={{ opacity: 0, y: 18 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.45, delay: 0.05 }}
      >
        <div
          style={{
            display: "flex",
            justifyContent: "space-between",
            alignItems: "center",
            gap: "12px",
            flexWrap: "wrap",
          }}
        >
          <h2 style={{ margin: 0 }}>Evaluation History</h2>

          <span style={{ opacity: 0.75, fontSize: "14px" }}>
            Total Results: <b>{rows.length}</b>
          </span>
        </div>

        <br />

        {rows.length === 0 ? (
          <p style={{ opacity: 0.8 }}>
            No results yet. Upload and evaluate an answer sheet first.
          </p>
        ) : (
          <div style={{ overflowX: "auto" }}>
            <table border="1" cellPadding="12" width="100%">
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Score</th>
                  <th>OCR Engine</th>
                  <th>Language</th>
                  <th>Feedback</th>
                  <th>Extracted Text</th>
                  <th>Action</th>
                </tr>
              </thead>

              <tbody>
                {rows.map((r, index) => (
                  <motion.tr
                    key={r.id}
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.25, delay: index * 0.03 }}
                  >
                    <td>{r.id}</td>
                    <td>
                      <b>{Number(r.score).toFixed(2)}%</b>
                    </td>
                    <td>{r.ocr_engine}</td>
                    <td>{r.language}</td>
                    <td style={{ maxWidth: "240px" }}>{r.feedback}</td>
                    <td style={{ maxWidth: "340px" }}>
                      {r.extracted_text?.slice(0, 140)}...
                    </td>
                    <td>
                      <motion.button
                        whileHover={{ y: -2, scale: 1.03 }}
                        whileTap={{ scale: 0.97 }}
                        onClick={() => setSelectedRow(r)}
                        style={{
                          background: "#2563eb",
                          color: "white",
                          padding: "7px 14px",
                          border: "none",
                          borderRadius: "10px",
                          cursor: "pointer",
                          marginRight: "10px",
                        }}
                      >
                        View
                      </motion.button>

                      <motion.button
                        whileHover={{ y: -2, scale: 1.03 }}
                        whileTap={{ scale: 0.97 }}
                        onClick={() => handleDelete(r.id)}
                        style={{
                          background: "#dd2828",
                          color: "white",
                          padding: "7px 14px",
                          border: "none",
                          borderRadius: "10px",
                          cursor: "pointer",
                        }}
                      >
                        Delete
                      </motion.button>
                    </td>
                  </motion.tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </motion.div>

      {/* ✅ VIEW MODAL (Animated) */}
      <AnimatePresence>
        {selectedRow && (
          <motion.div
            style={{
              position: "fixed",
              top: 0,
              left: 0,
              width: "100%",
              height: "100%",
              background: "rgba(0,0,0,0.45)",
              display: "flex",
              justifyContent: "center",
              alignItems: "center",
              padding: "20px",
              zIndex: 9999,
            }}
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
          >
            <motion.div
              style={{
                background: "white",
                padding: "25px",
                borderRadius: "18px",
                width: "85%",
                maxWidth: "950px",
                maxHeight: "85%",
                overflowY: "auto",
                boxShadow: "0px 18px 50px rgba(0,0,0,0.25)",
              }}
              initial={{ opacity: 0, y: 25, scale: 0.98 }}
              animate={{ opacity: 1, y: 0, scale: 1 }}
              exit={{ opacity: 0, y: 25, scale: 0.98 }}
              transition={{ duration: 0.3 }}
            >
              <h2 style={{ marginTop: 0 }}>
                Result Details (ID: {selectedRow.id})
              </h2>

              <p>
                <b>Score:</b> {Number(selectedRow.score).toFixed(2)}%
              </p>
              <p>
                <b>Feedback:</b> {selectedRow.feedback}
              </p>

              <hr />

              <h3>Explainable AI</h3>

              {(() => {
                const exp = safeParseExplainable(selectedRow);

                if (!exp) {
                  return (
                    <p style={{ color: "gray" }}>
                      Not available for this old result.
                      <br />
                      Evaluate again to generate explainable output.
                    </p>
                  );
                }

                return (
                  <div style={{ fontSize: "14px", lineHeight: "1.7" }}>
                    <p>
                      <b>Similarity:</b> {exp.similarity}
                    </p>
                    <p>
                      <b>Length Ratio:</b> {exp.length_ratio}
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
                      {exp.explanation}
                    </div>

                    </div>
                  );
                })()}

              <hr />

              <h3>Extracted Text</h3>
              <div
                style={{
                  background: "#f9fafb",
                  padding: "12px",
                  borderRadius: "12px",
                  whiteSpace: "pre-wrap",
                }}
              >
                {selectedRow.extracted_text}
              </div>

              <br />

              <motion.button
                whileHover={{ y: -2, scale: 1.03 }}
                whileTap={{ scale: 0.97 }}
                onClick={() => setSelectedRow(null)}
                style={{
                  background: "#111827",
                  color: "white",
                  padding: "10px 18px",
                  border: "none",
                  borderRadius: "12px",
                  cursor: "pointer",
                }}
              >
                Close
              </motion.button>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
