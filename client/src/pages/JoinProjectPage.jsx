import { useNavigate } from "react-router-dom";
import "../components/css/Button.css"
import MainLayout from "../components/layout/MainLayout.jsx";
import sharedApi from "../components/api/api";
import { useState } from "react";

function JoinProjectPage() {
  const navigate = useNavigate();
  const [errorMessage, setErrorMessage] = useState("");

  // Create Project
  async function handleNewProject(event) {
    event.preventDefault();
    const formData = new FormData(event.target);
    const projectData = Object.fromEntries(formData);
    // Call API
    
    try {
      const result = await sharedApi("/join_project", "POST", {userId: localStorage.getItem("userId"), projectId: projectData.projectId});
      if (result.success) {
        navigate(`/main-page`);
      }else{
        setErrorMessage(result.message);
      }
    } catch (error) {
      console.error("Error during project join:", error);
      setErrorMessage("An error occurred during project join. Please try again.");
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
        <span style={{ color: "red" }}>{errorMessage}</span>
      </div>
    </MainLayout>
  );
}

export default JoinProjectPage;