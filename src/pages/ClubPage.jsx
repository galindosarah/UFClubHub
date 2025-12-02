import { useParams } from "react-router-dom";
import { useEffect, useState } from "react";
import "./ClubPage.css"

export default function ClubPage() {
    const { clubId } = useParams();
    const [club, setClub] = useState(null);

//   useEffect(() => {
//     fetch(`http://localhost:8000/api/clubs/${clubId}/`)
//       .then(res => res.json())
//       .then(data => setClub(data));
//   }, [clubId]);

    // const handleJoinLeave = () => {
    //     setClub(prev => ({
    //     ...prev,
    //     is_member: !prev.is_member  
    //     }));
    // };

    //Demo joining/leaving club with no backend yet
    const [isMember, setIsMember] = useState(false);
    const demoJoinLeave = () => {
        setIsMember((prev) => !prev);
    }

    if (!club) return (
        <div>
            <div className="header">
                <h1>Club Name</h1>
                <button 
                    className={isMember ? "leave-button" : "join-button"}
                    onClick={demoJoinLeave}
                >
                    {isMember ? "Leave Club" : "Join Club"}
                </button>
            </div>

            <div className="info-wrap">
                <h2>About</h2>
                <p> To educate all UF students on the animation industry and animation as an art form, to provide networking, 
                    job, learning, and other opportunities to all students, and bridge the gap between online and in-person 
                    students interested in animation.</p>
        

            </div>
        </div>
    );;


    return (
        <div>
            <h1>{club.name}</h1>
            <p>{club.bio}</p>

            <button 
                className={club.is_member ? "leave-button" : "join-button"}
                onClick={handleJoinLeave}
            >
                {club.is_member ? "Leave Club" : "Join Club"}
            </button>
        </div>
    );
}