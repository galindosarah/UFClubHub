import { useState } from 'react'
import { BrowserRouter, Routes, Route, Link, Navigate } from "react-router-dom";
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'

import Login from "./pages/Login.jsx";
import Explore from "./pages/Explore.jsx";
import Account from "./pages/Account.jsx";
import MainLayout from './layouts/MainLayout.jsx';


export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* First load → go to Login */}
        <Route path="/" element={<Navigate to="/login" replace />} />

        {/* Public (no navbar) */}
        <Route path="/login" element={<Login />} />

        {/* App pages (with navbar) */}
        <Route element={<MainLayout />}>
          <Route path="/explore" element={<Explore />} />
          <Route path="/account" element={<Account />} />
        </Route>

        {/* Fallback
        <Route path="*" element={<Navigate to="/login" replace />} /> */}
      </Routes>
    </BrowserRouter>
  );
}