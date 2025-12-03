import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import "./Account.css"

export default function Account() {
  const navigate = useNavigate();
  const [user, setUser] = useState(null);

  useEffect(() => {
    // Get info of current user
    const storedUser = localStorage.getItem("user");
    if (storedUser) {
      setUser(JSON.parse(storedUser));
    } else {
      // No user logged in, redirect to login
      navigate("/login", { replace: true });
    }
  }, [navigate]);

  const goToStart = () => {
    // Clear user from localStorage on logout
    localStorage.removeItem("user");
    navigate("/login");
  };

  return ( 
    <div> 
      <div className="header">
        <h1>My Account</h1>
        <button onClick={goToStart} className="logout-button">Logout</button>
      </div>
      
      {/* Display email and account type */}
      <div className="profile-wrap">
        <p>Email: {user?.email}</p>
        <p>Account type: {user?.type === "club" ? "Club Account" : "User Account"}</p>
      </div>
    </div>
  );
}
