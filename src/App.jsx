import { useState } from 'react'
import { BrowserRouter, Routes, Route, Link, Navigate } from "react-router-dom";
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'

import Login from "./pages/Login.jsx";
import Explore from "./pages/Explore.jsx";
import Account from "./pages/Account.jsx";
import Clubs from "./pages/Clubs.jsx";
import ClubPage from './pages/ClubPage.jsx';
import ClubDashboard from './pages/ManageClub.jsx';
import MainLayout from './layouts/MainLayout.jsx';
import { AuthProvider } from './AuthContext.jsx';


export default function App() {
  //const { user } = useAuth();

  return (
    //<AuthProvider>
    <BrowserRouter>
      <Routes>
        {/* First load → go to Login */}
        <Route path="/" element={<Navigate to="/login" replace />} />

        {/* Public (no navbar) */}
        <Route path="/login" element={<Login />} />

        {/* App pages (with navbar) */}
        <Route element={<MainLayout />}>
          <Route path="/explore" element={<Explore />} />
          <Route path="/clubs" element={<Clubs />} />
          <Route path="/account" element={<Account />} />
          {/* <Route path="/clubs/:clubId" element={<ClubPage/>} /> */}
          <Route path="/clubs/demo" element={<ClubPage/>} />
        </Route>

        {/* Fallback
        <Route path="*" element={<Navigate to="/login" replace />} /> */}
      </Routes>
    </BrowserRouter>
    //<AuthProvider/>
  );
}