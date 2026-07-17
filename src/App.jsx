import { BrowserRouter, Routes, Route } from "react-router-dom";

import LoginPage from "./components/pages/LoginPage.jsx";
import MainPage from "./components/pages/MainPage.jsx";
import CreateUserPage from "./components/pages/CreateUserPage.jsx";
import CreateProjectPage from "./components/pages/CreateProjectPage.jsx";
import CheckInPage from "./components/pages/CheckInPage.jsx";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<LoginPage />} />
        <Route path="/create-user" element={<CreateUserPage />} />
        <Route path="/main-page" element={<MainPage />} />
        <Route path="/create-project" element={<CreateProjectPage />} />
        <Route path="/check-in" element={<CheckInPage />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;