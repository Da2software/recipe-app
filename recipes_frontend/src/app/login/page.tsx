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

export default function Login() {
  const [showPass, setShowPass] = React.useState(false);
  const [username, setUsername] = React.useState('');
  const [password, setPassword] = React.useState('');
  const router = useRouter();

  const handleChangeShowPass = (event: React.ChangeEvent<HTMLInputElement>) => {
    setShowPass(event.target.checked);
  };
  const onLogin = async(event: React.FormEvent)=>{
    event.preventDefault();

    const response = await fetch('/auth/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ username: username, password: password }),
    });

    if (response.ok) {
      // Redirect to another page upon successful login
      router.push('/dashboard');
    } else {
      // Handle login error
      alert('Login failed');
    }
  };
  return (
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
            <form
              className="grid grid-cols-1 rp-login mx-auto"
              id="login-form"
              onSubmit={onLogin}
            >
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
                required
                control={
                  <Checkbox value={showPass} onChange={handleChangeShowPass} />
                }
                label="Show Password"
              />
            </form>
          </CardContent>
          <CardActions className="w-100">
            <div className="flex mb-3 w-100 px-2">
              <Button variant="contained" type="submit" id="btn-login">
                Login
              </Button>
              <Button
                variant="contained"
                color="secondary"
                type="submit"
                className="ms-auto"
              >
                Sign Up
              </Button>
            </div>
          </CardActions>
        </Card>
      </Grid>
    </Grid>
  );
}
