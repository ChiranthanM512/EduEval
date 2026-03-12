import React from "react";
import { motion } from "framer-motion";
import logo from "../assets/image5.png";

export default function Navbar({ setLogged, page, setPage }) {
  function NavBtn({ id, label }) {
    const active = page === id;

    return (
      <motion.button
        onClick={() => setPage(id)}
        whileHover={{ y: -2, scale: 1.03 }}
        whileTap={{ scale: 0.97 }}
        style={{
          background: active ? "#2563eb" : "#374151",
          transition: "0.2s",
        }}
      >
        {label}
      </motion.button>
    );
  }

  return (
    <motion.div
      className="navbar"
      initial={{ opacity: 0, y: -15 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.45 }}
    >
      {/* LEFT SIDE BRAND */}
      <motion.div
        style={{
          display: "flex",
          alignItems: "center",
          gap: "10px",
          fontWeight: "bold",
          fontSize: "18px",
        }}
        initial={{ opacity: 0, x: -15 }}
        animate={{ opacity: 1, x: 0 }}
        transition={{ delay: 0.1, duration: 0.45 }}
      >
        <motion.img
          src={logo}
          alt="EduEvalve Logo"
          style={{
            width: "34px",
            height: "34px",
            objectFit: "contain",
            borderRadius: "10px",
            background: "white",
            padding: "5px",
          }}
          initial={{ scale: 0.7, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          transition={{ delay: 0.2, duration: 0.4 }}
        />

        <span>EduEval</span>
      </motion.div>

      {/* RIGHT SIDE BUTTONS */}
      <motion.div
        className="links"
        initial={{ opacity: 0, x: 15 }}
        animate={{ opacity: 1, x: 0 }}
        transition={{ delay: 0.15, duration: 0.45 }}
      >
        <NavBtn id="dashboard" label="Dashboard" />
        <NavBtn id="model" label="Model Answers" />
        <NavBtn id="upload" label="Upload & Evaluate" />
        <NavBtn id="results" label="Results" />

        <motion.button
          onClick={() => setLogged(false)}
          whileHover={{ y: -2, scale: 1.03 }}
          whileTap={{ scale: 0.97 }}
          style={{
            background: "#ef4444",
            transition: "0.2s",
          }}
        >
          Logout
        </motion.button>
      </motion.div>
    </motion.div>
  );
}
