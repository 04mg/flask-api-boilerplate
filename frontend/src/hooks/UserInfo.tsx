import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import { useEffect, useState } from "react"
import { URL } from "@/constants"

export default function UserInfo({ accessToken }: { accessToken: string }) {
  const [email, setEmail] = useState("")

  useEffect(() => {
    fetch(`${URL}/users/me`, {
      headers: {
        Authorization: `${accessToken}`
      }
    })
      .then(response => response.json())
      .then(data => setEmail(data.email))
  })

  return (
    <Card className="w-full max-w-md mx-auto">
      <CardHeader className="flex flex-row items-center gap-4 space-y-0">
        <Avatar className="w-16 h-16">
          <AvatarImage src={`https://api.dicebear.com/6.x/initials/svg?seed=${email}`} alt={email} />
          <AvatarFallback>{email}</AvatarFallback>
        </Avatar>
        <div className="flex-1">
          <CardTitle className="text-2xl">{email}</CardTitle>
        </div>
      </CardHeader>
      <CardContent>
        <div className="text-sm text-neutral-500 dark:text-neutral-400">
          You are <strong>logged in</strong>.
        </div>
      </CardContent>
    </Card>
  )
}