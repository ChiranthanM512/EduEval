import React, { useState } from "react";
import API from "../api";
import logo from "../assets/logo.png";
import { motion, AnimatePresence } from "framer-motion";

export default function Login({ setLogged }) {
  const [user, setUser] = useState({ username: "", password: "" });
  const [mode, setMode] = useState("login");
  const [loading, setLoading] = useState(false);

  async function submit() {
    try {
      if (!user.username || !user.password) {
        alert("Please enter username and password");
        return;
      }

      setLoading(true);

      if (mode === "register") {
        await API.post("/auth/register", user);
        alert("Registered successfully! Now login.");
        setMode("login");
        return;
      }

      await API.post("/auth/login", user);
      setLogged(true);
    } catch (err) {
      alert(err?.response?.data?.detail || "Something went wrong");
    } finally {
      setLoading(false);
    }
  }

  // ✅ Enter key works because of form submit
  function handleSubmit(e) {
    e.preventDefault();
    if (!loading) submit();
  }

  return (
    <motion.div
      style={styles.page}
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.45 }}
    >
      {/* MAIN CARD */}
      <motion.div
        style={styles.card}
        initial={{ opacity: 0, y: 25, scale: 0.98 }}
        animate={{ opacity: 1, y: 0, scale: 1 }}
        transition={{ duration: 0.55, ease: "easeOut" }}
      >
        {/* LEFT SIDE */}
        <motion.div
          style={styles.left}
          initial={{ scale: 1.05 }}
          animate={{ scale: 1 }}
          transition={{ duration: 0.9, ease: "easeOut" }}
        >
          <div style={styles.overlay} />

          <motion.div
            style={styles.leftContent}
            initial={{ opacity: 0, y: 15 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.15, duration: 0.55 }}
          >
            <motion.img
              src={logo}
              alt="EduEvalve Logo"
              style={styles.logo}
              initial={{ opacity: 0, scale: 0.85 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ delay: 0.25, duration: 0.45 }}
            />

            <motion.h1
              style={styles.title}
              initial={{ opacity: 0, y: 12 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.3, duration: 0.45 }}
            >
              EduEval
            </motion.h1>

            <motion.p
              style={styles.subtitle}
              initial={{ opacity: 0, y: 12 }}
              animate={{ opacity: 0.9, y: 0 }}
              transition={{ delay: 0.38, duration: 0.45 }}
            >
              AI-powered Answer Sheet Evaluation <br />
              (Hybrid OCR + Semantic Scoring)
            </motion.p>
          </motion.div>
        </motion.div>

        {/* RIGHT SIDE */}
        <motion.div
          style={styles.right}
          initial={{ opacity: 0, x: 18 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.2, duration: 0.55 }}
        >
          {/* ✅ FORM (ENTER KEY WORKS) */}
          <form onSubmit={handleSubmit}>
            {/* Title Animation */}
            <AnimatePresence mode="wait">
              <motion.h2
                key={mode}
                style={styles.formTitle}
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -10 }}
                transition={{ duration: 0.25 }}
              >
                {mode === "login" ? "Login" : "Register"}
              </motion.h2>
            </AnimatePresence>

            <label style={styles.label}>Username</label>
            <motion.input
              style={styles.input}
              placeholder="Enter username"
              value={user.username}
              whileFocus={{ scale: 1.02 }}
              transition={{ duration: 0.15 }}
              onChange={(e) => setUser({ ...user, username: e.target.value })}
            />

            <label style={styles.label}>Password</label>
            <motion.input
              style={styles.input}
              type="password"
              placeholder="Enter password"
              value={user.password}
              whileFocus={{ scale: 1.02 }}
              transition={{ duration: 0.15 }}
              onChange={(e) => setUser({ ...user, password: e.target.value })}
            />

            <motion.button
              type="submit"
              style={{
                ...styles.button,
                opacity: loading ? 0.7 : 1,
                cursor: loading ? "not-allowed" : "pointer",
              }}
              disabled={loading}
              whileHover={!loading ? { y: -2, scale: 1.02 } : {}}
              whileTap={!loading ? { scale: 0.98 } : {}}
              transition={{ duration: 0.15 }}
            >
              {loading
                ? "Please wait..."
                : mode === "login"
                  ? "Login"
                  : "Register"}
            </motion.button>
          </form>

          {/* Switch text animation */}
          <AnimatePresence mode="wait">
            <motion.p
              key={mode + "-switch"}
              style={styles.switchText}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -10 }}
              transition={{ duration: 0.25 }}
            >
              {mode === "login" ? (
                <>
                  New user?{" "}
                  <span
                    style={styles.switchLink}
                    onClick={() => setMode("register")}
                  >
                    Register
                  </span>
                </>
              ) : (
                <>
                  Already have an account?{" "}
                  <span style={styles.switchLink} onClick={() => setMode("login")}>
                    Login
                  </span>
                </>
              )}
            </motion.p>
          </AnimatePresence>
        </motion.div>
      </motion.div>
    </motion.div>
  );
}

const styles = {
  page: {
    height: "100vh",
    width: "100%",
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
    background: "linear-gradient(120deg, #e0f2fe, #f8fafc)",
    padding: "20px",
  },

  card: {
    width: "950px",
    height: "520px",
    display: "grid",
    gridTemplateColumns: "1fr 1fr",
    borderRadius: "22px",
    overflow: "hidden",
    background: "#fff",
    boxShadow: "0px 15px 40px rgba(0,0,0,0.12)",
  },

  left: {
    position: "relative",
    backgroundImage:
      "url('https://images.unsplash.com/photo-1524995997946-a1c2e315a42f?auto=format&fit=crop&w=900&q=60')",
    backgroundSize: "cover",
    backgroundPosition: "center",
  },

  overlay: {
    position: "absolute",
    inset: 0,
    background: "rgba(0,0,0,0.55)",
  },

  leftContent: {
    position: "relative",
    zIndex: 2,
    height: "100%",
    padding: "40px",
    display: "flex",
    flexDirection: "column",
    justifyContent: "center",
    gap: "15px",
    color: "white",
  },

  logo: {
    width: "65px",
    height: "65px",
    objectFit: "contain",
    background: "white",
    padding: "8px",
    borderRadius: "14px",
  },

  title: {
    fontSize: "42px",
    margin: 0,
  },

  subtitle: {
    fontSize: "16px",
    lineHeight: "1.6",
    opacity: 0.9,
    margin: 0,
  },

  right: {
    padding: "50px",
    display: "flex",
    flexDirection: "column",
    justifyContent: "center",
    gap: "12px",
  },

  formTitle: {
    marginBottom: "10px",
    fontSize: "28px",
    fontWeight: "700",
  },

  label: {
    fontSize: "14px",
    fontWeight: "600",
    marginTop: "6px",
  },

  input: {
    width: "100%",
    padding: "12px",
    borderRadius: "10px",
    border: "1px solid #d1d5db",
    fontSize: "15px",
    outline: "none",
    marginBottom: "10px",
  },

  button: {
    width: "100%",
    marginTop: "10px",
    padding: "12px",
    borderRadius: "10px",
    border: "none",
    background: "#2563eb",
    color: "white",
    fontSize: "16px",
    fontWeight: "600",
  },

  switchText: {
    marginTop: "14px",
    fontSize: "14px",
  },

  switchLink: {
    color: "#2563eb",
    cursor: "pointer",
    fontWeight: "600",
  },
};
