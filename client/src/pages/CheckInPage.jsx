import { useState, useEffect } from "react";
import { useLocation } from "react-router-dom";
import MainLayout from "../components/layout/MainLayout.jsx";
import CheckInTable from "../components/table/CheckInTable.jsx";

function CheckInPage() {
  // Get project ID from location state
  const location = useLocation();
  const projectId = location.state?.projectId;

  // List of hardwares parameter
  const [hardwaresList, setHardwaresList] = useState([]);

  // List of checked-in items parameter
  const [checkInItems, setCheckInItems] = useState([]);

  // Fetch checked-in items from API
  function getCheckedInItems(projectId) {
    // Simulate API call
    const result = [
      {
        id: 1,
        name: "ABC",
        checkedOut: 1200
      },
      {
        id: 2,
        name: "DEF",
        checkedOut: 850
      }
    ];
    setHardwaresList(result);
  }

  // Handle table data change
  function handleTableChange(items) {
    setCheckInItems(items);
  }

  // Handle check-in form submission
  function handleCheckIn(event) {
    event.preventDefault();
    // call API to check in items
  }

  // Execute when component rendering
  useEffect(() => {
    getCheckedInItems(projectId);
  }, [projectId]);

  return (
    <MainLayout>
      <div style={{ display: "flex", flexDirection: "column", alignItems: "center"}}>
        <h1>Check In (ID: {projectId})</h1>
        <form onSubmit={handleCheckIn}>
          <CheckInTable
            hardwaresList={hardwaresList} // List of hardwares
            onDataChange={handleTableChange} // Handle table data change
          />
          <button type="submit" style={{ width: "100%"}}>Check In</button>
        </form>
      </div>
    </MainLayout>
  );
}

export default CheckInPage;