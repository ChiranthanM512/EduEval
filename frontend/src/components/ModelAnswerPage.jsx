import React, { useEffect, useRef, useState } from "react";
import API from "../api";
import { motion } from "framer-motion";
import eduImg from "../assets/image2.jpg";

export default function ModelAnswerPage() {
  const [title, setTitle] = useState("");
  const [text, setText] = useState("");
  const [answers, setAnswers] = useState([]);
  const [editing, setEditing] = useState(null);
  const [editTitle, setEditTitle] = useState("");
  const [editText, setEditText] = useState("");

  // ✅ Ref for scrolling to Create Form Card
  const createFormRef = useRef(null);

  async function loadAnswers() {
    const res = await API.get("/model-answers/");
    setAnswers(res.data);
  }

  async function createAnswer() {
    if (!title || !text) return alert("Enter title and model answer!");

    await API.post("/model-answers/", {
      question_title: title,
      model_text: text,
    });

    setTitle("");
    setText("");
    loadAnswers();
  }

  async function updateAnswer() {
    if (!editTitle || !editText) return alert("Enter title and model answer!");

    await API.put(`/model-answers/${editing}`, {
      question_title: editTitle,
      model_text: editText,
    });

    setEditing(null);
    setEditTitle("");
    setEditText("");
    loadAnswers();
  }

  async function deleteAnswer(id) {
    if (!window.confirm("Are you sure you want to delete this answer?")) return;

    await API.delete(`/model-answers/${id}`);
    loadAnswers();
  }

  function startEdit(answer) {
    setEditing(answer.id);
    setEditTitle(answer.question_title);
    setEditText(answer.model_text);

    // ✅ scroll to edit card
    setTimeout(() => {
      window.scrollTo({ top: document.body.scrollHeight, behavior: "smooth" });
    }, 150);
  }

  function cancelEdit() {
    setEditing(null);
    setEditTitle("");
    setEditText("");
  }

  // ✅ Scroll down when Start Creating clicked
  function handleStartCreating() {
    if (createFormRef.current) {
      createFormRef.current.scrollIntoView({
        behavior: "smooth",
        block: "start",
      });
    }
  }

  // ✅ Example Auto Fill
  function fillExample() {
    setTitle("Deadlock");
    setText(
      `Deadlock is a condition in an operating system where a group of processes are unable to proceed because each process is holding a resource and waiting for another resource held by another process.

Deadlock occurs when the following four necessary conditions are satisfied:
1) Mutual Exclusion
2) Hold and Wait
3) No Preemption
4) Circular Wait`
    );

    // scroll to form
    setTimeout(() => {
      if (createFormRef.current) {
        createFormRef.current.scrollIntoView({
          behavior: "smooth",
          block: "start",
        });
      }
    }, 100);
  }

  useEffect(() => {
    loadAnswers();
  }, []);

  return (
    <div className="container">
      {/* ✅ TOP HERO CARD */}
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
            Create Model Answer 📘
          </h1>

          <p style={{ fontSize: "15px", opacity: 0.85, maxWidth: "520px" }}>
            Add model answers to evaluate student responses using Hybrid OCR and
            semantic scoring.
          </p>

          <motion.button
            whileHover={{ y: -2, scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
            onClick={handleStartCreating}
            style={{ marginTop: "18px" }}
          >
            Start Creating
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

      {/* ✅ EXAMPLE CARD (NEW) */}
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
        <h2 style={{ marginBottom: "10px" }}>Example: How to Create Model Answer</h2>

        <p style={{ marginBottom: "12px", opacity: 0.85 }}>
          Follow this format while writing model answers:
        </p>

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
          <b>Question Title:</b> Deadlock
          <br />
          <br />
          <b>Model Answer:</b>
          <br />
          Deadlock is a condition in an operating system where a group of processes
          are unable to proceed because each process is holding a resource and
          waiting for another resource held by another process.
          <br />
          <br />
          Deadlock occurs when the following four necessary conditions are satisfied:
          <br />
          1) Mutual Exclusion <br />
          2) Hold and Wait <br />
          3) No Preemption <br />
          4) Circular Wait
        </div>

        <div style={{ marginTop: "15px", display: "flex", gap: "10px" }}>
          <motion.button
            whileHover={{ y: -2, scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
            onClick={fillExample}
          >
            Use This Example
          </motion.button>

          <motion.button
            whileHover={{ y: -2, scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
            onClick={handleStartCreating}
            style={{ backgroundColor: "#6c757d" }}
          >
            Go to Form ↓
          </motion.button>
        </div>
      </motion.div>

      {/* ✅ CREATE FORM CARD (TARGET SCROLL HERE) */}
      <motion.div
        ref={createFormRef}
        className="card"
        initial={{ opacity: 0, y: 18 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.45, delay: 0.07 }}
      >
        <h2>Create Model Answer</h2>

        <label>Question Title</label>
        <input value={title} onChange={(e) => setTitle(e.target.value)} />

        <label>Model Answer</label>
        <textarea
          rows={6}
          value={text}
          onChange={(e) => setText(e.target.value)}
        />

        <br />
        <br />

        <motion.button
          whileHover={{ y: -2, scale: 1.02 }}
          whileTap={{ scale: 0.98 }}
          onClick={createAnswer}
        >
          Save Model Answer
        </motion.button>
      </motion.div>

      {/* ✅ SAVED TABLE */}
      <motion.div
        className="card"
        initial={{ opacity: 0, y: 18 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.45, delay: 0.09 }}
      >
        <h2>Saved Model Answers</h2>

        {answers.length === 0 ? (
          <p>No model answers created yet.</p>
        ) : (
          <table border="1" cellPadding="10" width="100%">
            <thead>
              <tr>
                <th>ID</th>
                <th>Question Title</th>
                <th>Model Answer</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {answers.map((a) => (
                <tr key={a.id}>
                  <td>{a.id}</td>
                  <td>{a.question_title}</td>
                  <td style={{ maxWidth: "300px", wordWrap: "break-word" }}>
                    {a.model_text}
                  </td>
                  <td>
                    <motion.button
                      whileHover={{ y: -2, scale: 1.02 }}
                      whileTap={{ scale: 0.98 }}
                      onClick={() => startEdit(a)}
                      style={{ marginRight: "5px" }}
                    >
                      Edit
                    </motion.button>

                    <motion.button
                      whileHover={{ y: -2, scale: 1.02 }}
                      whileTap={{ scale: 0.98 }}
                      onClick={() => deleteAnswer(a.id)}
                      style={{ color: "red" }}
                    >
                      Delete
                    </motion.button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </motion.div>

      {/* ✅ EDIT CARD */}
      {editing && (
        <motion.div
          className="card"
          initial={{ opacity: 0, y: 18 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.45 }}
          style={{
            backgroundColor: "#f9f9f9",
            borderLeft: "4px solid #007bff",
          }}
        >
          <h2>Edit Model Answer</h2>

          <label>Question Title</label>
          <input
            value={editTitle}
            onChange={(e) => setEditTitle(e.target.value)}
          />

          <label>Model Answer</label>
          <textarea
            rows={6}
            value={editText}
            onChange={(e) => setEditText(e.target.value)}
          />

          <br />
          <br />

          <motion.button
            whileHover={{ y: -2, scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
            onClick={updateAnswer}
            style={{ marginRight: "5px" }}
          >
            Update Answer
          </motion.button>

          <motion.button
            whileHover={{ y: -2, scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
            onClick={cancelEdit}
            style={{ backgroundColor: "#6c757d" }}
          >
            Cancel
          </motion.button>
        </motion.div>
      )}
    </div>
  );
}
