import { Recipe, RecipesPage } from "@/models/recipeApi";

// #region queries
const dashboardQuery =`
{
    recipesPage(page: $page){
      recipes{
        id
        title
        image
        authorId
        ingredients
        directions
        NER
        category
        owner {
          id
          userName
        },
        comments{
          text,
          replies{
            text
          }
        }
      }
      $total
      }
  }
`
// #endregion queries

export class RecipeController {
    baseUrl: string = process.env.RECIPES_API + "/graphql";

    toRecipe(recipe: Object | any): Recipe {
        return {
            id: recipe["id"],
            title: recipe["title"],
            image: recipe["image"],
            author_id: recipe["author_id"],
            category: recipe["category"],
            directions: recipe["directions"],
            ingredients: recipe["ingredients"],
            NER: recipe["NER"],
            created_at: recipe["created_at"],
            updated_at: recipe["updated_at"],
            onwner: recipe["user"],
            comments: recipe["comments"]
        }
    }

    async getDashboard(page=1, showTotal = true): Promise<RecipesPage>{
        let query = dashboardQuery.replace("$page", page.toString());
        query = query.replace("$total", showTotal ? "total" : "")
        let result: any = await fetch(this.baseUrl, {
            method: 'POST',
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                query: query
            })
        });
        // in case it fails we return empty
        if (!result.ok) return { recipes: [] }
        result = await result.json();
        const recipesPage = result.data.recipesPage;
        return recipesPage;
    }
}   