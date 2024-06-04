import { createSlice } from "@reduxjs/toolkit"

export interface IUserState{
    username: string,
    email: string,
    isAuth: boolean
}

const initialState: IUserState = {
    username: "",
    email: "",
    isAuth: false
}

export const userSlice = createSlice({
    name: "user",
    initialState, 
    reducers: {
        addUser: (state: IUserState, action)=>{
            const { username, email, isAuth } = action.payload;
            state.username = username;
            state.email = email;
            state.isAuth = isAuth;
        },
        changeUsername: (state: IUserState, action) => {
            state.username = action.payload;
        },
        changeEmail: (state: IUserState, action) => {
            state.email = action.payload;
        },
        changeAuth: (state: IUserState, action) => {
            state.isAuth = action.payload;
        },
    }
});

export const { addUser, changeUsername, changeEmail, changeAuth } = userSlice.actions;
export default userSlice.reducer;