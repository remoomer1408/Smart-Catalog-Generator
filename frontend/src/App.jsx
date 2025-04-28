import React, { useState } from 'react';

function App() {
  const [file, setFile] = useState(null);
  const [response, setResponse] = useState(null);
  const [loading, setLoading] = useState(false);

  // Handle file change (when user selects a file)
  const handleFileChange = (event) => {
    const uploadedFile = event.target.files[0];
    if (uploadedFile) {
      setFile(uploadedFile);
    }
  };

  // Handle form submission to send the file to backend
  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) {
      alert('Please select a CSV file');
      return;
    }

    setLoading(true);

    const formData = new FormData();
    formData.append('file', file);

    try {
      const res = await fetch('http://localhost:8000/generate-catalog/', {
        method: 'POST',
        body: formData,
      });

      if (res.ok) {
        const data = await res.json();
        setResponse(data.data);
      } else {
        alert('Error uploading file. Please try again.');
      }
    } catch (error) {
      console.error('Error:', error);
      alert('There was an error processing your request.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-3xl font-bold text-center">Smart Catalog Generator</h1>

      {/* File Upload Form */}
      <form onSubmit={handleSubmit} className="my-6">
        <input
          type="file"
          accept=".csv"
          onChange={handleFileChange}
          className="border-2 border-gray-300 p-2 rounded-md"
        />
        <button
          type="submit"
          className="bg-blue-500 text-white py-2 px-4 rounded-md ml-4"
          disabled={loading}
        >
          {loading ? 'Generating...' : 'Upload & Generate'}
        </button>
      </form>

      {/* Displaying the generated catalog data */}
      {response && (
        <div>
          <h2 className="text-2xl font-semibold mb-4">Generated Catalog</h2>
          <table className="table-auto w-full border-collapse border border-gray-300">
            <thead>
              <tr>
                <th className="border border-gray-300 px-4 py-2">Product Name</th>
                <th className="border border-gray-300 px-4 py-2">Title</th>
                <th className="border border-gray-300 px-4 py-2">Description</th>
                <th className="border border-gray-300 px-4 py-2">Features</th>
              </tr>
            </thead>
            <tbody>
              {response.map((item, index) => (
                <tr key={index}>
                  <td className="border border-gray-300 px-4 py-2">{item.product_name}</td>
                  <td className="border border-gray-300 px-4 py-2">{item.title}</td>
                  <td className="border border-gray-300 px-4 py-2">{item.description}</td>
                  <td className="border border-gray-300 px-4 py-2">
                    <ul>
                      {item.features.map((feature, idx) => (
                        <li key={idx}>{feature}</li>
                      ))}
                    </ul>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}

export default App;
