import React, { useEffect, useMemo, useState } from "react";
import { motion } from "framer-motion";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid,
} from "recharts";

import eduImg from "../assets/image1.png";

import api from "../api";
import "../styles.css";

function clamp(n, a, b) {
  return Math.max(a, Math.min(b, n));
}

function formatScore(n) {
  if (n === null || n === undefined || Number.isNaN(Number(n))) return "--";
  return Number(n).toFixed(2);
}

function scoreColor(score) {
  if (score >= 85) return "pill green";
  if (score >= 65) return "pill orange";
  return "pill red";
}

function AnimatedNumber({ value }) {
  const [display, setDisplay] = useState(0);

  useEffect(() => {
    let start = 0;
    const end = Number(value || 0);
    const duration = 700;
    const startTime = performance.now();

    function tick(now) {
      const t = clamp((now - startTime) / duration, 0, 1);
      const eased = 1 - Math.pow(1 - t, 3);
      const current = start + (end - start) * eased;
      setDisplay(current);

      if (t < 1) requestAnimationFrame(tick);
    }

    requestAnimationFrame(tick);
  }, [value]);

  return <span>{display.toFixed(0)}</span>;
}

export default function Dashboard() {
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(true);

  async function loadResults() {
    try {
      setLoading(true);
      const res = await api.get("/results/");
      setResults(res.data || []);
    } catch (err) {
      console.error("Dashboard results fetch error:", err);
      setResults([]);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadResults();
  }, []);

  // Stats
  const stats = useMemo(() => {
    if (!results.length) {
      return {
        total: 0,
        avg: 0,
        best: 0,
        last: 0,
        recent: [],
        trend: [],
      };
    }

    const sorted = [...results].sort((a, b) => (b.id || 0) - (a.id || 0));
    const scores = results.map((r) => Number(r.score || 0));

    const total = results.length;
    const avg = scores.reduce((s, x) => s + x, 0) / total;
    const best = Math.max(...scores);
    const last = Number(sorted[0]?.score || 0);

    const recent = sorted.slice(0, 6);

    // last 10 evaluations for trend
    const last10 = sorted.slice(0, 10).reverse();
    const trend = last10.map((r, idx) => ({
      name: `#${r.id || idx + 1}`,
      score: Number(r.score || 0),
    }));

    return { total, avg, best, last, recent, trend };
  }, [results]);

  const avgProgress = clamp(stats.avg, 0, 100);

  return (
    <div className="dashWrap">
      {/* HERO */}
      <motion.div
        className="dashHero"
        initial={{ opacity: 0, y: 18 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <div className="dashHeroLeft">
          <h1 className="dashTitle">Hi! Welcome to EduEval 📘</h1>
          <p className="dashSubtitle">
            Track evaluations, view score trends, and monitor student progress in
            one place.
          </p>

          <div className="dashHeroButtons">
            <button className="btnPrimary" onClick={loadResults}>
              Refresh Dashboard
            </button>
          </div>
        </div>

        <div className="dashHeroRight">
          <img
            className="dashHeroImg"
            alt="Education illustration"
            src={eduImg}

          />
        </div>
      </motion.div>

      {/* STAT CARDS */}
      <div className="dashGrid4">
        <motion.div
          className="statCard"
          whileHover={{ y: -6 }}
          transition={{ duration: 0.2 }}
        >
          <div className="statTop">
            <div className="statIcon">📄</div>
            <div className="statLabel">Total Evaluations</div>
          </div>
          <div className="statValue">
            {loading ? "..." : <AnimatedNumber value={stats.total} />}
          </div>
        </motion.div>

        <motion.div
          className="statCard"
          whileHover={{ y: -6 }}
          transition={{ duration: 0.2 }}
        >
          <div className="statTop">
            <div className="statIcon">📊</div>
            <div className="statLabel">Average Score</div>
          </div>
          <div className="statValue">
            {loading ? "..." : `${formatScore(stats.avg)}%`}
          </div>
          <div className="progressWrap">
            <div className="progressBar">
              <div
                className="progressFill"
                style={{ width: `${avgProgress}%` }}
              />
            </div>
            <div className="progressText">{avgProgress.toFixed(0)}%</div>
          </div>
        </motion.div>

        <motion.div
          className="statCard"
          whileHover={{ y: -6 }}
          transition={{ duration: 0.2 }}
        >
          <div className="statTop">
            <div className="statIcon">🏆</div>
            <div className="statLabel">Best Score</div>
          </div>
          <div className="statValue">
            {loading ? "..." : `${formatScore(stats.best)}%`}
          </div>
        </motion.div>

        <motion.div
          className="statCard"
          whileHover={{ y: -6 }}
          transition={{ duration: 0.2 }}
        >
          <div className="statTop">
            <div className="statIcon">⏱️</div>
            <div className="statLabel">Last Score</div>
          </div>
          <div className="statValue">
            {loading ? "..." : `${formatScore(stats.last)}%`}
          </div>
        </motion.div>
      </div>

      {/* GRID 2 */}
      <div className="dashGrid2">
        {/* CHART */}
        <motion.div
          className="panel"
          initial={{ opacity: 0, y: 14 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.45, delay: 0.05 }}
        >
          <div className="panelHeader">
            <h2>Score Trend</h2>
            <span className="panelHint">Last 10 evaluations</span>
          </div>

          <div className="chartBox">
            {stats.trend.length === 0 ? (
              <div className="emptyState">
                No evaluations yet. Upload and evaluate to see trends.
              </div>
            ) : (
              <ResponsiveContainer width="100%" height={260}>
                <LineChart data={stats.trend}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="name" />
                  <YAxis domain={[0, 100]} />
                  <Tooltip />
                  <Line
                    type="monotone"
                    dataKey="score"
                    strokeWidth={3}
                    dot={{ r: 4 }}
                  />
                </LineChart>
              </ResponsiveContainer>
            )}
          </div>
        </motion.div>

        {/* RECENT TABLE */}
        <motion.div
          className="panel"
          initial={{ opacity: 0, y: 14 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.45, delay: 0.1 }}
        >
          <div className="panelHeader">
            <h2>Recent Evaluations</h2>
            <span className="panelHint">Latest 6 results</span>
          </div>

          <div className="tableWrap">
            <table className="miniTable">
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Score</th>
                  <th>Language</th>
                  <th>OCR</th>
                </tr>
              </thead>
              <tbody>
                {stats.recent.length === 0 ? (
                  <tr>
                    <td colSpan="4" className="emptyCell">
                      No data yet.
                    </td>
                  </tr>
                ) : (
                  stats.recent.map((r) => (
                    <tr key={r.id}>
                      <td>{r.id}</td>
                      <td>
                        <span className={scoreColor(Number(r.score || 0))}>
                          {formatScore(r.score)}%
                        </span>
                      </td>
                      <td>{r.language || "unknown"}</td>
                      <td>{r.ocr_engine || "--"}</td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        </motion.div>
      </div>

      
    </div>
  );
}
