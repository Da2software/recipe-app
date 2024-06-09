export interface User {
    id: number,
    email: string,
    user_name: string
}

export interface Comment {
    id: number,
    recipe_id: string,
    text: string,
    user_id: number,
    is_sub: boolean,
    comment_id?: number,
    created_at: Date,
    replies?: Comment[],
    owner: User
}

export interface Stars {
    recipe_id: string,
    total: number
}