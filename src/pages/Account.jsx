import { useNavigate } from "react-router-dom";
import "./Account.css"

export default function Account() {
  const navigate = useNavigate();

  const goToStart = () => {
    navigate("/login");
  };

  return ( 
  <div> 
    <div className="header">
      <h1>My Account</h1>
      <button onClick={goToStart} className="logout-button">Logout</button>
    </div>
    
    <div className="profile-wrap">
      <p>Email: </p>
      

    </div>
    
    

   </div>
  );
}