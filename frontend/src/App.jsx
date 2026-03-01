import { useState } from 'react';

function App() {
  const [file, setFile] = useState(null);
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
    setResults(null);
    setError(null);
  };

  const handleScan = async () => {
    if (!file) return;

    setLoading(true);
    setError(null);
    
    const formData = new FormData();
    formData.append('file', file);

    try {
      // Send the file to your FastAPI backend
      const response = await fetch('http://127.0.0.1:8000/scan/terraform/', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) throw new Error('Failed to scan file. Check the backend.');

      const data = await response.json();
      setResults(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen p-8 text-gray-800 font-sans">
      <div className="max-w-4xl mx-auto space-y-8">
        
        {/* Header */}
        <header className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
          <h1 className="text-3xl font-bold text-gray-900">IaC Security Command Center</h1>
          <p className="text-gray-500 mt-2">Upload your Terraform files for automated vulnerability analysis.</p>
        </header>

        {/* Upload Section */}
        <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200 flex items-center space-x-4">
          <input 
            type="file" 
            accept=".tf" 
            onChange={handleFileChange}
            className="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100 cursor-pointer"
          />
          <button 
            onClick={handleScan} 
            disabled={!file || loading}
            className="bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-6 rounded-md transition-colors disabled:opacity-50"
          >
            {loading ? 'Scanning...' : 'Run Scan'}
          </button>
        </div>

        {/* Error State */}
        {error && (
          <div className="bg-red-50 border-l-4 border-red-500 p-4 text-red-700">
            <p className="font-bold">Error</p>
            <p>{error}</p>
          </div>
        )}

        {/* Results Section */}
        {results && (
          <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
            <h2 className="text-xl font-bold mb-4">Scan Results: {results.filename}</h2>
            
            {results.vulnerabilities_found === 0 ? (
              <div className="bg-green-50 text-green-700 p-4 rounded-md">
                ✅ No vulnerabilities found. Infrastructure is secure.
              </div>
            ) : (
              <div className="space-y-4">
                <div className="bg-red-50 text-red-700 p-4 rounded-md font-bold">
                  🚨 {results.vulnerabilities_found} Vulnerabilities Detected
                </div>
                
                <div className="grid gap-4">
                  {results.details.map((vuln, index) => (
                    <div key={index} className="border border-gray-200 rounded-md p-4 flex justify-between items-start">
                      <div>
                        <p className="font-bold text-gray-900">{vuln.resource}</p>
                        <p className="text-sm text-gray-500 font-mono mb-2">{vuln.type}</p>
                        <p className="text-gray-700">{vuln.issue}</p>
                      </div>
                      <span className={`px-3 py-1 rounded-full text-xs font-bold ${
                        vuln.severity === 'CRITICAL' ? 'bg-red-100 text-red-800' : 'bg-orange-100 text-orange-800'
                      }`}>
                        {vuln.severity}
                      </span>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}

      </div>
    </div>
  );
}

export default App;