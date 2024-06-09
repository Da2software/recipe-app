import { Comment, User } from "./userApi";

export interface Recipe{
    id: number,
    title: string,
    ingredients: string[],
    directions: string[],
    image?: string,
    NER: string[],
    author_id: number,
    category: string,
    created_at?: Date,
    updated_at?: Date,
    onwner?: User,
    comments?: Comment[]
}
export interface RecipesPage{
    recipes: Recipe[],
    total?: number
}