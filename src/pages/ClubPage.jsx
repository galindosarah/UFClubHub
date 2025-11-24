import { useParams } from "react-router-dom";
import { useEffect, useState } from "react";

export default function ClubPage() {
  const { clubId } = useParams();
  const [club, setClub] = useState(null);

//   useEffect(() => {
//     fetch(`http://localhost:8000/api/clubs/${clubId}/`)
//       .then(res => res.json())
//       .then(data => setClub(data));
//   }, [clubId]);



  if (!club) return <p>Loading...</p>;


  return (
    <div>
      <h1>{club.name}</h1>
      <p>{club.bio}</p>

      <button onClick={handleJoinLeave}>
        {club.is_member ? "Leave Club" : "Join Club"}
      </button>
    </div>
  );
}