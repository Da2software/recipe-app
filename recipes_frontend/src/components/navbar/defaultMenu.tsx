"use client";
import AppBar from '@mui/material/AppBar';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import Button from '@mui/material/Button';
import Link from 'next/link';
import Box from "@mui/material/Box";


export default function DefaulMenu(){
    return (
      <AppBar position="static">
        <Toolbar>
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            <Link href="/" passHref>
              Recipe App
            </Link>
          </Typography>
          <Box sx={{ display: "flex" }}>
            <Link href="/login" passHref>
              <Button color="inherit">Login</Button>
            </Link>
            <Link href="/signup" passHref>
              <Button color="inherit">Sign Up</Button>
            </Link>
          </Box>
        </Toolbar>
      </AppBar>
    );
}