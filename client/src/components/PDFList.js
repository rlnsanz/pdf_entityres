import React, { useState, useEffect } from 'react';

function PDFList({ onSelect }) {
  const [pdfFiles, setPdfFiles] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  // Fetch PDF files from the server
  useEffect(() => {
    setIsLoading(true);
    fetch('/api/pdf-list')
      .then(response => response.json())
      .then(data => {
        setPdfFiles(data);
        setIsLoading(false);
      })
      .catch(error => {
        console.error('Error fetching PDF files:', error);
        setError(error);
        setIsLoading(false);
      });
  }, []);

  // Render PDF list
  return (
    <div className="pdf-list">
      <h2>Available PDFs</h2>
      {isLoading ? (
        <p>Loading...</p>
      ) : error ? (
        <p>Error loading PDFs!</p>
      ) : (
        <ul>
          {pdfFiles.map(pdf => (
            <li key={pdf.name} onClick={() => onSelect(pdf)}>
              {pdf.name}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

export default PDFList;
