import { BrowserRouter, Routes, Route } from "react-router-dom";

import LoginPage from "./pages/LoginPage.jsx";
import MainPage from "./pages/MainPage.jsx";
import CreateUserPage from "./pages/CreateUserPage.jsx";
import CreateProjectPage from "./pages/CreateProjectPage.jsx";
import JoinProjectPage from "./pages/JoinProjectPage.jsx";
import ViewProjectPage from "./pages/ViewProjectPage.jsx";
import CheckOutPage from "./pages/CheckOutPage.jsx";
import CheckInPage from "./pages/CheckInPage.jsx";
import ProtectedRoute from "./components/layout/ProtectedRoute.jsx";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* 不需要登入 */}
        <Route path="/" element={<LoginPage />} />
        <Route path="/create-user" element={<CreateUserPage />} />

        {/* 需要登入 */}
        <Route element={<ProtectedRoute />}>
          <Route path="/main-page" element={<MainPage />} />
          <Route path="/create-project" element={<CreateProjectPage />} />
          <Route path="/join-project" element={<JoinProjectPage />} />
          <Route path="/view-project" element={<ViewProjectPage />} />
          <Route path="/check-out" element={<CheckOutPage />} />
          <Route path="/check-in" element={<CheckInPage />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;