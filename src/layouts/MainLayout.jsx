import { Outlet } from "react-router-dom";
import NavBar from "../components/NavBar.jsx";

export default function MainLayout() {
  return (
    <>
      <NavBar />
      <main style={{ padding: 12 }}>
        <Outlet />
      </main>
    </>
  );
}