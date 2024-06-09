"use client";

import { RecipeController } from "@/api/recipeApi";
import RecipeReviewCard from "@/components/recipes/recipeCard";
import { Recipe } from "@/models/recipeApi";
import { Container, Grid } from "@mui/material";
import React, { useEffect } from "react";
const recipeController: RecipeController = new RecipeController();
const recipesRetrieve = (setRecipes: any) => {
    recipeController.getDashboard(1, true).then((res) => {
      setRecipes(res.recipes);
    });
  };
export default function Dashboard() {
  const [recipes, setRecipes] = React.useState<Recipe[]>([]);
  useEffect(()=>{
      recipesRetrieve(setRecipes);
  })
  const recipeCards = recipes.map((recipe) => (
    <Grid xs={12} sm={12} md={6}>
        <RecipeReviewCard recipe={recipe}></RecipeReviewCard>
    </Grid>
  ));
  return (
    <Container maxWidth="md">
      <Grid container>{recipeCards}</Grid>
    </Container>
  );
}
