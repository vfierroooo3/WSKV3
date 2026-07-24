import { useNavigate } from "react-router-dom";
import NavigateButton from "../button/NavigateButton";
import "../css/Table.css";
function ProjectTable({ projects }) {
  const navigate = useNavigate();

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
          {projects.map((project) => (
            <tr key={project.id}>
              <td className="project-table-cell">{project.id}</td>
              <td className="project-table-cell">{project.name}</td>
              <td className="project-table-cell" style={{ display: "flex", alignItems: "center" }}>
                <NavigateButton text="View" destination="/view-project" data={{ projectId: project.id }}/>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default ProjectTable;