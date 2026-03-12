import React, { useState } from "react";

import Login from "./components/Login";
import Navbar from "./components/Navbar";
import Dashboard from "./components/Dashboard";
import UploadPage from "./components/UploadPage";
import ResultsTable from "./components/ResultsTable";
import ModelAnswerPage from "./components/ModelAnswerPage";

import "./styles.css";

export default function App() {
  const [logged, setLogged] = useState(false);
  const [page, setPage] = useState("dashboard");

  if (!logged) return <Login setLogged={setLogged} />;

  return (
    <>
      <Navbar setLogged={setLogged} setPage={setPage} />

      {page === "dashboard" && <Dashboard />}
      {page === "model" && <ModelAnswerPage />}
      {page === "upload" && <UploadPage />}
      {page === "results" && <ResultsTable />}
    </>
  );
}
