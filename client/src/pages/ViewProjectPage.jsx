import { useEffect, useState } from "react";
import { useLocation } from "react-router-dom";
import sharedApi from "../components/api/api";
import MainLayout from "../components/layout/MainLayout.jsx";
import NavigateButton from "../components/button/NavigateButton.jsx";
import "../components/css/Table.css";
function ViewProjectPage() {
  const location = useLocation();
  const projectId = location.state?.projectId;

  const [projectInfo, setProjectInfo] = useState({
    projectId: projectId,
    projectName: "",
    projectDescription: "",
    hardware: [],
  });
  
  // Get my projects List
  async function getProjectsInfo(projectId){
    try {
      const result = await sharedApi("/get_project_info", "POST", { projectId });
      if (result.success) {
        setProjectInfo({
          projectId: result.project.projectId,
          projectName: result.project.projectName,
          projectDescription: result.project.description,
          hardware: result.project.hwSets,
        });
      }
    } catch (error) {
      console.error("Error during get project info:", error);
    }
  }
  
  useEffect(() => {
    getProjectsInfo(projectId);
  }, [projectId]);
  
  return (
    <MainLayout>
      <div style={{display: "flex", flexDirection: "column", alignItems: "center"}}>
        <div style={{width: "30%"}}>
          <h1>Project Overview</h1>
          <table className="view-table">
            <tbody>
              <tr>
                <td className="view-table-header">Project ID</td>
                <td className="view-table-header">Project Name</td>
                <td className="view-table-header">Project Description</td>
              </tr>
              <tr>
                <td className="view-table-cell">{projectInfo.projectId}</td>
                <td className="view-table-cell">{projectInfo.projectName}</td>
                <td className="view-table-cell">{projectInfo.projectDescription}</td>
              </tr>
            </tbody>
          </table>
          <br/>
          <h1>Current Resources</h1>
          <table className="view-table">
            <tbody>
              <tr>
                <td className="view-table-header">Hardware Name</td>
                <td className="view-table-header">Current Rented</td>
              </tr>
              {Object.entries(projectInfo.hardware).map(([hardwareName, currentRent]) => (
                <tr key={hardwareName}>

                  <td className="view-table-cell">
                    {hardwareName}
                  </td>

                  <td className="view-table-cell">
                    {currentRent}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
          <br/>
          <div className="button-container">
            <NavigateButton 
              text="Check Out" 
              destination="/check-out" 
              data={{
                projectId: projectInfo.projectId, 
                projectName: projectInfo.projectName
              }}
            />
            <NavigateButton 
              text="Check In" 
              destination="/check-in" 
              data={{
                projectId: projectInfo.projectId, 
                projectName: projectInfo.projectName,
                hardware: projectInfo.hardware
              }}
            />
          </div>
        </div>
      </div>
    </MainLayout>
  );
}

export default ViewProjectPage;