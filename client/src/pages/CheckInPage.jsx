import { useState, useEffect, use } from "react";
import { useLocation } from "react-router-dom";
import "../components/css/Button.css"
import MainLayout from "../components/layout/MainLayout.jsx";
import CheckInTable from "../components/table/CheckInTable.jsx";
import sharedApi from "../components/api/api.jsx";

function CheckInPage() {
  // Get project ID from location state
  const location = useLocation();
  const projectId = location.state?.projectId;
  const projectName = location.state?.projectName;

  // Project info parameters
  const [hardwaresList, setHardwaresList] = useState([]);
  
  // List of checked-in items parameter
  const [checkInItems, setCheckInItems] = useState([]);

  // Handle table data change
  function handleTableChange(items) {
    setCheckInItems(items);
  }

  // Get my projects List
  async function getProjectsInfo(projectId){
    try {
      const result = await sharedApi("/get_project_info", "POST", { projectId });
      if (result.success) {
        setHardwaresList(result.project.hwSets);
      }
    } catch (error) {
      console.error("Error during get project info:", error);
    }
  }

  // Handle check-in form submission
  async function handleCheckIn(event) {
    event.preventDefault();
    try {
      const results = await Promise.all(
        checkInItems.map((item) =>
          sharedApi(
            "/check_in",
            "POST",
            {
              projectId: projectId,
              hwSetName: item.hwName,
              qty: item.requestQuantity
            }
          )
        )
      );

      const hasFailed = results.some((result) => !result.success);

      if (hasFailed) {
        setErrorMessage("Some items failed to check in.");
      } else {
        alert("All items checked out successfully!");
        getProjectsInfo(projectId); // Refresh the hardware list after check-in
      }

    } catch (error) {
      setErrorMessage("An error occurred while checking in the items.");
    }
  }

  useEffect(() => {
    getProjectsInfo(projectId);
  }, [projectId]);

  return (
    <MainLayout>
      <div style={{ display: "flex", flexDirection: "column", alignItems: "center"}}>
        <h1>Check In Rescoures</h1>
        <form onSubmit={handleCheckIn}>
          <h3>Project ID: {projectId}</h3>
          <h3>Project Name: {projectName}</h3>
          <CheckInTable
            hardwaresList={hardwaresList} // List of hardwares
            onDataChange={handleTableChange} // Handle table data change
          />
          <button type="submit" className="custom-button">Check In</button>
        </form>
      </div>
    </MainLayout>
  );
}

export default CheckInPage;