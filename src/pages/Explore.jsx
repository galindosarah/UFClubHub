import React, { useState } from 'react';
import SearchBar from "../components/SearchBar";

export default function Explore() {
  const [results, setResults] = useState([]);

  /* function to fetch results from backend */
  const fetchResults = (query = "") => {

  }

  /* show all results by default */
  // useEffect(() => {
  //   fetchResults();
  // }, []);

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
              <div key={index}>
                {item.name}
              </div>
            ))
            ) : (
              <p>No results found.</p>
            )}
          
        </div>
    </div>
  );
}