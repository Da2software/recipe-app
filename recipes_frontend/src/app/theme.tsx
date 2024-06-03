"use client";
import { amber, deepOrange } from '@mui/material/colors';
import { createTheme, ThemeProvider, styled } from '@mui/material/styles';

declare module '@mui/material/styles' {
  interface Theme {
    status: {
      danger: string;
    };
  }
  // allow configuration using `createTheme`
  interface ThemeOptions {
    status?: {
      danger?: string;
    };
  }
}


const theme = createTheme({
  palette: {
    primary: amber,
    secondary: deepOrange,
  },
});

export default function ThemeProviderContainer({ children }: any) {
    return (
      <ThemeProvider theme={theme}>
        {children}
      </ThemeProvider>
    );
  }
