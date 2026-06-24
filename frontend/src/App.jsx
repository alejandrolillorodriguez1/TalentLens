import { useEffect, useState } from "react";
import axios from "axios";
import "./App.css"

function App() {
  const [role, setRole] = useState("user");

  const [offers, setOffers] = useState([]);
  const [selectedFiles, setSelectedFiles] = useState({});
  const [result, setResult] = useState(null);

  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");

  const [candidates, setCandidates] = useState([]);
   const API_URL = "http://127.0.0.1:8001";

  const loadOffers = async () => {
    try {
      const response = await axios.get(`${API_URL}/offers`);
      setOffers(response.data);
    } catch (error) {
      console.error("Error cargando ofertas:", error);
    }
  };

  const loadCandidates = async () => {
    try {
      const response = await axios.get(`${API_URL}/candidates`);
      setCandidates(response.data);
    } catch (error) {
      console.error("Error cargando candidatos:", error);
    }
  };

  useEffect(() => {
    loadOffers();
    loadCandidates();
  }, []);

  const handleFileChange = (offerId, file) => {
    setSelectedFiles({
      ...selectedFiles,
      [offerId]: file,
    });
  };

  const handleApply = async (offerId) => {
    const file = selectedFiles[offerId];

    if (!file) {
      alert("Selecciona un CV en PDF antes de aplicar.");
      return;
    }

    const formData = new FormData();
    formData.append("cv_file", file);

    try {
      const response = await axios.post(
        `${API_URL}/apply/${offerId}`,
        formData
      );

      setResult(response.data);
      await loadCandidates();
    } catch (error) {
      console.error("Error aplicando a la oferta:", error);
      alert("Ha ocurrido un error al enviar el CV.");
    }
  };

  const handleCreateOffer = async (e) => {
    e.preventDefault();

    if (!title || !description) {
      alert("Por favor, completa todos los campos.");
      return;
    }

    try {
      await axios.post(`${API_URL}/offers`, {
        offer_name : title,
        description
      });

      setTitle("");
      setDescription("");
      await loadOffers();
    } catch (error) {
      console.error("Error creando oferta:", error);
      alert("Error creando la oferta");
    }
  };

  return (
    <div className="app">
      <h1>TalentLens</h1>

      <button onClick={() => setRole("user")}>Usuario</button>
      <button onClick={() => setRole("admin")}>Admin</button>

      {role === "admin" && (
        <>
          <h2>Panel administrador</h2>

          <h3>Crear oferta</h3>

          <form onSubmit={handleCreateOffer}>
            <input
              type="text"
              placeholder="Título de la oferta"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
            />

            <textarea
              placeholder="Descripción de la oferta"
              value={description}
              onChange={(e) => setDescription(e.target.value)}
            />

            <button type="submit">Crear oferta</button>
          </form>

          <h3>Candidatos evaluados</h3>

          <table>
            <thead>
              <tr>
                <th>CV</th>
                <th>Oferta</th>
                <th>Score</th>
                <th>Decisión</th>
              </tr>
            </thead>

            <tbody>
              {candidates.map((candidate) => (
                <tr key={candidate.id}>
                  <td>{candidate.cv_name}</td>
                  <td>{candidate.offer_name}</td>
                  <td>{candidate.score}</td>
                  <td>{candidate.decision}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </>
      )}

      {role === "user" && (
        <>
          <h2>Ofertas disponibles</h2>

          {offers.map((offer) => (
            <div key={offer.id} className="offer-card">
              <h3>{offer.offer_name}</h3>
              <p>{offer.description}</p>

              <input
                type="file"
                accept="application/pdf"
                onChange={(e) =>
                  handleFileChange(offer.id, e.target.files[0])
                }
              />

              <button onClick={() => handleApply(offer.id)}>
                Aplicar a esta oferta
              </button>
            </div>
          ))}

          {result && (
            <div className="result">
              <h2>Resultado</h2>
              <p>Oferta: {result.offer_name}</p>
              <p>Score: {result.score}</p>
              <p>Decisión: {result.decision}</p>
              <h3>Skills del candidato</h3>
              <ul>
                {result.candidate_skills.map((skill, index) => (
                  <li key={index}>{skill}</li>
                ))}
              </ul>

              <h3>Skills requeridas</h3>
              <ul>
                {result.required_skills.map((skill, index) => (
                  <li key={index}>{skill}</li>
                ))}
              </ul>
            </div>
          )}
        </>
      )}
    </div>
  );
}

export default App;