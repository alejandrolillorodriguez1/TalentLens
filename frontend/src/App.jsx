import { useEffect, useState } from "react";
import axios from "axios";

function App() {
  const [offers, setOffers] = useState([]);
  const [selectedFiles, setSelectedFiles] = useState({});
  const [result, setResult] = useState(null);
  const [title,setTitle] = useState("");
  const [description,setDescription] = useState("");

  useEffect(() => {
    axios
      .get("http://127.0.0.1:8000/offers")
      .then((response) => {
        setOffers(response.data);
      })
      .catch((error) => {
        console.error("Error cargando ofertas:", error);
      });
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
        `http://127.0.0.1:8000/apply/${offerId}`,
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        }
      );

      setResult(response.data);
    } catch (error) {
      console.error("Error aplicando a la oferta:", error);
      alert("Ha ocurrido un error al enviar el CV.");
    }
  };

  const handleCreateOffer = async (e) => {
    e.preventDefault();
    if (!title || !description) {
      alert("Por favor, completa todos los campos para crear una oferta.");
      return;
    }
    
    try {
      await axios.post("http://127.0.0.1:8000/offers",{
        title : title,
        description : description
      });
      setTitle("");
      setDescription("");
      const response = await axios.get("http://127.0.0.1:8000/offers")
      setOffers(response.data);
    }catch(error){
      console.error("Error creando oferta:", error);
      alert("Error creando la oferta");
    }
  }
    

  return (
    <div>
      <h1>TalentLens</h1>
      
      <h2>Crear oferta</h2>

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

      <h2>Ofertas disponibles</h2>

      {offers.map((offer) => (
        <div key={offer.id}>
          <h3>{offer.title}</h3>
          <p>{offer.description}</p>

          <input
            type="file"
            accept="application/pdf"
            onChange={(e) => handleFileChange(offer.id, e.target.files[0])}
          />

          <button onClick={() => handleApply(offer.id)}>
            Aplicar a esta oferta
          </button>
        </div>
      ))}

      {result && (
        <div>
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
    </div>
  );
}

export default App;