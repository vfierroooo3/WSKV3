import "../css/Table.css";
import NavigateButton from "../button/NavigateButton";

function ProjectTable({ projects }) {
  return (
    <div style={{ width: "100%", maxWidth: "900px", overflowX: "auto" }}>
      <table className="project-table">
        <thead>
          <tr>
            <th className="project-table-header">Project ID</th>
            <th className="project-table-header">Project Name</th>
            <th className="project-table-header">Action</th>
          </tr>
        </thead>

        <tbody>
          {projects.length === 0 ? (
            <tr>
              <td colSpan="3" className="project-table-cell">No projects available.</td>
            </tr>
          ) : projects.map((project) => (
            <tr key={projects.projectId}>
              <td className="project-table-cell">{project.projectId}</td>
              <td className="project-table-cell">{project.projectName}</td>
              <td className="project-table-cell" style={{ display: "flex", alignItems: "center" }}>
                <NavigateButton text="View" destination="/view-project" data={{ projectId: project.projectId }}/>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default ProjectTable;