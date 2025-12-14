import { useState } from "react";

const BACKEND_URL = "https://ai-photo-personalisation.onrender.com";

function App() {
  const [file, setFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleFileChange = (e) => {
    const selected = e.target.files[0];
    setFile(selected);
    setPreview(URL.createObjectURL(selected));
    setResult(null);
  };

  const handleGenerate = async () => {
    if (!file) {
      alert("Please upload an image");
      return;
    }

    setLoading(true);

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch(
        `${BACKEND_URL}/generate`,
        {
          method: "POST",
          body: formData,
        }
      );

      const data = await response.json();

      setResult(`${BACKEND_URL}/${data.image_path}`);
    } catch (err) {
      alert("Something went wrong");
    }

    setLoading(false);
  };

  return (
    <div style={{ padding: "40px", fontFamily: "Arial" }}>
      <h2>AI Personalisation</h2>

      <input type="file" accept="image/*" onChange={handleFileChange} />

      {preview && (
        <div style={{ marginTop: "20px" }}>
          <p>Uploaded Image:</p>
          <img src={preview} width="200" />
        </div>
      )}

      <div style={{ marginTop: "20px" }}>
        <button onClick={handleGenerate} disabled={loading}>
          {loading ? "Generating..." : "Generate Personalised Illustration"}
        </button>
      </div>

      {result && (
        <div style={{ marginTop: "30px" }}>
          <p>Result:</p>
          <img src={result} width="300" />
        </div>
      )}
    </div>
  );
}

export default App;
