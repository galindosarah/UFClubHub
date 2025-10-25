import React, { useState } from 'react';
import "./SearchBar.css";

const SearchBar = ({ onSearch }) => {
    const [query, setQuery] = useState("");

    const handleChange = (event) => {
        const value = event.target.value;
        setQuery(value);
        onSearch(value);
    }

    return (
            <div className="searchBar">
                <input 
                    type="text" 
                    placeholder="Search..." 
                    value={query}
                    onChange={handleChange}
                    />
            </div>
        
    );
}

export default SearchBar;