import React, { useState, useEffect } from 'react';
import SearchBar from "../components/SearchBar";
import { Link } from "react-router-dom";
import "./Explore.css"

export default function Explore() {
  const [results, setResults] = useState([]);

  /* function to fetch results from backend */
  const fetchResults = async (query = "") => {
  try {
    const response = await fetch(`http://localhost:8000/api/search/?q=${query}`);
    const data = await response.json();

    setResults(data);
  } catch (err) {
    console.error("Failed to fetch clubs:", err);
  }
};

useEffect(() => {
    fetchResults();
  }, []);


  const handleSearch = (query) => {
    fetchResults(query);
  }
  
  return (

    <div>
  
        <h1>Explore</h1>
        
        <div>
          <SearchBar onSearch={handleSearch}/>
        </div>

        <div className="results">
          {results.length > 0 ? 
            (results.map((item, index) => (
              <Link key={item.club_name} 
                //to={`/clubs/${item.id}`} 
                to={`/clubs/demo`}
                className='club-link'>
                <div  
                    className="club-card">
                  <h2 className="club-name">{item.club_name}</h2>
                  <p className="club-bio">{item.category}</p>
                </div>
              </Link>
            ))
            ) : (
              <p>No results found.</p>
            )}
          
        </div>
    </div>
  );
}