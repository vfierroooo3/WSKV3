import { useNavigate } from "react-router-dom";
import "../components/css/Button.css"
import MainLayout from "../components/layout/MainLayout.jsx";
import { useState } from "react";
import sharedApi from "../components/api/api.js";

function CreateProjectPage() {
  const navigate = useNavigate();
  const [errorMessage, setErrorMessage] = useState("");
  // Create Project
  async function handleNewProject(event) {
    event.preventDefault();
    const formData = new FormData(event.target);
    const projectData = Object.fromEntries(formData);
    // Call API
     try{
      const result = await sharedApi("/create_project", "POST", {userId: localStorage.getItem("userId"),projectId: projectData.projectId, projectName: projectData.projectName, description: projectData.projectDescription});
      if (result.success) {
        navigate(`/main-page`);
      } else{
        setErrorMessage(result.message);
      }
     } catch (error) {
        setErrorMessage("An error occurred while creating the project.");
      }
    }


  return (
    <MainLayout>
      <div style={{ display: "flex", flexDirection: "column", alignItems: "center"}}>
        <h1>Create Project</h1>
        <form style={{ display: "flex", flexDirection: "column", gap: "12px", width: "300px"}} onSubmit={handleNewProject}>
          <div>
            <label>ID:</label>
            <br/>
            <input type="text" id="projectId" name="projectId" style={{width: "300px"}}/>
          </div>
          <div>
            <label>Name:</label>
            <br/>
            <input type="text" id="projectName" name="projectName" required style={{width: "300px"}} />
          </div>
          <div>
            <label>Description:</label>
            <br/>
            <textarea id="projectDescription" name="projectDescription" required style={{width: "300px", height: "100px"}} />
          </div>
          <button type="submit" className="custom-button">Create Project</button>
        </form>
      <span style={{ color: "red" }}>{errorMessage}</span>

      </div>
    </MainLayout>
  );
}

export default CreateProjectPage;