import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { AlertCircle } from "lucide-react"
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert"
import { URL } from "@/constants"

export function LoginRegister({ onLogin }: { onLogin: (access: string) => void }) {
  const [activeTab, setActiveTab] = useState("login")
  const [error, setError] = useState("")

  const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    const formData = new FormData(event.currentTarget)
    const email = formData.get("email") as string
    const password = formData.get("password") as string

    if (!email || !password) {
      setError("Please fill in all fields")
      return
    }

    setError("")

    fetch(`${URL}/tokens/${activeTab}`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ email, password }),
    })
      .then((response) => {
        if (!response.ok) {
          response.json().then((data) => {
            setError(data.message)
          })
          return;
        }
        return response.json()
      })
      .then((data) => {
        onLogin(data.access_token)
      })
      .catch((error) => {
        setError(error.message)
      })
  }

  return (
    <Card className="w-[350px]">
      <CardHeader>
        <CardTitle>Welcome</CardTitle>
        <CardDescription>Login or create a new account</CardDescription>
      </CardHeader>
      <CardContent>
        <Tabs value={activeTab} onValueChange={setActiveTab}>
          <TabsList className="grid w-full grid-cols-2">
            <TabsTrigger value="login">Login</TabsTrigger>
            <TabsTrigger value="register">Register</TabsTrigger>
          </TabsList>
          <TabsContent value="login">
            <form onSubmit={handleSubmit}>
              <div className="grid w-full items-center gap-4">
                <div className="flex flex-col space-y-1.5">
                  <Label htmlFor="login-email">Email</Label>
                  <Input id="login-email" name="email" type="email" placeholder="Enter your email" />
                </div>
                <div className="flex flex-col space-y-1.5">
                  <Label htmlFor="login-password">Password</Label>
                  <Input id="login-password" name="password" type="password" placeholder="Enter your password" />
                </div>
              </div>
              <Button className="w-full mt-4" type="submit">Login</Button>
            </form>
          </TabsContent>
          <TabsContent value="register">
            <form onSubmit={handleSubmit}>
              <div className="grid w-full items-center gap-4">
                <div className="flex flex-col space-y-1.5">
                  <Label htmlFor="register-email">Email</Label>
                  <Input id="register-email" name="email" type="email" placeholder="Enter your email" />
                </div>
                <div className="flex flex-col space-y-1.5">
                  <Label htmlFor="register-password">Password</Label>
                  <Input id="register-password" name="password" type="password" placeholder="Create a password" />
                </div>
              </div>
              <Button className="w-full mt-4" type="submit">Register</Button>
            </form>
          </TabsContent>
        </Tabs>
      </CardContent>
      <CardFooter>
        {error && (
          <Alert variant="destructive">
            <AlertCircle className="h-4 w-4" />
            <AlertTitle>Error</AlertTitle>
            <AlertDescription>{error}</AlertDescription>
          </Alert>
        )}
      </CardFooter>
    </Card>
  )
}