import { useNavigate } from "react-router-dom";
import "../css/Button.css";

function NavigateButton({
  text,
  destination,
  data = null,
  type = "button",
  disabled = false,
}) {
  const navigate = useNavigate();

  function handleNavigate() {
    if (data !== null) {
      navigate(destination, {state: data});
    } else {
      navigate(destination);
    }
  }

  return (
    <button
      type={type}
      onClick={handleNavigate}
      className="custom-button"
      disabled={disabled}
    >
      {text}
    </button>
  );
}

export default NavigateButton;