import { useNavigate } from "react-router-dom";
import "../components/css/Button.css"
import MainLayout from "../components/layout/MainLayout.jsx";

function JoinProjectPage() {
  const navigate = useNavigate();

  // Create Project
  function handleNewProject(event) {
    event.preventDefault();
    const formData = new FormData(event.target);
    const projectData = Object.fromEntries(formData);
    // Call API
    const successfulCreation = true; // Simulate API call
    if (successfulCreation) {
      navigate(`/main-page`);
    }else{
      document.getElementById("error-message").innerText = "ID is not correct!";
    }
  }

  return (
    <MainLayout>
      <div style={{ display: "flex", flexDirection: "column", alignItems: "center"}}>
        <h1>Join Project</h1>
        <form style={{ display: "flex", flexDirection: "column", gap: "12px", width: "300px"}} onSubmit={handleNewProject}>
            <label>Existing Project ID:</label>
            <input type="text" id="projectId" name="projectId" style={{width: "300px"}}/>
            <button type="submit" className="custom-button">Join Project</button>
        </form>
        <span id="error-message" style={{ color: "red" }}></span>
      </div>
    </MainLayout>
  );
}

export default JoinProjectPage;