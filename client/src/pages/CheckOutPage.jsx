import { useEffect, useState } from "react";
import { useLocation } from "react-router-dom";
import MainLayout from "../components/layout/MainLayout.jsx";
import CheckOutTable from "../components/table/CheckOutTable.jsx";

function CheckOutPage() {
  // Get project ID from location state
  const location = useLocation();
  const projectId = location.state?.projectId;

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
    console.log("Check out items:", checkOutItems);
    // call API to check out items
  }

  // Execute when component rendering
  useEffect(() => {
    getHardwareList(projectId);
  }, [projectId])

  return (
    <MainLayout>
      <div style={{ display: "flex", flexDirection: "column", alignItems: "center"}}>
        <h1>Check Out (ID: {projectId})</h1>
        <form onSubmit={handleCheckOut}>
          <CheckOutTable
            hardwaresList={hardwaresList} // Pass hardware list to table
            onDataChange={handleTableChange} // Handle data change from table
          />
          <button type="submit" style={{ width: "100%"}}>Check Out</button>
        </form>
      </div>
    </MainLayout>
  );
}

export default CheckOutPage;