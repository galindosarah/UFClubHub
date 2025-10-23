import { Link, useLocation } from "react-router-dom";
import "./NavBar.css";

export default function NavBar() {
  const { pathname } = useLocation();
  return (
    // <header style={{ padding: 12 }}>
    //   <nav style={{ display: "flex", gap: 12 }}>
    <header className="navbar">
      <nav className="navbar__inner">
        {/* Add more links as you add more pages */}
        <Link to="/explore" aria-current={pathname === "/explore" ? "page" : undefined}>
          Explore
        </Link>
        <Link to="/account" aria-current={pathname === "/account" ? "page" : undefined}>
          My Account
        </Link>
      </nav>
    </header>
  );
}
