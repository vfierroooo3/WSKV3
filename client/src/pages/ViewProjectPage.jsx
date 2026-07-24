import { useEffect, useState } from "react";
import { useLocation } from "react-router-dom";
import MainLayout from "../components/layout/MainLayout.jsx";
import NavigateButton from "../components/button/NavigateButton.jsx"
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
  function getProjectsInfo(projectId){
    // Simulate API call
    const result = {
      projectId: projectId,
      projectName: "ABC",
      projectDescription: "XXXX",
      hardware: [
        {
          hardwareId: 1,
          hardwareName: "Boeing 777F",
          currentRent: 0,
        },
        {
          hardwareId: 2,
          hardwareName: "Bell 206",
          currentRent: 0,
        },
      ],
    };
    // put the result into state
    setProjectInfo(result);
  }
  
  useEffect(() => {
    getProjectsInfo(projectId);
  }, [projectId]);
  
  return (
    <MainLayout>
      <div style={{display: "flex", flexDirection: "column", alignItems: "center"}}>
        <div>
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
          <table className="view-table" style={{display: "flex", alignItems: "flex-end"}}>
            <tbody>
              <tr>
                <td className="view-table-header">Hardware ID</td>
                <td className="view-table-header">Hardware Name</td>
                <td className="view-table-header">Current Rented</td>
              </tr>
              {projectInfo.hardware.map((item) => (
                <tr key={item.hardwareId}>
                  <td className="view-table-cell">
                    {item.hardwareId}
                  </td>

                  <td className="view-table-cell">
                    {item.hardwareName}
                  </td>

                  <td className="view-table-cell">
                    {item.currentRent}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
          <br/>
          <div className="button-container">
            <NavigateButton text="Check Out" destination="/check-out" data={{projectId: projectInfo.projectId, projectName: projectInfo.projectName}}/>
            <NavigateButton text="Check In" destination="/check-in" data={{projectId: projectInfo.projectId, projectName: projectInfo.projectName}}/>
          </div>
        </div>
      </div>
    </MainLayout>
  );
}

export default ViewProjectPage;