import { useEffect, useState } from "react";
import { useLocation } from "react-router-dom";
import "../components/css/Button.css"
import MainLayout from "../components/layout/MainLayout.jsx";
import CheckOutTable from "../components/table/CheckOutTable.jsx";

function CheckOutPage() {
  // Get project ID from location state
  const location = useLocation();
  const projectId = location.state?.projectId;
  const projectName = location.state?.projectName;
  
  // hardware list parameters
  const [hardwaresList, setHardwaresList] = useState([]);

  // Check out items parameters
  const [checkOutItems, setCheckOutItems] = useState([]);

  // Get hardware list from API
  function getHardwareList(projectId) {
    // Simulate API call
    const result = [
      {
        id: 1,
        name: "ABC",
        capacity: 1200,
        available: 1200,
      },
      {
        id: 2,
        name: "DEF",
        capacity: 850,
        available: 850,
      }
    ];
    setHardwaresList(result);
  }

  // Check out items change handler
  function handleTableChange(items) {
    setCheckOutItems(items);
  }

  // Check out items submit handler
  function handleCheckOut(event) {
    event.preventDefault();
    // call API to check out items
  }

  // Execute when component rendering
  useEffect(() => {
    getHardwareList(projectId);
  }, [projectId])

  return (
    <MainLayout>
      <div style={{ display: "flex", flexDirection: "column", alignItems: "center"}}>
        <h1>Check Out Resources</h1>
        <form onSubmit={handleCheckOut}>
          <h3>Project ID: {projectId}</h3>
          <h3>Project Name: {projectName}</h3>
          <CheckOutTable
            hardwaresList={hardwaresList} // Pass hardware list to table
            onDataChange={handleTableChange} // Handle data change from table
          />
          <button type="submit" className="custom-button">Check Out</button>
        </form>
      </div>
    </MainLayout>
  );
}

export default CheckOutPage;