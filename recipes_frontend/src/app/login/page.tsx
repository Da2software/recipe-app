"use client";
import * as React from "react";
import Button from "@mui/material/Button";
import {
  CardActions,
  Card,
  CardContent,
  TextField,
  Typography,
  Checkbox,
  FormControlLabel,
  Grid,
} from "@mui/material";
import { useRouter } from "next/navigation";
import { useDispatch } from "react-redux";
import { IUserState, addUser } from "../userSlice";

export default function Login() {
  const [showPass, setShowPass] = React.useState(false);
  const [username, setUsername] = React.useState('');
  const [password, setPassword] = React.useState('');
  const router = useRouter();
  const dispatch = useDispatch()

  const handleChangeShowPass = (event: React.ChangeEvent<HTMLInputElement>) => {
    setShowPass(event.target.checked);
  };
  const setUserState = ()=>{
    fetch(process.env.USERS_API + "/auth/", {
      method: "GET",
      credentials: "same-origin",
    }).then((res) => {
      if (res.ok) {
        const body: any = res.body;
        const userRes: IUserState = {
          username: body["user_name"],
          email: body["email"],
          isAuth: true,
        };
        dispatch(addUser(userRes));
      } else {
        console.warn("User not authenticated!");
      }
    });
    
  };
  const onLogin = async (event: React.FormEvent) => {
    event.preventDefault();

    const response = await fetch(process.env.USERS_API + "/auth/token", {
      method: "POST",
      credentials: "same-origin",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
      body: new URLSearchParams({
        username: username,
        password: password,
      }),
    });

    if (response.ok) {
      setUserState();
      router.push("/dashboard");
    } else {
      alert("Login failed");
    }
  };
  return (
    <form action="login" id="login-form" onSubmit={(e) => onLogin(e)}>
      <Grid container className="px-2 w-100">
        <Grid item xs={12} sm={8} md={6} lg={4} xl={3} className="m-auto">
          <Card className="my-5" variant="outlined">
            <CardContent>
              <img
                src={"/assets/login.jpeg"}
                alt="login-image"
                className="login-img"
              />
              <Typography variant="h3" gutterBottom className="text-center">
                Login
              </Typography>
              <div className="grid grid-cols-1 rp-login mx-auto">
                <TextField
                  id="username"
                  label="Username"
                  variant="filled"
                  placeholder="Username"
                  required
                  className="my-2"
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                />
                <TextField
                  id="password"
                  label="Password"
                  type={showPass ? "text" : "password"}
                  variant="filled"
                  placeholder="password"
                  className="my-2"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  required
                />
                <FormControlLabel
                  control={
                    <Checkbox
                      value={showPass}
                      onChange={handleChangeShowPass}
                    />
                  }
                  label="Show Password"
                />
              </div>
            </CardContent>
            <CardActions className="w-100">
              <div className="flex mb-3 w-100 px-2">
                <Button variant="contained" type="submit" id="btn-login">
                  Login
                </Button>
                <Button
                  variant="contained"
                  color="secondary"
                  className="ms-auto"
                  onClick={(e) => router.push("/signup")}
                >
                  Sign Up
                </Button>
              </div>
            </CardActions>
          </Card>
        </Grid>
      </Grid>
    </form>
  );
}
