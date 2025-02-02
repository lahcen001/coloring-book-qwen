import { useState } from 'react';
import './App.css';

function App() {
  const [promptText, setPromptText] = useState('');
  const [generatedImage, setGeneratedImage] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  const handlePromptChange = (event) => {
    setPromptText(event.target.value);
  };

  const generateColoringPage = async () => {
    if (!promptText.trim()) {
      setError('Please enter a prompt.');
      return;
    }

    setIsLoading(true);
    setError(null);

    try {
      const response = await fetch('http://127.0.0.1:5001/generate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ prompt: promptText }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        setError(errorData.error || 'Failed to generate image.');
        setIsLoading(false);
        return;
      }

      const data = await response.json();
      setGeneratedImage(data.image);
    } catch (err) {
      setError(`An error occurred: ${err.message}`);
    } finally {
      setIsLoading(false);
    }
  };

  const downloadImage = () => {
    if (!generatedImage) return;

    const link = document.createElement('a');
    link.download = 'coloring-page.png';
    link.href = generatedImage;
    link.click();
  };

  return (
    <div className="App">
      <h1>Coloring Book Generator</h1>
      
      <div className="prompt-section">
        <input
          type="text"
          placeholder="Enter your prompt here"
          value={promptText}
          onChange={handlePromptChange}
        />
        <button onClick={generateColoringPage} disabled={isLoading}>
          {isLoading ? 'Generating...' : 'Generate Coloring Page'}
        </button>
      </div>
      
      {error && <p className="error">{error}</p>}

      {generatedImage && (
        <div className="image-container">
          <img src={generatedImage} alt="Generated Coloring Page" />
          <button onClick={downloadImage}>Download Image</button>
        </div>
      )}
    </div>
  );
}

export default App;
