import { Link, useLocation } from "react-router-dom";
import { useAuth } from "../AuthContext";
import "./NavBar.css";

export default function NavBar() {
  const { pathname } = useLocation();
  // const { userType } = useAuth();
  return (
    <header className="navbar">
      <nav className="navbar__inner">

        {/* LEFT SIDE — logo placeholder */}
        <div className="navbar__left">
          <div className="logo-placeholder">OneSPOT</div>
        </div>

        {/* RIGHT SIDE — nav links */}
        <div className="navbar__right">
          <Link
            to="/explore"
            aria-current={pathname === "/explore" ? "page" : undefined}
          >
            Explore
          </Link>
          
          <Link
            to="/clubs"
            aria-current={pathname === "/clubs" ? "page" : undefined}
          >
            My Clubs
          </Link>

          <Link
            to="/account"
            aria-current={pathname === "/account" ? "page" : undefined}
          >
            My Account
          </Link>
        </div>


      {/* <div className="navbar__right">
        {userType === "regular" && (
          <>
            <Link to="/explore" aria-current={pathname === "/explore" ? "page" : undefined}>
              Explore
            </Link>
          
            <Link to="/clubs" aria-current={pathname === "/clubs" ? "page" : undefined}>
              My Clubs
            </Link>

            <Link to="/account" aria-current={pathname === "/account" ? "page" : undefined}>
              My Account
            </Link>
          </>
        )}

        {userType === "club" && (
          <>
            <Link to="/explore" aria-current={pathname === "/explore" ? "page" : undefined}>
              Manage Club
            </Link>         

            <Link to="/account" aria-current={pathname === "/account" ? "page" : undefined}>
              My Account
            </Link>
          </>
        )}
      </div> */}

      </nav>
    </header>
  );
}