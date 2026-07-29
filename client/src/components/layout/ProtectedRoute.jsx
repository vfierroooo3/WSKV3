import { Navigate, Outlet } from "react-router-dom";

function ProtectedRoute() {
  const isLogin = localStorage.getItem("isLogin") === "true";

  if (!isLogin) {
    return <Navigate to="/" replace />;
  }

  return <Outlet />;
}

export default ProtectedRoute;