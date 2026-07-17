import { BrowserRouter, Routes, Route } from "react-router-dom";

import LoginPage from "./pages/LoginPage.jsx";
import MainPage from "./pages/MainPage.jsx";
import CreateUserPage from "./pages/CreateUserPage.jsx";
import CreateProjectPage from "./pages/CreateProjectPage.jsx";
import EditProjectPage from "./pages/EditProjectPage.jsx";
import CheckOutPage from "./pages/CheckOutPage.jsx";
import CheckInPage from "./pages/CheckInPage.jsx";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<LoginPage />} />
        <Route path="/create-user" element={<CreateUserPage />} />
        <Route path="/main-page" element={<MainPage />} />
        <Route path="/create-project" element={<CreateProjectPage />} />
        <Route path="/edit-project" element={<EditProjectPage />} />
        <Route path="/check-out" element={<CheckOutPage />} />
        <Route path="/check-in" element={<CheckInPage />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;