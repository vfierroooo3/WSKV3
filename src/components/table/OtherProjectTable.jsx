function ProjectTable() {
  function getProjectList(){
    // Call API to fetch project list
  }
  // getProjectList()
  const projects = [
    {
      id: 1,
      name: "Project Alpha",
      status: "Active",
    },
    {
      id: 2,
      name: "Project Beta",
      status: "Active",
    },
    {
      id: 3,
      name: "Project Gamma",
      status: "Completed",
    },
  ];

  const tableStyle = {
    width: "530px",
    borderCollapse: "collapse",
    backgroundColor: "#ffffff",
  };

  const headerStyle = {
    padding: "12px",
    border: "1px solid #dddddd",
    backgroundColor: "#f3f4f6",
    textAlign: "left",
  };

  const cellStyle = {
    padding: "12px",
    border: "1px solid #dddddd",
    textAlign: "left",
  };

  return (
    <div
      style={{
        width: "100%",
        maxWidth: "900px",
        overflowX: "auto",
      }}
    >
      <table style={tableStyle}>
        <thead>
          <tr>
            <th style={headerStyle}>Project ID</th>
            <th style={headerStyle}>Project Name</th>
            <th style={headerStyle}>Status</th>
            <th style={headerStyle}>Action</th>
          </tr>
        </thead>

        <tbody>
          {projects.map((project) => (
            <tr key={project.id}>
              <td style={cellStyle}>{project.id}</td>
              <td style={cellStyle}>{project.name}</td>
              <td style={cellStyle}>{project.status}</td>
              <td style={{ ...cellStyle, display: "flex", gap: "10px" }}>
                <button type="button">
                  Check In
                </button>
                <button type="button">
                  Check Out
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default ProjectTable;