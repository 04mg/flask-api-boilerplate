import { useState } from "react";
import { LoginRegister } from "./components/LoginForm"
import UserInfo from "./hooks/UserInfo";


function App() {
  const [accessToken, setAccessToken] = useState("");

  return (
    <div className="flex justify-center items-center h-screen">
      {accessToken == "" ? <LoginRegister onLogin={setAccessToken} /> : <UserInfo accessToken={accessToken} />}
    </div>
  )
}

export default App
