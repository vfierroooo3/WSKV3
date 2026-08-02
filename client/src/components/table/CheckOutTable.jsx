import { useState } from "react";
import "../css/Table.css";
function CheckOutTable({hardwaresList, onDataChange}) {
  // Request quantities parameter
  const [requests, setRequests] = useState({});

  // Handle request quantity change
  function handleRequestChange(hardwareNm, value) {
    const quantity = Number(value); // Convert input value to number
    
    // Update the requests state with the new quantity for the specific hardware
    const updatedRequests = {
      ...requests, // previous requests
      [hardwareNm]: quantity, // current hardware request
    };

    setRequests(updatedRequests); // Update the state to requests parameter

    // filter selected items (only those with a request quantity)
    const selectedItems = hardwaresList
      .map((item) => ({
        ...item,
        requestQuantity: updatedRequests[item.hwName] ?? 0,
      }))
      .filter((item) => item.requestQuantity > 0);

    onDataChange(selectedItems); // Call the onDataChange callback with the selected items
  }
  return (
    <div style={{ width: "100%", maxWidth: "900px", margin: "24px auto", overflowX: "auto" }}>
      <table className="check-table">
        <thead>
          <tr>
            <th className="check-table-header">Hardware Name</th>
            <th className="check-table-header">Capacity</th>
            <th className="check-table-header">Available</th>
            <th className="check-table-header">Request</th>
          </tr>
        </thead>

        <tbody>
          {hardwaresList.map((hardware) => (
            <tr key={hardware.hwName}>
              <td className="check-table-cell">{hardware.hwName}</td>
              <td className="check-table-cell">
                {hardware.capacity.toLocaleString()}
              </td>
              <td className="check-table-cell">{hardware.availability.toLocaleString()}</td>
              <td className="check-table-cell">
                <input
                  type="number"
                  min="0"
                  max={hardware.availability}
                  value={requests[hardware.hwName] ?? ""}
                  onChange={(event) =>
                    handleRequestChange(hardware.hwName, event.target.value)
                  }
                  style={{ width: "100%" }}
                />
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default CheckOutTable;