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
import { json } from "stream/consumers";

export default function SignUp() {
  const [showPass, setShowPass] = React.useState(false);
  const [username, setUsername] = React.useState('');
  const [email, setEmail] = React.useState('');
  const [password, setPassword] = React.useState('');
  const [vPassword, setVPassword] = React.useState('');
  const router = useRouter();

  const handleChangeShowPass = (event: React.ChangeEvent<HTMLInputElement>) => {
    setShowPass(event.target.checked);
  };
  const onSignUp = async (event: React.FormEvent) => {
    event.preventDefault();
    const body = {
      username: username,
      email: email,
      password: password,
    };

    const response = await fetch(process.env.USERS_API + "/auth/signup", {
      method: "POST",
      credentials: "same-origin",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
      body: JSON.stringify(body),
    });

    if (response.ok) {
      router.push("/login");
    } else {
      alert("Sign Up failed");
    }
  };
  return (
    <form action="login" id="login-form" onSubmit={(e) => onSignUp(e)}>
      <Grid container className="px-2 w-100">
        <Grid item xs={12} sm={8} md={6} lg={4} xl={3} className="m-auto">
          <Card className="my-5" variant="outlined">
            <CardContent>
              <img
                src={"/assets/signup.jpeg"}
                alt="login-image"
                className="login-img"
              />
              <Typography variant="h3" gutterBottom className="text-center">
                Sign Up
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
                  id="email"
                  label="Email"
                  variant="filled"
                  placeholder="Email"
                  required
                  className="my-2"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
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
                <TextField
                  id="check_password"
                  label="Verify Password"
                  type={showPass ? "text" : "password"}
                  variant="filled"
                  placeholder="Verify password"
                  className="my-2"
                  value={vPassword}
                  onChange={(e) => setVPassword(e.target.value)}
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
                <Button variant="contained" type="submit" onSubmit={onSignUp}>
                  Sign Up
                </Button>
                <Button
                  variant="contained"
                  id="btn-login"
                  color="secondary"
                  className="ms-auto"
                  onClick={(e) => router.push("/login")}
                >
                  Login
                </Button>
              </div>
            </CardActions>
          </Card>
        </Grid>
      </Grid>
    </form>
  );
}
