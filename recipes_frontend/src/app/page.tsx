import Image from "next/image";
import Container from '@mui/material/Container';
import { Grid, Typography } from "@mui/material";

export default function Home() {
  return (
    <Container maxWidth="md" className="my-5">
      <Grid container>
        <Grid item xs={12} md={6} className="flex">
          <Typography variant="h2" gutterBottom className="text-center my-auto">
            Welcome to Recipe App!
          </Typography>
        </Grid>
        <Grid item xs={12} md={6}>
          <img src={"/assets/home1.png"} alt="home image 1" className="w-100" />
        </Grid>
        <Grid item xs={12}>
          <Grid container direction={{ xs: "column-reverse", md: "row" }}>
            <Grid item xs={12} md={6} className="flex">
              <img
                src={"/assets/home3.png"}
                alt="home image 1"
                className="home3-img m-auto"
              />
            </Grid>
            <Grid item xs={12} md={6} className="flex">
              <Grid container className="my-auto">
                <Grid item xs={12}>
                  <Typography variant="h5" gutterBottom>
                    Discover, Create, and Savor Delicious Recipes
                  </Typography>
                </Grid>
                <Grid item xs={12}>
                  <Typography variant="body1" gutterBottom>
                    Are you passionate about cooking? Whether you’re a seasoned
                    chef or a kitchen novice, Recipe App is your culinary
                    companion. Explore a world of flavors, create your own
                    mouthwatering recipes, and organize your favorites—all in
                    one place.
                  </Typography>
                </Grid>
              </Grid>
            </Grid>
          </Grid>
        </Grid>
      </Grid>
    </Container>
  );
}
